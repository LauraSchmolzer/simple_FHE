# 👾 Simple FHE toy

This repository experiments with Fully Homomorphic Encryption (FHE) based on the paper *Fully Homomorphic Encryption: A Mathematical Introduction* by Sara Logsdon. In FHE, we can compute on encrypted data without decrypting it.  

> "Given encryptions E(m₁), …, E(mₜ), one can compute f(m₁, …, mₜ), without compromising the privacy of the data."  
> [Sara Logsdon, ePrint 2023/1402](https://eprint.iacr.org/2023/1402.pdf)

### Standard Learning with Errors (LWE)

LWE is the original lattice-based problem introduced by Regev in 2005. Here, the secret is a vector $s$, and a small noise $e$ is added to each sample over the integers modulo $q$. Standard LWE arithmetic operates on vectors modulo $q$, which is similar to finite field arithmetic but does not require all elements to be invertible.


### General Learning with Errors (GLWE)

GLWE is a foundational lattice-based security assumption used in modern cryptography. It serves and the mathematical foundation or scheme for encryption. It generalizes LWE and Ring-LWE.
In RLWE the lattice is ring-shaped. This means that the set of polynomials is closed under addition, subtraction, and multiplication — all operations produce another polynomial in the ring.

The secret key is a vector of $k$ random polynomials:  
  $$S = (S_0, \dots, S_{k-1}) \in R^k$$ 
  where each $S_i$ is a polynomial in the ring  
  $$R := \mathbb{Z}[X]/(X^N + 1)$$  
  with integer coefficients up to degree $N-1$.  

### Multiplication on Polynomial rings
As we multiply in the ring $R_q := (\mathbb{Z}/q\mathbb{Z})[X]/(X^N + 1)$, meaning all coefficients are reduced to mod q, numbers 'wrap around'. 

Another crucial part is that $(X^N+q)$ identifies $X^N=-1$. This means that powers beyond degree $N-1$ wraps around with a sign flip. This makes the ring closed under addition and multiplication, as well as giving it a fixed size (degree $<N$).


## 🔐 Encryption Procedure 

To encrypt a message $M \in R_p$ whith plaintext space $R_p := (\mathbb{Z}/p\mathbb{Z})/(X^N + 1)$ :
- Let the secret key be a list of *k* random polynomials $S = (S_0, \dots, S_{k-1}) \in R^k$ from $R_q := \mathbb{Z}_q[X]/(X^N + 1)$  
- Ciphertext modulus $q$  and plaintext modulus $p$ 
- A scaling factor $\Delta = \lfloor q / p \rfloor$  

### Encoding message

Scale the emssage into ciphertext space, spreading the message into the larger modulus $ q$  such that small noise won't destroy it :
$$\Delta \cdot M \in R_q$$ 

### Sample mask polynomials and small noise

- The mask polynomial is randomly sampled from the rings as $A_i \sim R_q$
- The small noise *E*  (for this experimental code randomly sampled from integers between $[-1,1]$ )

### Compute the body
The body polynomial is computed as:

$$B = \displaystyle\sum\limits_{i=0}^{k-1} (A_i \cdot S_i) + \Delta \cdot M + E (\mod q)$$

This body ensures that recovering the secret key becomes a hard lattice problem (CVP) by:
- Mixing the random masks with the secret key
- Embedding the encoded message
- Adding small noise for security

### The ciphertext
The final GLWE ciphertext is :
$$C = (A_0, ..., A_{k-1},B)$$
where $(A_0,...,A_{k-1})$ is the mask and $B$ is the body.

## 🔓 Decryption Procedure 
To decrypt the ciphertext $$C = (A_0, ..., A_{k-1},B)$$ :
- The secret key $S = (S_0, \dots, S_{k-1}) \in R^k$ is needed.

We ahve to compute $$ B - \displaystyle\sum\limits_{i=0}^{k-1} (A_i \cdot S_i) = \Delta \cdot M + E (\mod q)$$ where if $E$ is small enough in $\Delta \cdot M + E (\mod q)$$, diving by $\Delta$ and rounding recovers $M$.

However, when preforming an operation on encrypted data in FHE, the 'noise' inside the ciphertext grows. When the noise grows too large, it may overlap with the actual data. This may lead to a false decryption. Therefor, bootstrapping is needed.


## 👾 Addition of two messages
When having two messages encrypted by a GLWE under secret key $S$, we can add these ciphertexts together. The result will be a new GLWE ciphertext encrypting the message $M + M'$ under the secret key $S$, with noise that grew a bit.

$C^{(+)} = C + C' = (A_0+A_0',..., A_{k-1}+A_{k-1}',B+B') \in GLWE_{S, \omega}(\Delta(M+M')) \subset R_q^{k+1}$


## 🔏 What is Bootstrapping?

Bootstrapping is a trick to reset that noise back to a low level by running the decryption circuit through the homomorphic evaluation process. The process is done by the Cloud/Server (who has no decryption keys). It does this by taking the very noisy ciphertext and encrypt the Secret key with istelf, creating an encrypted Secret key. Then, the decryption algorithm is run inside the encrypted domain using this key. 

