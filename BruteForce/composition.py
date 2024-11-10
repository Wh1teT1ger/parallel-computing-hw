import hashlib
from typing import Callable
from typing import List

def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

class Composition:
    def __init__(self, hash_list: List[Callable[[bytes], bytes]]):
        self.hash_list = hash_list
        
    def hash(self, data: bytes) -> bytes:
        text = data
        for hash in self.hash_list:
            text = hash(text)
        return text
    
    