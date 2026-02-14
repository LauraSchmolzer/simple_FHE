# Simple FHE toy

This repository experiments with Fully Homomorphic Encryption (FHE) based on the paper *Fully Homomorphic Encryption: A Mathematical Introduction* by Sara Logsdon. In FHE, we can compute on encrypted data without decrypting it.  

> "Given encryptions E(m₁), …, E(mₜ), one can compute f(m₁, …, mₜ), without compromising the privacy of the data."  
> [Sara Logsdon, ePrint 2023/1402](https://eprint.iacr.org/2023/1402.pdf)

## Standard Learning with Errors (LWE)

LWE is the original lattice-based problem introduced by Regev in 2005. Here, the secret is a vector $s$, and a small noise $e$ is added to each sample over the integers modulo $q$. Standard LWE arithmetic operates on vectors modulo $q$, which is similar to finite field arithmetic but does not require all elements to be invertible.


## General Learning with Errors (GLWE)

GLWE is a foundational lattice-based security assumption used in modern cryptography. It serves and the mathematical foundation or scheme for encryption. It generalizes LWE and Ring-LWE.
In RLWE the lattice is ring-shaped. This means that the set of polynomials is closed under addition, subtraction, and multiplication — all operations produce another polynomial in the ring.

The secret key is a vector of $k$ random polynomials:  
  $$S = (S_0, \dots, S_{k-1}) \in R^k $$ 
  where each $S_i$ is a polynomial in the ring  
  $$ R := \mathbb{Z}[X]/(X^N + 1) $$  
  with integer coefficients up to degree $N-1$.  

# Encryption Procedure 

To encrypt a message $ M \in R_p $ whith plaintext space $ R_p := (\mathbb{Z}/p\mathbb{Z})/(X^N + 1) $ :
- Let the secret key be a list of *k* random polynomials $ S = (S_0, \dots, S_{k-1}) \in R^k $  from $  R_q := \mathbb{Z}_q[X]/(X^N + 1) $  
- Ciphertext modulus $ q$  and plaintext modulus $ p$ 
- A scaling factor $   \Delta = \floor(q / p) $  

## Encoding message

Scale the emssage into ciphertext space, spreading the message into the larger modulus $ q$  such that small noise won't destroy it :
  $$  \Delta \cdot M \in R_q $$ 

## Sample mask polynomials and small noise

- The mask polynomial is randomly sampled from the rings as \(A_i \sim R_q\)
- The small noise *E*  (for this experimental code randomly sampled from integers between $ [-1,1]$ )

## Compute the body
The body polynomial is computed as:

$$ B = sum_{i=0 to k-1} (A_i \cdot S_i) + \Delta \cdot M + E (\mod q) $$

This body ensures that recovering the secret key becomes a hard lattice problem (CVP) by:
- Mixing the random masks with the secret key
- Embedding the encoded message
- Adding small noise for security

## The ciphertext
The final GLWE ciphertext is :
$$ C = (A_0, ..., A_{k-1},B)$$
Where $(A_0,...,A_{k-1})$ is the mask and $B$ is the body.

