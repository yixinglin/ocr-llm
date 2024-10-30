import base64

def base64_encode(data: bytes):
    return base64.b64encode(data).decode('utf-8')

def base64_decode(data: str) -> bytes:
    return base64.b64decode(data.encode('utf-8'))


import hashlib

def file_to_md5(data: bytes):
    return hashlib.md5(data).hexdigest()
