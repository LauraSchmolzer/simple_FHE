import numpy as np

# ----------------------------- Parameters -----------------------------
# 0 =< p , q ∈ Z, p =< q , ∆ = q/p, p & q are powers of 2

k = 2                       # number of mask polynomials
N = 4                       # degree of polynomials
q = 128                     # ciphertext modulus
p = 8                       # plaintext modulus
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

# Multiplication of ring polynomial
def multiply_polynomials(poly1, poly2):
    # Standard Polynomial multiplication
    m = len(poly1)
    n = len(poly2)
    # The resulting polynomial has size m+n-1
    prod = [0] * (m+n-1)

    for i in range(m):
        for j in range(n):
            prod[i + j] += poly1[i] * poly2[j]

    # Reduce module X^N + 1
    for i in range(N,len(prod)):
        prod[i-N] -= prod[i] # wrap around with sign flip

    # Truncate to degree < N, get rid of leftover storage
    result = prod[:N]

    # Reduce coefficients mod q
    result = [x % q for x in result]

    return np.array(result) # convert to numpy array for easier handling

# ----------------------------- Encryption Procedure -----------------------------
def encrypt(S,M):
    A = sample_polynomials(k,N,q)
    e = sample_noise(N)

    encoded_m = encode(M)

    sum_AS = np.zeros(N, dtype=int)  # start with zero polynomial

    for i in range(k):
        sum_AS = (sum_AS + multiply_polynomials(A[i], S[i])) % q # compute the sum

    B = (sum_AS + encoded_m + e) % q
    return (A,B)

# ----------------------------- Decryption Procedure -----------------------------

def decrypt(S, C):
    A, B = C
    
    sum_AS = np.zeros(N, dtype=int)  # start with zero polynomial

    for i in range(k):
        sum_AS = (sum_AS + multiply_polynomials(A[i], S[i])) % q # compute the sum
    
    M_tilde = (B - sum_AS) % q
    
    # Divide by delta and round
    M = np.round(M_tilde / delta).astype(int) % p
    
    return M

# ----------------------------- Addition of two messages -----------------------------

def adddition_two_ciphers(C1,C2):
    A1,B1 = C1
    A2,B2 = C2

    B = (B1+B2) % q

    A = [(A1[i] + A2[i]) % q for i in range(k)]

    return (A,B)

# ----------------------------- Simple tests -----------------------------
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

M = np.array([1, 2, 3, 4])  # plaintext polynomial in R_p

C = encrypt(S, M)
M_dec = decrypt(S, C)

print("Original message:", M)
print("Decrypted message:", M_dec)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

M1 = np.array([1, 2, 3, 4])  # plaintext polynomial in R_p
M2 = np.array([4, 3, 2, 1]) 

C1 = encrypt(S, M1)
C2 = encrypt(S, M2)

C = adddition_two_ciphers(C1,C2)
M_dec = decrypt(S,C)

M_check = (M1+M2) % p

print("Original messages:", M1, M2)
print("Decrypted message:", M_dec)
print("Expected message:", M_check)


# %%
