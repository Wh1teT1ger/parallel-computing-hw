import hashlib
from BruteForce import *

def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def test_linear(steeps):
    times = []
    numbers = []
    steep = 100
    hash_list = [hash_sha256,  hash_sha256,  hash_sha256]
    composition = composition.Composition(hash_list)
    target_hash = composition.hash(b"helloword")
    while steep < steeps:
        manager = LinearBruteForce(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=8, hash_function=composition.hash)
        result = manager.brute_force(target_hash)
        