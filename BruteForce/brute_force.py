import hashlib
import itertools
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
from queue import Queue

class BruteForce:
    def __init__(self, alphabet: str, max_size: int, workers_num: int, hash_function: Callable[[bytes], bytes], steps=None):
        self.alphabet = alphabet
        self.max_size = max_size
        self.workers_num = workers_num
        self.hash_function = hash_function
        self.hash_counter = 0
        self.lock = threading.Lock()
        self.steps = steps

    def brute_force(self, target: bytes) -> Optional[str]:
        def worker(input_queue, output_queue, found: threading.Event):
            while True:
                text = input_queue.get()
                if text == None:
                    return
                if found.is_set():
                    return
                with self.lock:
                    if self.steps and self.hash_counter >= self.steps:
                        return
                    self.hash_counter += 1
                candidate = self.hash_function(text.encode())
                if candidate == target:
                    output_queue.put(text)
                    found.set()
                    return

    

        
        input_queue = Queue()
        output_queue = Queue()
        threads = []
        found = threading.Event()

        for combination in self._generate_combinations():
            input_queue.put(combination)
        
        for _ in range(self.workers_num):
            thread = threading.Thread(target=worker, args=(input_queue, output_queue, found))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            


        return output_queue.get() if not output_queue.empty() else None
    
    def _generate_combinations(self):
        for size in range(1, self.max_size + 1):
            for combination in itertools.product(self.alphabet, repeat=size):
                yield ''.join(combination)

# Пример использования
def hash_function(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

if __name__ == "__main__":
    manager = BruteForce(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=4, workers_num=4, hash_function=hash_function)
    target_hash = hash_function(b"pass")
    print("start")
    result = manager.brute_force(target_hash)
    print("Found match:", result)