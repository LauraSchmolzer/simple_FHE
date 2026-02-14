import numpy as np

# ----------------------------- Parameters -----------------------------
# 0 =< p , q ∈ Z, p =< q , ∆ = q/p, p & q are powers of 2

k = 2                       # number of mask polynomials
N = 4                       # degree of polynomials
q = 4                       # ciphertext modulus
p = 2                       # plaintext modulus
delta = q // p              # scaling factor for messages


# Secret key
S = [np.random.randint(0, q, N) for _ in range(k)]

# ----------------------------- Helper Functions -----------------------------
## Encoding message
def encode(M):
    return np.array([delta*m for m in M], dtype=int)

## Sample mask polynomials and small noise
def sample_polynomials(k,degree,mod):
    return [np.random.randint(0, mod, degree) for _ in range(k)]

def sample_noise(degree):
    return np.random.randint(-1, 2, degree)  # toy Gaussian

# ----------------------------- Encryption Procedure -----------------------------
def encrypt(S,M):
    A = sample_polynomials(k,N,q)
    e = sample_noise(N)

    encoded_m = encode(M)
    
    ## Compute and return the body
    sum_AS = sum(A[i]*S[i] for i in range(k))

    B = (sum_AS + encoded_m + e) % q
    return (A,B)