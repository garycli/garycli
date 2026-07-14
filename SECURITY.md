# 🔒 Security Policy

[🇨🇳 中文版](SECURITY_CN.md)

---

## Supported Versions

We provide security fixes for the following versions:

| Version | Support Status |
|---------|----------------|
| Latest `main` branch | ✅ Actively maintained |
| Older version tags | ❌ No security patches |

We recommend always running the latest version.

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public Issues.**

If you discover a security issue, please report it privately through one of these channels:

- **GitHub Private Security Advisory** (recommended):  
  Go to [Security → Report a vulnerability](https://github.com/garycli/garycli/security/advisories/new)
- **Email**: Contact the maintainer directly if contact details are listed in the README or `member.md`

Please include as much of the following as possible:

- Type of vulnerability (e.g. code execution, key exposure, privilege escalation)
- Steps to reproduce (a minimal reproducible case is ideal)
- Potential impact and affected scope
- Suggested fix, if you have one

We commit to acknowledging your report within **7 business days** and will work with you to agree on a disclosure timeline after confirming the issue.

---

## Security Considerations for This Project

Gary CLI runs locally on your machine. The following covers the security boundaries you should be aware of when using it.

### 🔑 API Key Management

- Gary stores API Keys in a local config file (typically under `~/.gary/`)
- **Never** commit config files containing API Keys to any version control system
- **Never** paste your API Key into Issues, PRs, or any public discussion
- If you suspect a Key has been exposed, immediately revoke it and regenerate a new one from your AI provider's dashboard
- Consider creating a dedicated API Key for Gary with usage caps (most providers including DeepSeek and OpenAI support per-key spending limits)

### 🧩 Skill Pack Safety

The Skill system allows installing and executing arbitrary Python code — this is what makes it flexible, but it also carries risk:

- **Only install Skills from sources you trust**: the official repository, Skills you wrote yourself, or third-party Skills whose source code you have reviewed
- Before installing, read the Skill's `tools.py` to confirm it does what it claims
- When installing via URL or Git, verify the trustworthiness of the source:

```bash
# Review source code before installing — don't blindly execute
/skill install https://github.com/unknown-user/gary-skill-xxx.git
```

- Gary provides no security guarantees for third-party Skill packs

### ⚙️ System Command Execution

During normal operation, Gary invokes local toolchain binaries (`arm-none-eabi-gcc`, `pyocd`, `stm32loader`, etc.). These calls:

- Run with your current user's permissions — Gary does not request root or admin privileges
- Use AI-generated arguments; in unfamiliar environments, pay attention to terminal output on first use

If you are running Gary in a restricted environment (e.g. a shared server or CI pipeline), ensure that toolchain invocations comply with that environment's security policy.

### 📦 Install Scripts

Gary provides one-liner install scripts via `curl | bash` and `irm | iex`. These patterns require you to trust the script content:

- You can inspect the script before running:
  - Linux / macOS: <https://www.garycli.com/install.sh>
  - Windows: <https://www.garycli.com/install.ps1>
- Alternatively, use the [manual installation](https://github.com/garycli/garycli#manual-installation) method for full control over what gets executed

### 🔌 Hardware Access Permissions

Gary accesses hardware through serial ports (`/dev/ttyUSB*`) and SWD debug probes:

- On Linux, users need to be added to the `dialout` group (`sudo usermod -aG dialout $USER`) — this is the standard permission model for serial port access
- Gary only accesses ports you explicitly configure; it does not scan for or take over other devices
- On shared development machines, be mindful of serial device access control

### 🤖 AI-Generated Code

Gary uses AI to generate STM32 code and then automatically compiles and flashes it. Keep in mind:

- All generated code passes through GCC compilation before flashing — a compile failure will block the flash step
- For production systems or safety-critical applications, manually review generated code before flashing
- Gary is designed for development and debugging workflows; it is not intended for directly generating production firmware

---

## Responsible Disclosure

We follow a responsible disclosure process:

1. You report the vulnerability privately
2. We confirm and fix the issue
3. After the fix is released, we coordinate on disclosure details and attribution
4. You receive public credit (if you wish)

Thank you to everyone who helps keep Gary secure.

---

[Back to Home](https://github.com/garycli/garycli) · [Report a Vulnerability](https://github.com/garycli/garycli/security/advisories/new) · [Website](https://www.garycli.com)
