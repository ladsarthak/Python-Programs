from decimal import Decimal, getcontext
import time

# ============================================
# CONFIG
# ============================================

DIGITS = int(input("Enter the number of digits of pi to compute: "))
DELAY = 0.000000000000000001
OUTPUT_FILE = "pi.txt"

# ============================================
# CHUDNOVSKY ALGORITHM
# ============================================

def compute_pi(n_digits):
    getcontext().prec = n_digits + 10

    C = 426880 * Decimal(10005).sqrt()

    M = 1
    L = 13591409
    X = 1
    K = 6
    S = Decimal(L)

    iterations = n_digits // 14 + 1

    for i in range(1, iterations):
        M = (M * (K**3 - 16*K)) // (i**3)
        L += 545140134
        X *= -262537412640768000
        term = Decimal(M * L) / X
        S += term
        K += 12

    pi = C / S

    return str(pi)[:n_digits + 2]

# ============================================
# MAIN
# ============================================

print("Computing pi...\n")

pi_digits = compute_pi(DIGITS)

current = ""

for char in pi_digits:
    current += char

    # print current value
    print(current)

    # update file continuously
    with open(OUTPUT_FILE, "w") as f:
        f.write(current)

    time.sleep(DELAY)

print(f"Final value saved to {OUTPUT_FILE}")