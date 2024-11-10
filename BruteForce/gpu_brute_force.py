import numpy as np
import hashlib
from numba import cuda
import itertools
import composition


# CUDA kernel for computing SHA-256 hash and comparing with target
@cuda.jit
def brute_force_sha256_kernel(combinations, target_hash, match_index, hash):
    # Thread index
    idx = cuda.grid(1)

    # Check if index is within bounds
    if idx < combinations.shape[0]:
        candidate = combinations[idx]

        # Calculate SHA-256 hash
        sha256_hash = hash(candidate)

        # Compare with target hash
        if sha256_hash == target_hash:
            match_index[0] = idx  # Set match index
            cuda.syncthreads()  # Synchronize to stop further checks

def brute_force_sha256(target_hash, alphabet, max_size, hash, batch_size=1024):
    target_hash_gpu = np.array(bytearray(target_hash), dtype=np.uint8)
    match_index = np.array([-1], dtype=np.int32)  # To store the index of a match if found

    target_hash_gpu = cuda.to_device(target_hash_gpu)
    match_index_gpu = cuda.to_device(match_index)
    print('Start')
    # Generate combinations in batches
    for batch in generate_combinations_batch(alphabet, max_size, batch_size):
        print(batch)
        batch_gpu = cuda.to_device(np.array(batch, dtype=np.object))

        # Launch kernel
        threads_per_block = 128
        blocks_per_grid = (len(batch) + (threads_per_block - 1)) // threads_per_block
        brute_force_sha256_kernel[blocks_per_grid, threads_per_block](batch_gpu, target_hash_gpu, match_index_gpu)

        # Copy result back to check if a match was found
        match_index_gpu.copy_to_host(match_index)
        if match_index[0] != -1:
            return batch[match_index[0]].decode()

    return None  # No match found in any batch

# Generate combinations in batches to limit memory usage
def generate_combinations_batch(alphabet, max_size, batch_size):
    for size in range(1, max_size + 1):
        combinations = itertools.product(alphabet, repeat=size)
        batch = []
        for comb in combinations:
            batch.append(''.join(comb).encode())
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
    
def hash_sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

# Example usage
if __name__ == "__main__":
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    max_size = 4
    hash_list = [hash_sha256,  hash_sha256,  hash_sha256]
    composition = composition.Composition(hash_list)
    target_hash = composition.hash(b"pass")
    result = brute_force_sha256(target_hash, alphabet, max_size, composition.hash)
    if result:
        print(f"Match found: {result}")
    else:
        print("No match found.")
