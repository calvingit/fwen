# Security Policy

## Supported Versions

Currently, only the latest version of fwen is supported with security updates.

| Version | Supported          |
|---------|---------------------|
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                 |

## Reporting a Vulnerability

If you discover a security vulnerability in fwen, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please send an email to: calvingit@users.noreply.github.com

Include the following information in your report:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Suggested fix (if known)

### What Happens Next

1. We will acknowledge receipt of your report within 48 hours
2. We will investigate the vulnerability
3. We will provide regular updates on our progress
4. We will release a fix as soon as possible, typically within 7 days
5. We will announce the security fix once it's available

### Security Best Practices

When using fwen:
- Review generated code before deployment
- Keep dependencies updated
- Don't commit sensitive credentials
- Use environment variables for configuration
- Follow Flutter security best practices

## Security Features

fwen includes several security-conscious features:
- Validates project names to prevent path traversal
- Creates projects in isolated directories
- Does not collect or transmit any data
- All code generation happens locally

## Dependency Security

We regularly update dependencies to address security vulnerabilities:
- Automated dependency scanning runs weekly
- Security vulnerabilities are patched in patch releases
- Check [Security](https://github.com/calvingit/fwen/security) for dependency advisories

## Privacy

fwen:
- Does not collect user data
- Does not make network requests
- Does not track usage
- Runs entirely locally on your machine

---

**Repository:** https://github.com/calvingit/fwen

Thank you for helping keep fwen secure! 🔒
