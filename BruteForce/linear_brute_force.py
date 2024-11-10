import hashlib
import itertools
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
import composition

class LinearBruteForce:
    def __init__(self, alphabet: str, max_size: int, hash_function: Callable[[bytes], bytes], steps=None):
        self.alphabet = alphabet
        self.max_size = max_size
        self.steps = steps
        self.hash_function = hash_function
        self.hash_counter = 0
        
    def _generate_combinations(self):
        for size in range(1, self.max_size + 1):
            for combination in itertools.product(self.alphabet, repeat=size):
                yield ''.join(combination)
                    
    def brute_force(self, target: bytes) -> Optional[str]:
        step: int = 0
        for combination in self._generate_combinations():
            if self.steps and step >= self.steps:
                break
            candidate = self.hash_function(combination.encode())
            if candidate == target:
                return combination
            step += 1
        return None

def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

if __name__ == "__main__":
    hash_list = [hash_sha256,  hash_sha256,  hash_sha256]
    composition = composition.Composition(hash_list)
    target_hash = composition.hash(b"pass")
    manager = LinearBruteForce(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=8, hash_function=composition.hash)
    print("start")
    result = manager.brute_force(target_hash)
    print("Found match:", result)