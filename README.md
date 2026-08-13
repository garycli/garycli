<div align="center">

# 🗡️ GaryCLI

### AI-native embedded engineering execution

**From a natural-language requirement to code, build, flash, runtime evidence, diagnosis, and repair.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Platforms](https://img.shields.io/badge/Targets-STM32%20%7C%20RP2040%20%7C%20ESP%20%7C%20CanMV_K230-0A7EA4.svg)](#-supported-platforms)
[![Website](https://img.shields.io/badge/Website-garycli.com-111111.svg)](https://www.garycli.com)

**GaryCLI is not just an AI code generator. It is an embedded engineering agent designed to execute as much of the real development loop as the connected toolchain and hardware can verify.**

[Quick Start](#-quick-start) · [Why GaryCLI](#-why-garycli) · [Execution Loop](#-execution-loop) · [Supported Platforms](#-supported-platforms) · [Commands](#-commands) · [Skills](#-skills) · [Contributing](#-contributing)

[中文 README](./README_CN.md)

</div>

---

## ⚡ Why GaryCLI?

AI coding tools are very good at producing source code. Embedded development has a different definition of “done.” A plausible `main.c` is only the beginning.

A real embedded task often looks like this:

```text
Requirement
   ↓
Understand board / chip / pins / peripherals
   ↓
Generate or modify project files
   ↓
Compile with the real toolchain
   ↓
Flash / deploy to the target
   ↓
Observe serial logs / registers / runtime state
   ↓
Diagnose failures
   ↓
Patch → rebuild → reflash → re-check
```

GaryCLI is built around that loop.

Instead of treating the model as a shell script generator, GaryCLI separates responsibilities:

- **The model reasons** about intent, failures, tradeoffs, and next actions.
- **Tools execute deterministic engineering operations** such as compilation, flashing, serial monitoring, register access, project inspection, and deployment.
- **Evidence drives the next step** whenever the connected environment can provide it.

The goal is simple:

> **Move from “AI wrote some embedded code” toward “AI completed a verifiable engineering task.”**

---

## 🔄 Execution loop

A typical hardware-connected workflow is:

```text
Natural-language task
      │
      ▼
Project / code generation
      │
      ▼
Compile ───────────────┐
      │ success        │ failure
      ▼                │
Flash / deploy         └──► Diagnose compiler error ─► Patch
      │
      ▼
Runtime observation
(serial / logs / registers / traceback)
      │
      ├── expected evidence ─► Done
      │
      └── mismatch / failure ─► Diagnose ─► Patch ─► Rebuild
```

### Evidence matters

GaryCLI distinguishes several levels of evidence:

1. **Code-level** — files were generated or modified as intended.
2. **Build-level** — the real compiler/toolchain accepted the project.
3. **Deployment-level** — firmware or files were successfully written to the target.
4. **Runtime-level** — serial output, traceback, register state, or other observable software evidence matches expectations.
5. **Physical-behavior-level** — a real external effect was measured or observed by connected instrumentation.

A successful compile or flash does **not** automatically prove that the physical task is correct. Physical verification requires an observable signal, sensor, probe, test fixture, or explicit user confirmation.

---

## 🎯 What GaryCLI can do

### Natural language → engineering actions

```bash
gary do "PA0 has an LED. Make a 1 kHz PWM breathing-light demo"
gary do "Read MPU6050 acceleration through I2C and print it over UART"
gary --connect --do "Flash the current project and diagnose why there is no serial output"
```

Typical task classes include:

- GPIO, PWM, ADC, EXTI, UART, I2C, SPI, timers
- OLEDs, sensors, buzzers, displays, encoders, motors
- Project generation and incremental modification
- Cross-compilation and build diagnosis
- Firmware flashing / target deployment
- Serial monitoring and runtime-log analysis
- Register-assisted fault analysis on supported STM32 workflows
- MicroPython deployment and traceback repair on supported boards

### Closed-loop repair

GaryCLI can continue after failure instead of stopping at a suggestion:

```text
Build fails
→ read compiler diagnostics
→ locate likely source/configuration issue
→ patch project
→ rebuild

Program boots but device does not respond
→ inspect available runtime evidence
→ check address / init order / pin assumptions / peripheral state
→ patch
→ reflash
→ observe again
```

### Deterministic tool layer

The project includes tools and workflows for tasks such as:

- compiler and project inspection
- SWD / UART ISP deployment for supported STM32 targets
- serial-port discovery and monitoring
- register and fault-state inspection where available
- MicroPython raw-REPL synchronization and runtime-log collection
- I2C scanning and peripheral smoke tests
- pin-conflict checks
- PWM parameter calculation
- Flash / RAM analysis
- PID-related analysis tools
- font / bitmap generation
- extensible Skills

---

## 🚀 Quick Start

GaryCLI requires **Python 3.10+**.

### One-line install

Linux / macOS / WSL:

```bash
curl -fsSL https://www.garycli.com/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://www.garycli.com/install.ps1 | iex
```

### Manual install

```bash
git clone https://github.com/garycli/garycli.git
cd garycli
python3 setup.py --auto
python3 stm32_agent.py --doctor
```

### Configure the AI backend

```bash
gary config
```

GaryCLI supports multiple backend styles, including OpenAI-compatible APIs, Anthropic Messages-style interfaces, Gemini integrations, and local/model-provider configurations supported by the repository.

### Diagnose the local environment

```bash
gary doctor
```

This checks the configured AI endpoint, compiler resources, Python dependencies, serial/debug tooling, and detected hardware where applicable.

---

## 💻 Usage

### One-shot task

```bash
gary do "Write a WS2812 rainbow demo for 8 LEDs"
```

### Run with hardware connected

```bash
gary --connect --do "Blink the LED every 500 ms and verify startup over serial"
```

### Select a chip

```bash
gary --chip STM32F407VET6 --connect --do "Read ADC voltage and print it over UART"
```

### Interactive mode

```bash
gary
gary --connect
gary --chip STM32F103C8T6
```

Then iterate naturally:

```text
Gary > Build an SSD1306 clock on I2C1.
Gary > The display is blank. Diagnose it using the connected hardware evidence.
Gary > Change the I2C address to 0x3D and try again.
Gary > Add an AHT20 and show temperature on the second line.
```

GaryCLI tries to preserve project context and make incremental changes rather than regenerate everything unnecessarily.

---

## 📋 Commands

### Terminal commands

| Command | Purpose |
| --- | --- |
| `gary` | Start interactive mode |
| `gary do "task"` | Run a one-shot task |
| `gary --connect --do "task"` | Run a task with hardware connection enabled |
| `gary --chip <model>` | Select a target chip |
| `gary --connect` | Start with hardware connection enabled |
| `gary config` | Configure the AI backend |
| `gary doctor` | Diagnose the environment |

### Interactive commands

| Command | Purpose |
| --- | --- |
| `/connect [chip]` | Connect a debugger / initialize target context |
| `/disconnect` | Disconnect hardware |
| `/serial [port] [baudrate]` | Connect serial monitoring |
| `/serial list` | List serial ports |
| `/chip [model]` | Show or switch the target chip |
| `/flash [bin]` | Deploy the latest or specified artifact |
| `/probes` | List debug probes |
| `/status` | Show hardware/runtime status |
| `/config` | Reconfigure the AI backend |
| `/projects` | Show project history |
| `/member [path\|reload]` | Inspect or reload project memory |
| `/language [en\|zh]` | Switch CLI language |
| `/skill list` | List installed Skills |
| `/skill install <source>` | Install a Skill |
| `/skill create <name>` | Create a Skill template |
| `/clear` | Clear conversation history |
| `/exit` / `/quit` | Exit |

---

## 📟 Supported platforms

The public repository currently contains these major workflows:

| Platform | Typical targets | Workflow |
| --- | --- | --- |
| **STM32F0 / F1 / F3 / F4** | F030F4, F103C8T6, F303RCT6, F407VET6, F411CEU6 | HAL C generation, GCC build, pyOCD/SWD flashing, UART ISP option, register-assisted debugging |
| **RP2040** | RP2040, Pico, Pico W | MicroPython validation, USB serial/raw REPL sync, boot-log and traceback debugging |
| **ESP32 family** | ESP32, S2, S3, C3, C6 and common boards | MicroPython validation, raw REPL sync, boot-log and traceback debugging |
| **ESP8266 family** | ESP8266, NodeMCU, D1 Mini, ESP-01 | MicroPython validation, raw REPL sync, boot-log and traceback debugging |
| **CanMV K230 family** | CanMV K230, K230D | MicroPython validation, `/sdcard` deployment, file inspection, runtime-log debugging |

Support depth is platform-dependent. A workflow listed here does not imply that every SDK, framework, board revision, debugger, peripheral, or physical verification scenario is supported.

---

## 🔌 STM32 hardware connection

For STM32 closed-loop debugging, the most useful setup is usually **SWD + UART**:

```text
ST-Link / J-Link      STM32
  SWDIO   ─────────── SWDIO
  SWCLK   ─────────── SWCLK
  GND     ─────────── GND
  VTref   ─────────── 3.3V

USB-UART              STM32
  TX      ──────────→ MCU RX
  RX      ←────────── MCU TX
  GND     ─────────── GND
```

- **SWD** provides flashing, target control, register access, and fault analysis.
- **UART** provides runtime logs and application-level evidence.

UART ISP can be used on supported STM32 targets when a debugger is unavailable, but it provides less diagnostic visibility than SWD.

---

## 🧩 Skills

Skills extend GaryCLI with additional deterministic tools and instructions.

```bash
/skill list
/skill install ~/Downloads/skill.zip
/skill install https://github.com/example/gary-skill.git
/skill create motor_driver "Motor control helpers"
/skill reload
/skill export motor_driver
```

A Skill can contain:

```text
skill.json
├── tools.py          # executable tool functions
├── schemas.json      # function schemas
├── prompt.md         # task-specific instructions
└── requirements.txt  # optional dependencies
```

The design principle is the same as the core project: keep physical/engineering operations in explicit tools and let the model decide when and why to use them.

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                         GaryCLI                            │
│                  CLI / interactive TUI                    │
├────────────────────────────────────────────────────────────┤
│                   Agent reasoning layer                    │
│        task planning · diagnosis · tool selection          │
├───────────────────────┬────────────────────────────────────┤
│ Project / build layer │ Hardware / runtime layer           │
│ code · compiler       │ SWD · UART ISP · serial · REPL     │
│ workspace · repair    │ registers · logs · deployment      │
├───────────────────────┴────────────────────────────────────┤
│                         Skills                             │
│      deterministic engineering tools + schemas            │
└────────────────────────────────────────────────────────────┘
```

Repository layout:

```text
garycli/
├── ai/                 # AI provider clients and tool registry
├── compiler/           # build/compiler logic
├── core/               # agent runtime, projects, platform state
├── hardware/           # SWD, serial, ISP, MicroPython transport
├── prompts/            # system/platform prompts
├── tui/                # interactive terminal UI and commands
├── skills/             # bundled Skill sources
├── tests/              # automated tests
├── stm32_agent.py      # CLI entry point
├── gary_skills.py      # Skill manager
├── setup.py            # setup and resource bootstrap
└── config.py           # runtime paths and defaults
```

---

## 🧪 Practical examples

```text
Gary > PA0 is connected to an LED. Make it breathe using PWM.

Gary > Read an AHT20 over I2C1 and print temperature/humidity over UART.

Gary > The firmware flashes successfully but the serial port is silent. Diagnose it.

Gary > Scan the I2C bus and tell me which addresses respond.

Gary > Build a PID motor-speed demo using PWM output and encoder feedback.

Gary > Deploy this MicroPython project to the connected ESP32 and fix any boot traceback.
```

---

## ⚠️ Hardware safety and verification

GaryCLI can execute real commands against connected hardware. Treat generated code and automated actions as engineering output that still requires appropriate review.

Before using it on power electronics, motors, heaters, batteries, actuators, high-current loads, safety-critical equipment, or valuable prototypes:

- set conservative current/voltage/speed limits;
- use independent hardware protection where appropriate;
- verify pin mappings and power domains;
- keep a safe recovery / flashing path;
- do not equate “build succeeded” or “flash succeeded” with physical correctness.

---

## 🗺️ Roadmap

Completed in the public repository:

- [x] STM32F0/F1/F3/F4 base workflow
- [x] SWD flashing and register-assisted debugging
- [x] UART ISP option
- [x] Skill system
- [x] RP2040 / Pico MicroPython workflow
- [x] ESP32 / ESP8266 MicroPython workflow
- [x] CanMV K230 / K230D MicroPython workflow
- [x] Modular AI / compiler / core / hardware / prompt / TUI packages

Directions under continued development:

- [ ] broader native-SDK and chip-family coverage
- [ ] stronger automated hardware validation
- [ ] richer serial / signal visualization
- [ ] improved project import and migration workflows
- [ ] community Skill discovery and distribution
- [ ] IDE / GUI integrations

---

## 🤝 Contributing

Issues and pull requests are welcome. Useful contribution areas include:

- reproducible hardware/toolchain bugs;
- new target and board support;
- deterministic engineering tools and Skills;
- compiler/deployment diagnostics;
- tests and CI improvements;
- documentation, examples, and translations.

Please read [CONTRIBUTING.md](./CONTRIBUTING.md), [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md), and [SECURITY.md](./SECURITY.md) before contributing.

For security-sensitive reports, follow the security policy instead of opening a public issue.

---

## 📜 License

GaryCLI is released under the [Apache-2.0 License](./LICENSE).

---

<div align="center">

**🗡️ Just Gary Do It.**

[Website](https://www.garycli.com) · [Issues](https://github.com/garycli/garycli/issues) · [Contributing](./CONTRIBUTING.md) · [Changelog](./CHANGELOG.md)

</div>
