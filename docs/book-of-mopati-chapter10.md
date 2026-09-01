# Book of Mopati — Chapter 10: Cryptographic Research Boundaries

> **Classification:** standard_physics, engineering_analogy, research_hypothesis  
> **Evidence:** Standard cryptography and quantum key-distribution results must be distinguished from speculative tachyonic or chaos-based constructions.  
> **Certification scope:** No security claim is treated as proven without an explicit threat model and recognized security argument.

## 10.1 Security depends on assumptions

A cryptographic system is evaluated relative to:
- algorithm;
- key space;
- attacker capabilities;
- computational or information-theoretic assumptions;
- protocol composition;
- implementation details;
- side channels.

Security is not established by naming a mechanism quantum, chaotic, thermodynamic, or tachyonic.

## 10.2 Chaos is not a cryptographic proof

Sensitive dependence on initial conditions can be illustrated by

$$
\|\delta x(t)\|
\approx
\|\delta x(0)\|
e^{\lambda t},
$$

for a positive Lyapunov exponent $\lambda$ in a regime where the approximation is meaningful.

**Where:**
- $\delta x(0)$ is a small initial perturbation;
- $\delta x(t)$ is the evolved perturbation;
- $\lambda$ measures exponential separation rate.

This may characterize chaotic sensitivity.

It does not prove one-wayness, pseudorandomness, collision resistance, or semantic security.

## 10.3 Quantum cryptography

Some quantum key-distribution protocols have rigorous security results under stated assumptions.

Those results do not transfer automatically to software that merely uses quantum terminology or simulated quantum-like variables.

## 10.4 Time-locking

Time-lock puzzles, delayed-disclosure systems, and verifiable delay functions can impose temporal conditions using established cryptographic techniques.

A future timestamp or delayed release rule does not imply retrocausal information transfer.

## 10.5 Tachyonic cryptography as research hypothesis

A proposed tachyonic cryptographic layer must specify:
- deterministic algorithms;
- entropy sources;
- key derivation;
- adversary model;
- security definition;
- attack analysis or proof;
- reproducible implementation.

Without those, it remains a research sketch.

## 10.6 XOR composition

For bit strings $A$ and $B$ of equal length,

$$
C
=
A
\oplus
B.
$$

The security of $C$ depends on the entropy, independence, secrecy, and reuse properties of $A$ and $B$.

XOR itself does not automatically combine security guarantees.

## 10.7 Implementation rule

Cryptographic examples in the Book must either:
- use established libraries and state their guarantees; or
- be clearly labeled pseudocode or research sketches.

## 10.8 Conclusion

> Physical cost, chaos, quantum resources, and temporal constraints may inspire cryptographic research, but security claims must be established with cryptographic definitions, threat models, proofs, and attacks.
