"""
microcoap.py — Minimal CoAP library for MicroPython (ESP32)
============================================================
A tiny implementation of the Constrained Application Protocol (RFC 7252).
Supports GET and PUT methods for CoAP server use on ESP32.

This file goes on your ESP32 alongside coap_smart_home.py.
"""

import socket
import struct
import json

# ── CoAP constants ──
COAP_PORT = 5683
COAP_VERSION = 1

# Method codes
COAP_GET = 1
COAP_POST = 2
COAP_PUT = 3
COAP_DELETE = 4

# Response codes (class.detail → single byte encoding)
COAP_CREATED = 65       # 2.01
COAP_DELETED = 66       # 2.02
COAP_VALID = 67         # 2.03
COAP_CHANGED = 68       # 2.04
COAP_CONTENT = 69       # 2.05
COAP_BAD_REQUEST = 128  # 4.00
COAP_NOT_FOUND = 132    # 4.04
COAP_METHOD_NOT_ALLOWED = 133  # 4.05

# Message types
COAP_CON = 0   # Confirmable
COAP_NON = 1   # Non-confirmable
COAP_ACK = 2   # Acknowledgement
COAP_RST = 3   # Reset

# Option numbers
OPT_URI_PATH = 11
OPT_CONTENT_FORMAT = 12

# Content formats
CT_TEXT = 0
CT_JSON = 50


class CoapPacket:
    """Parsed CoAP message."""
    def __init__(self):
        self.version = COAP_VERSION
        self.type = COAP_CON
        self.code = 0
        self.message_id = 0
        self.token = b''
        self.options = []
        self.payload = b''

    @property
    def method(self):
        return self.code

    @property
    def uri_path(self):
        """Extract full URI path from options (e.g. 'sensors' or 'led')."""
        parts = []
        for opt_num, opt_val in self.options:
            if opt_num == OPT_URI_PATH:
                parts.append(opt_val.decode() if isinstance(opt_val, bytes) else opt_val)
        return '/'.join(parts)


def parse_packet(data):
    """Parse raw bytes into a CoapPacket."""
    if len(data) < 4:
        return None

    pkt = CoapPacket()
    byte0 = data[0]
    pkt.version = (byte0 >> 6) & 0x03
    pkt.type = (byte0 >> 4) & 0x03
    tkl = byte0 & 0x0F
    pkt.code = data[1]
    pkt.message_id = struct.unpack('!H', data[2:4])[0]

    offset = 4

    # Token
    if tkl > 0:
        pkt.token = data[offset:offset + tkl]
        offset += tkl

    # Options
    prev_opt = 0
    while offset < len(data):
        if data[offset] == 0xFF:  # Payload marker
            offset += 1
            break
        delta = (data[offset] >> 4) & 0x0F
        length = data[offset] & 0x0F
        offset += 1

        if delta == 13:
            delta = data[offset] + 13
            offset += 1
        elif delta == 14:
            delta = struct.unpack('!H', data[offset:offset+2])[0] + 269
            offset += 2

        if length == 13:
            length = data[offset] + 13
            offset += 1
        elif length == 14:
            length = struct.unpack('!H', data[offset:offset+2])[0] + 269
            offset += 2

        opt_num = prev_opt + delta
        opt_val = data[offset:offset + length]
        offset += length
        pkt.options.append((opt_num, opt_val))
        prev_opt = opt_num

    # Payload
    if offset < len(data):
        pkt.payload = data[offset:]

    return pkt


def build_response(msg_type, code, msg_id, token, payload=b'', content_format=CT_JSON):
    """Build a CoAP response packet as bytes."""
    if isinstance(payload, str):
        payload = payload.encode()

    tkl = len(token)
    byte0 = (COAP_VERSION << 6) | (msg_type << 4) | tkl
    header = struct.pack('!BBH', byte0, code, msg_id)

    data = header + token

    # Add Content-Format option if we have a payload
    if payload:
        # Option delta=12 (Content-Format), length=1
        opt_byte = (OPT_CONTENT_FORMAT << 4) | 1
        data += struct.pack('!BB', opt_byte, content_format)
        # Payload marker + payload
        data += b'\xFF' + payload

    return data


class CoapServer:
    """Minimal CoAP server for MicroPython."""

    def __init__(self, port=COAP_PORT):
        self.port = port
        self.resources = {}
        self.sock = None

    def add_resource(self, path, callback):
        """Register a resource handler.
        
        callback(method, payload) should return (response_code, response_payload).
        - method: COAP_GET or COAP_PUT
        - payload: bytes (request body, empty for GET)
        Returns: (code, payload_string)
        """
        self.resources[path] = callback

    def start(self):
        """Start listening for CoAP requests on UDP port."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.setblocking(False)
        print(f"  CoAP server listening on UDP port {self.port}")

    def poll(self):
        """Check for and handle one incoming packet. Non-blocking."""
        try:
            data, addr = self.sock.recvfrom(256)
        except OSError:
            return  # No data available

        pkt = parse_packet(data)
        if pkt is None:
            return

        uri = pkt.uri_path
        method = pkt.method

        if uri in self.resources:
            try:
                code, resp_payload = self.resources[uri](method, pkt.payload)
            except Exception as e:
                print("Resource error:", e)
                code = COAP_BAD_REQUEST
                resp_payload = json.dumps({"error": str(e)})
        else:
            code = COAP_NOT_FOUND
            resp_payload = json.dumps({"error": "not found"})

        # Build and send response
        if pkt.type == COAP_CON:
            resp_type = COAP_ACK
        else:
            resp_type = COAP_NON

        response = build_response(resp_type, code, pkt.message_id, pkt.token, resp_payload)
        self.sock.sendto(response, addr)

    def stop(self):
        """Stop the server."""
        if self.sock:
            self.sock.close()
            self.sock = None
