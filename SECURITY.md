# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please email [mopati@example.com] with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if you have one)

You should receive a response within 48 hours. If the issue is confirmed, we will:

1. Release a patch as soon as possible
2. Credit you in the CHANGELOG (unless you prefer to remain anonymous)
3. Publish a security advisory

## Security Considerations for HL Programs

### Energy-Based Security

Since HL programs operate on physical principles:

1. **Landauer Bound**: Irreversible operations have energy cost (k_B T ln(2) per bit)
2. **Attack Cost**: Measured in Joules, not CPU cycles
3. **Thermodynamic Audit**: All HL programs can be audited for energy consumption

### Tachyonic Blockchain Security

The tachyonic blockchain (Chapter 10) has specific security properties:

- **Byzantine resistance**: Up to energy budget
- **Attack cost**: Must exceed honest participant work (thermodynamically)
- **Trusted hardware**: Requires SGX or equivalent for energy attestation

If you find vulnerabilities in the consensus mechanism, please report them.

## Responsible Disclosure

We follow coordinated disclosure:

1. You report the vulnerability privately
2. We confirm and develop a fix
3. We release the patch
4. We publicly disclose with credit after users have had time to upgrade

Thank you for helping keep the Universal Hamiltonian Framework secure!
