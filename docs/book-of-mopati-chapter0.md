# Book of Mopati — Chapter 0: Mathematical Foundations

> **Classification:** standard_physics, engineering_analogy  
> **Evidence:** Standard analytical mechanics is established physics; cross-domain uses are modeling choices and must be justified separately.  
> **Certification scope:** This chapter states the mathematical conditions under which Hamiltonian language is valid and explains every symbol used in its core equations.

## 0.1 Canonical variables and the Hamiltonian

For a mechanical system, let $q_i$ denote generalized coordinates and let $\dot q_i$ denote their time derivatives. If the system has a regular Lagrangian $L(q,\dot q,t)$, the conjugate momentum is

$$
p_i = \frac{\partial L}{\partial \dot q_i}.
$$

**Where:**
- $q_i$ is the $i$th generalized coordinate;
- $\dot q_i = dq_i/dt$ is its generalized velocity;
- $p_i$ is the momentum conjugate to $q_i$;
- $L$ is the Lagrangian;
- $t$ is time.

When the map from velocities to momenta is locally invertible, the Hamiltonian is obtained by the Legendre transform

$$
H(q,p,t)
=
\sum_i p_i \dot q_i - L(q,\dot q,t).
$$

**Meaning:** $H$ is the generator of canonical Hamiltonian evolution. In many familiar autonomous mechanical systems it equals the total energy, but that identification is model-dependent and should not be assumed universally.

Hamilton's equations are

$$
\dot q_i = \frac{\partial H}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial H}{\partial q_i}.
$$

The first equation tells us how coordinates change; the second tells us how their conjugate momenta change.

## 0.2 Conservation is not minimization

Along a Hamiltonian trajectory,

$$
\frac{dH}{dt}
=
\frac{\partial H}{\partial t}
+
\{H,H\}
=
\frac{\partial H}{\partial t}.
$$

The Poisson bracket of any function with itself is zero:

$$
\{H,H\}=0.
$$

Therefore, if the Hamiltonian has no explicit time dependence,

$$
\frac{\partial H}{\partial t}=0
\quad\Longrightarrow\quad
\frac{dH}{dt}=0.
$$

**Meaning:** an autonomous Hamiltonian system normally conserves $H$. It does not spontaneously move toward the minimum of $H$.

## 0.3 Stationary action

The action of a path $q(t)$ is

$$
S[q]
=
\int_{t_1}^{t_2}
L(q,\dot q,t)\,dt.
$$

Physical trajectories satisfy the stationarity condition

$$
\delta S = 0.
$$

This is more precise than saying that nature always "minimizes" action. A stationary point may be a minimum, maximum, or saddle point depending on the problem.

The corresponding Euler–Lagrange equations are

$$
\frac{d}{dt}
\left(
\frac{\partial L}{\partial \dot q_i}
\right)
-
\frac{\partial L}{\partial q_i}
=
0.
$$

## 0.4 Phase space and symplectic structure

Canonical phase space is coordinatized by $(q_i,p_i)$. Its standard symplectic two-form is

$$
\omega
=
\sum_i dq_i \wedge dp_i.
$$

**Where:** $\wedge$ is the antisymmetric wedge product of differential forms.

Hamiltonian flow preserves this symplectic structure and, by Liouville's theorem, preserves phase-space volume.

This does **not** imply that every data space, market state, software state, or social state is literally a symplectic phase space. That structure must be defined and demonstrated.

## 0.5 Hamiltonian flow, gradient flow, and dissipation

These are different mathematical objects.

### Hamiltonian flow

$$
\dot q_i = \frac{\partial H}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial H}{\partial q_i}.
$$

This describes conservative, symplectic evolution.

### Gradient flow

For a scalar objective $J(x)$,

$$
\dot x = -\nabla J(x).
$$

Then

$$
\frac{dJ}{dt}
=
\nabla J \cdot \dot x
=
-\|\nabla J\|^2
\le 0.
$$

**Meaning:** gradient flow drives the objective $J$ downhill. This is the appropriate mathematical template for minimization.

### Dissipative flow

A damped system contains nonconservative mechanisms such as friction or coupling to an environment. Its mechanical energy may decrease, but the decrease comes from dissipation rather than canonical Hamiltonian flow.

### Engineering soft score

A software or market objective such as $J(x)$ is a designer-defined score unless a genuine physical Hamiltonian structure has separately been established.

## 0.6 Quantum connection

Quantum mechanics uses a Hamiltonian operator $\hat H$ to generate time evolution:

$$
i\hbar
\frac{\partial}{\partial t}
|\psi(t)\rangle
=
\hat H |\psi(t)\rangle.
$$

**Where:**
- $i$ is the imaginary unit;
- $\hbar$ is the reduced Planck constant;
- $|\psi(t)\rangle$ is the quantum state;
- $\hat H$ is the Hamiltonian operator.

Quantum entanglement is a property of a nonseparable quantum state. Classical coupling or statistical correlation is not, by itself, quantum entanglement.

## 0.7 Numerical integration

A symplectic integrator approximately preserves the geometric structure of Hamiltonian dynamics over long integrations.

It does **not** generally guarantee:
- exact numerical energy at every time step;
- stability for arbitrary step sizes;
- correctness for an incorrect physical model.

## 0.8 Foundational invariant

The Book of Mopati does not require Hamiltonian mechanics to be "the true map of reality."

The defensible foundation is:

> Hamiltonian mechanics is a precise formalism for systems that satisfy its mathematical conditions. UHF uses it exactly where those conditions hold, uses Hamiltonian-inspired constructions explicitly as engineering analogies elsewhere, and labels unverified physical extensions as research hypotheses.
