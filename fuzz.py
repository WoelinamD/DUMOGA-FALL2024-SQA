import random
import math
import statistics

def fuzz_sqrt():
    print("Fuzzing sqrt...")
    for _ in range(10):  # Generate 10 test cases
        try:
            value = random.uniform(-1000, 1000)  # Random float in a range
            result = math.sqrt(value)
            print(f"math.sqrt({value}) = {result}")
        except Exception as e:
            print(f"math.sqrt({value}) raised {type(e).__name__}: {e}")

def fuzz_average():
    print("Fuzzing average...")
    for _ in range(10):
        try:
            size = random.randint(0, 10)  # List size between 0 and 10
            values = [random.uniform(-1000, 1000) for _ in range(size)]
            result = statistics.mean(values)
            print(f"statistics.mean({values}) = {result}")
        except Exception as e:
            print(f"statistics.mean({values}) raised {type(e).__name__}: {e}")

def fuzz_median():
    print("Fuzzing median...")
    for _ in range(10):
        try:
            size = random.randint(0, 10)
            values = [random.uniform(-1000, 1000) for _ in range(size)]
            result = statistics.median(values)
            print(f"statistics.median({values}) = {result}")
        except Exception as e:
            print(f"statistics.median({values}) raised {type(e).__name__}: {e}")

def fuzz_mode():
    print("Fuzzing mode...")
    for _ in range(10):
        try:
            size = random.randint(0, 10)
            values = [random.choice([1, 2, 3, 4, 5]) for _ in range(size)]  # Random integers with potential duplicates
            result = statistics.mode(values)
            print(f"statistics.mode({values}) = {result}")
        except Exception as e:
            print(f"statistics.mode({values}) raised {type(e).__name__}: {e}")

def fuzz_sum():
    print("Fuzzing sum...")
    for _ in range(10):
        try:
            size = random.randint(0, 10)
            values = [random.uniform(-1000, 1000) for _ in range(size)]
            result = sum(values)
            print(f"sum({values}) = {result}")
        except Exception as e:
            print(f"sum({values}) raised {type(e).__name__}: {e}")

if __name__ == "__main__":
    fuzz_sqrt()
    fuzz_average()
    fuzz_median()
    fuzz_mode()
    fuzz_sum()