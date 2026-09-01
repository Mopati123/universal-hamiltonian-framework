# Book of Mopati — Chapter 10: Cryptographic Research Boundaries

> **Classification:** standard_physics, engineering_analogy, research_hypothesis  
> **Evidence:** Standard cryptography and quantum key-distribution results must be distinguished from speculative tachyonic or chaos-based constructions.  
> **Certification scope:** No unbreakable-security claim is permitted without a recognized proof under an explicit threat model.

## 10.1 Security is a property under assumptions

A cryptographic system is evaluated relative to:

- an algorithm;
- a key space;
- attacker capabilities;
- computational or information-theoretic assumptions;
- implementation details;
- protocol composition;
- side channels.

Security is not established by calling a mechanism quantum, chaotic, thermodynamic, or tachyonic.

## 10.2 Chaos is not a cryptographic proof

Chaotic systems can exhibit sensitive dependence on initial conditions.

That property alone does not imply one-wayness, pseudorandomness, collision resistance, semantic security, or resistance to cryptanalysis.

A chaos-derived construction requires ordinary cryptographic analysis.

## 10.3 Quantum cryptography

Some quantum key-distribution protocols have rigorous security results under stated assumptions.

Those results do not transfer automatically to arbitrary algorithms that use quantum terminology or simulated quantum variables.

## 10.4 Time-locking

Time-lock puzzles, delayed disclosure schemes, trusted release mechanisms, and verifiable delay functions can impose temporal conditions using established cryptographic techniques.

A model that depends on a future timestamp does not imply retrocausal information transfer.

## 10.5 Tachyonic cryptography

A proposed tachyonic cryptographic layer is a research_hypothesis unless it is reduced to a precise protocol with:

- deterministic algorithms;
- entropy sources;
- key derivation;
- adversarial model;
- security definition;
- proof or attack analysis;
- reproducible implementation.

There is currently no basis for calling such a construction unbreakable.

## 10.6 XOR composition

Combining multiple bit strings with XOR does not automatically combine their security strengths.

The result depends on independence, entropy, attacker knowledge, key reuse, and protocol details.

Composition requires analysis.

## 10.7 Implementation rule

Cryptographic examples in the Book must either:

- use established libraries and clearly state their guarantees; or
- be labeled pseudocode/research sketches and explicitly state that they are not production cryptography.

## 10.8 Conclusion

The valid UHF boundary is:

> Physical cost, chaos, quantum resources, and temporal constraints may inspire cryptographic research, but security claims must be established using cryptographic definitions, threat models, proofs, and attacks—not analogy.
