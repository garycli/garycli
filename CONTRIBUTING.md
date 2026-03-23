# 🗡️ Contributing Guide
[🇨🇳 中文版](CONTRIBUTING_CN.md)

> Thank you for your interest in contributing to **Gary CLI**!  
> Whether you're fixing a bug, adding chip support, building a Skill pack, or improving documentation — every contribution helps more embedded developers get their hands free.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Quick Start: Local Dev Environment](#quick-start-local-dev-environment)
- [Project Structure](#project-structure)
- [Ways to Contribute](#ways-to-contribute)
  - [🐛 Reporting Bugs](#-reporting-bugs)
  - [💡 Feature Requests](#-feature-requests)
  - [🔧 Submitting Code Fixes or Features](#-submitting-code-fixes-or-features)
  - [🧩 Contributing a Skill Pack](#-contributing-a-skill-pack)
  - [📟 Adding Chip Support](#-adding-chip-support)
  - [📄 Improving Documentation](#-improving-documentation)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Code Style](#code-style)
- [Commit Message Convention](#commit-message-convention)
- [FAQ](#faq)

---

## Code of Conduct

This project is built on an open, friendly, and inclusive community. Please:

- Be respectful of others' contributions, even when you disagree
- Provide clear context in Issues and PRs rather than venting frustration
- Keep discussions focused on the project

---

## Quick Start: Local Dev Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/garycli.git
cd garycli

# 2. Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies in editable mode
pip install -r requirements.txt
pip install -e .

# 4. Install the cross-compiler toolchain (needed to test code gen + compile flow)
# Ubuntu / Debian:
sudo apt install gcc-arm-none-eabi
# macOS:
brew install --cask gcc-arm-embedded

# 5. Download HAL resources
python3 setup.py --hal

# 6. Run diagnostics to confirm everything is ready
python3 stm32_agent.py --doctor
```

---

## Project Structure

```
garycli/
├── stm32_agent.py        # Main program: TUI + AI dialogue + tool orchestration
├── compiler.py           # GCC cross-compilation wrapper
├── config.py             # Config files and path management
├── setup.py              # Installation and initialization script
├── stm32_extra_tools.py  # Built-in tool collection (I2C scan, PWM calc, etc.)
├── gary_skills.py        # Skill system manager
├── requirements.txt      # Python dependencies
├── install.sh            # Linux / macOS install script
├── install.ps1           # Windows install script
└── ~/.gary/              # User data directory (generated at runtime)
    ├── skills/           # Installed Skill packs
    ├── projects/         # Historical project archives
    ├── templates/        # Template library
    └── member.md         # Knowledge / memory base
```

When adding new functionality, place it in the appropriate module rather than piling everything into `stm32_agent.py`.

---

## Ways to Contribute

### 🐛 Reporting Bugs

Open a new Issue on the [Issues](https://github.com/PrettyMyGirlZyy4Embedded/garycli/issues) page. Please include:

- **Gary version** / Python version / OS
- **Chip model** (e.g. STM32F103C8T6)
- **AI backend in use** (e.g. deepseek-chat, gpt-4o)
- **Steps to reproduce** (a minimal reproducible case is ideal)
- **Actual behavior** vs **expected behavior**
- For compile or flash issues, please include the output of `gary doctor`

---

### 💡 Feature Requests

Submit via Issues with the prefix `[Feature]` in the title. Please describe:

- What problem this feature solves (frame it as a use case, not just a technical spec)
- Any initial implementation ideas, pseudocode, or architecture sketches if you have them

---

### 🔧 Submitting Code Fixes or Features

1. **Open an Issue first** for anything non-trivial — this avoids wasted effort
2. Create a branch on your fork:

```bash
git checkout -b fix/i2c-scan-crash
# or
git checkout -b feat/stm32g0-support
```

3. Write your code, making sure:
   - Existing Function Calling behavior across all three AI backends is not broken
   - New tools are registered in `stm32_extra_tools.py` with their corresponding schema
   - Hardware-related code is validated against the `gary doctor` diagnostic checks
4. Submit a PR using the template

---

### 🧩 Contributing a Skill Pack

Skills are Gary's primary extension mechanism — new Skill contributions are especially welcome!

#### Standard Skill Directory Layout

```
my_skill/
├── skill.json         # Skill metadata
├── tools.py           # Python tool functions
├── schemas.json       # OpenAI Function Calling schemas
├── prompt.md          # Prompt instructions for the AI
└── requirements.txt   # Additional Python dependencies (optional)
```

#### skill.json Example

```json
{
  "name": "my_skill",
  "version": "1.0.0",
  "description": "One-line description of what this Skill does",
  "author": "your-github-username",
  "tags": ["motor", "pid", "sensor"],
  "gary_min_version": "0.1.0"
}
```

#### tools.py Example

```python
def my_tool_function(param: str) -> dict:
    """Tool function: describe what it does — the AI reads this docstring."""
    # Your implementation
    return {"success": True, "result": "..."}

# This mapping must be exported
TOOLS_MAP = {
    "my_tool_function": my_tool_function,
}
```

#### schemas.json Example

```json
[
  {
    "type": "function",
    "function": {
      "name": "my_tool_function",
      "description": "Describe when the AI should call this tool",
      "parameters": {
        "type": "object",
        "properties": {
          "param": {
            "type": "string",
            "description": "What this parameter represents"
          }
        },
        "required": ["param"]
      }
    }
  }
]
```

#### prompt.md Example

```markdown
## My Tool
When the user wants to do X, call my_tool_function with the relevant parameters.
```

#### Testing Your Skill Locally

```bash
# Install and hot-reload inside gary interactive mode
/skill install ./my_skill/
/skill reload
/skill list
```

#### PR Requirements for Skill Contributions

- Set the `author` field in `skill.json` to your GitHub username
- In the PR description, explain: what problem the Skill solves, and which chip/peripheral combination you tested with
- If the Skill requires specific hardware, note the prerequisites in `prompt.md`

---

### 📟 Adding Chip Support

Gary currently focuses on the STM32F0 / F1 / F3 / F4 families. To add support for a new series (e.g. STM32G0, STM32H7):

1. Add HAL / CMSIS resource download logic for the new family in `setup.py`
2. Add the corresponding compile flags (MCU flag, linker script, etc.) in `compiler.py`
3. Register the new family in the chip detection logic in `stm32_agent.py`
4. Provide at least one baseline `main.c` template that compiles cleanly
5. In the PR, state which specific chip models and dev boards you actually tested on

---

### 📄 Improving Documentation

Documentation contributions are always welcome, including:

- Fixing errors or outdated information in `README.md` / `README_CN.md`
- Adding FAQ entries (common install issues, chip-specific gotchas)
- Adding new `gary do` usage examples for common scenarios
- Translating documentation into other languages

Documentation PRs do not require a prior Issue — just submit directly.

---

## Pull Request Guidelines

Before submitting a PR, please verify:

- [ ] PR title concisely describes the change
- [ ] PR description covers: **why** the change is needed, **how** it's implemented, **how** you tested it
- [ ] If fixing an Issue, include `Closes #<issue-number>` in the description
- [ ] New functionality passes `gary doctor` diagnostics locally
- [ ] Code passes `flake8` / `black` checks (see below)
- [ ] No unrelated dependencies are introduced

---

## Code Style

This project is Python. Please follow these conventions:

```bash
# Install formatting tools
pip install black flake8

# Format your code
black .

# Lint check
flake8 . --max-line-length=100 --exclude=.venv
```

Key conventions:

- Indentation: 4 spaces
- Max line length: 100 characters
- Prefer double quotes for strings
- All functions and classes should have docstrings — especially tool functions, since the AI reads these to understand what each tool does
- Avoid bare `print()` in the main flow; use `rich` console output consistently

---

## Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

[optional body: explain why and what changed in more detail]

[optional footer: linked Issues or Breaking Change notes]
```

**Types:**

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `skill` | New or updated Skill pack |
| `chip` | New chip family support |
| `refactor` | Code restructuring (no behavior change) |
| `perf` | Performance improvement |
| `ci` | CI/CD configuration changes |

**Examples:**

```
feat(compiler): add STM32G0 series compile flags

Adds support for STM32G030/G031/G071 and similar variants,
including HAL download logic and linker script configuration.

Closes #42
```

```
skill: add uart_protocol_analyzer Skill

Analyzes captured UART traffic and identifies framing patterns
for common sensors including DHT11 and MPU6050.
```

---

## FAQ

**Q: I don't have STM32 hardware — can I still contribute?**  
Yes. Code generation, the compile pipeline, AI backend integration, Skill development, and documentation improvements all work without physical hardware.

**Q: Can a Skill make outbound network requests?**  
Yes, but please clearly state this in both `skill.json`'s `description` field and `prompt.md` so users know the Skill reaches out to the network.

**Q: How long does PR review take?**  
Maintainers aim to respond within 7 days. If you haven't heard back, feel free to leave a comment to ping.

**Q: I want to refactor a core module — what should I keep in mind?**  
Open an Issue first to discuss the approach. Refactors to core modules (especially the AI dispatch loop in `stm32_agent.py`) must preserve consistent behavior across all three flashing modes: SWD, UART ISP, and no-hardware mode.

**Q: What AI backends should I test against?**  
At minimum, test with one Function Calling-capable backend (e.g. deepseek-chat or gpt-4o). If your change touches backend-agnostic logic, a single backend is sufficient; if it touches provider-specific handling, test the affected providers.

---

> **🗡️ Just Gary Do It.**  
> Every line of code, every Skill pack, every documentation fix — it's a gift to the STM32 developer community.

[Back to Home](https://github.com/PrettyMyGirlZyy4Embedded/garycli) · [Open an Issue](https://github.com/PrettyMyGirlZyy4Embedded/garycli/issues) · [Website](https://www.garycli.com)
