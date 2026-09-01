#!/usr/bin/env python3
# Purpose: minimal raw-CDP client for Chrome remote debugging (no third-party deps)
# Usage:
#   cdp.py eval "<js>" [tab_url_substring]     # evaluate JS, print result
#   cdp.py tabs                                # list tabs (id, title, url)
#   cdp.py navigate <url> [tab_url_substring]
# Dependencies: python3 stdlib only. Working dir: anywhere.
import json, socket, base64, os, struct, sys, urllib.request

DEBUG_HOST = "localhost:9222"

def http(method, path, body=None):
    s = socket.create_connection((DEBUG_HOST.split(":")[0], 9222), timeout=10)
    req = f"{method} {path} HTTP/1.1\r\nHost: localhost:9222\r\nConnection: close\r\n\r\n"
    body_bytes = body.encode() if body else b""
    if body:
        s.sendall((f"{method} {path} HTTP/1.1\r\nHost: {DEBUG_HOST}\r\nContent-Length: {len(body_bytes)}\r\nConnection: close\r\n\r\n").encode())
        s.send(body_bytes)
    else:
        s.send(req.encode())
    data = b""
    while True:
        chunk = s.recv(65536)
        if not chunk: break
        data += chunk
    s.close()
    return data

class WS:
    def __init__(self, url):
        assert url.startswith("ws://")
        rest = url[len("ws://"):].split("/")
        hostport, path = rest[0], "/" + "/".join(rest[1:])
        host, port = hostport.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=30)
        key = os.urandom(16).hex()
        req = (f"GET {path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
               f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        assert b"101" in resp.split(b"\r\n")[0], resp[:200]
    def send(self, obj):
        payload = json.dumps(obj).encode()
        header = bytearray([0x81])
        n = len(payload)
        if n < 126: header.append(0x80 | n)
        elif n < 65536: header += bytes([0x80|126, n>>8, n&0xff])
        else: header += bytes([0x80|127]) + n.to_bytes(8,"big")
        mask = os.urandom(4)
        header += mask
        masked = bytes(b ^ mask[i%4] for i,b in enumerate(payload))
        self.sock.sendall(bytes(header)+masked)
    def recv_msg(self):
        def read_exact(n):
            buf=b""
            while len(buf)<n:
                chunk=self.sock.recv(n-len(buf))
                if not chunk: raise EOFError
                buf+=chunk
            return buf
        b1,b2 = self.sock.recv(2)
        ln = b2 & 0x7f
        if ln==126: ln = struct.unpack(">H", self.sock.recv(2))[0]
        elif ln==127: ln = struct.unpack(">Q", self.sock.recv(8))[0]
        if b2 & 0x80: self.sock.recv(4)  # (server shouldn't mask)
        payload = read_exact(ln) if ln else b""
        opcode = b1 & 0x0f
        if opcode == 1: return json.loads(payload)
        if opcode == 9:  # ping -> pong
            self.sock.sendall(bytes([0x8a, 0x80]) + os.urandom(4))
            return self.recv_msg()
        return self.recv_msg()
    def cmd(self, method, params=None, _id=[0]):
        _id[0]+=1
        self.send({"id":_id[0],"method":method,"params":params or {}})
        while True:
            msg=self.recv_msg()
            if msg.get("id")==_id[0]:
                return msg
    def close(self): self.sock.close()

def get_tab(match=None):
    tabs=json.load(urllib.request.urlopen(f"http://{DEBUG_HOST}/json"))
    pages=[t for t in tabs if t["type"]=="page"]
    if match:
        pages=[t for t in pages if match in t["url"] or match in t["title"]]
    return pages[0]

if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="tabs":
        for t in json.load(urllib.request.urlopen(f"http://{DEBUG_HOST}/json")):
            if t["type"]=="page": print(t["id"][:8], "|", t["title"][:50], "|", t["url"][:80])
    elif cmd=="eval":
        expr, match = sys.argv[2], (sys.argv[3] if len(sys.argv)>3 else None)
        ws=WS(get_tab(match)["webSocketDebuggerUrl"])
        r=ws.cmd("Runtime.evaluate",{"expression":expr,"returnByValue":True})
        print(json.dumps(r.get("result",{}).get("result",{}).get("value")))
        ws.close()
    elif cmd=="navigate":
        url, match = sys.argv[2], (sys.argv[3] if len(sys.argv)>3 else None)
        ws=WS(get_tab(match)["webSocketDebuggerUrl"])
        ws.cmd("Page.navigate",{"url":url})
        print("navigated to", url)
        ws.close()
