# Changelog

本文件记录 Gary CLI 的所有重要变更，格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

All notable changes to Gary CLI are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- CanMV K230 / K230D MicroPython workflow
- RP2040 / Pico and ESP32 / ESP8266 MicroPython workflows
- Modular `ai/`, `compiler/`, `core/`, `hardware/`, `prompts/`, and `tui/` packages

### Changed

- Expanded provider support to OpenAI-compatible, Anthropic Messages, and Gemini SDK interfaces
- Reworked project caching and incremental repair around `workspace/projects/latest_workspace`

---

## [0.2.0] - 2026-03-23

### Added

- `CONTRIBUTING.md` / `CONTRIBUTING_CN.md` — 贡献指南（中英双语）
- `SECURITY.md` / `SECURITY_CN.md` — 安全政策（中英双语）
- `CODE_OF_CONDUCT.md` / `CODE_OF_CONDUCT_CN.md` — 行为准则（中英双语）
- `CHANGELOG.md` — 变更日志
- GitHub Actions CI：lint / test / release 自动化工作流
- GitHub Issue 模板：Bug report / Feature request / Skill submission
- GitHub PR 模板
- 基础测试骨架 `tests/`

---

## [0.1.0-alpha] - 2026-03-19

### Added

- 🗣️ 自然语言 → 可编译 STM32 HAL 代码生成
- 🔄 自动闭环调试（生成 → 编译 → 烧录 → 串口验证 → 寄存器读取 → 修复 → 重烧）
- ⚡ SWD（默认）+ UART ISP（可选）双烧录策略
- 🧰 10 个内置工具：PID 自整定、I2C 扫描、引脚冲突检测、PWM 参数计算、舵机标定、信号采集分析、外设冒烟测试、Flash/RAM 分析、功耗估算、字模生成
- 🔌 支持 7 个 AI 后端：DeepSeek、Kimi、OpenAI、Gemini、通义千问、智谱 GLM、Ollama
- 🧩 Skill 插件系统：支持从文件 / ZIP / Git / URL 安装，支持热加载
- 📟 支持芯片：STM32F0 / F1 / F3 / F4 系列
- `gary do` 一次性任务模式 + `gary` 交互对话模式
- `gary doctor` 环境诊断命令
- `gary config` AI 后端配置命令
- Linux / macOS 一键安装脚本 `install.sh`
- Windows PowerShell 安装脚本 `install.ps1`
- 双语文档：`README.md`（英文）+ `README_CN.md`（中文）
- Apache-2.0 开源协议

---

[Unreleased]: https://github.com/garycli/garycli/compare/V0.2.0...HEAD
[0.2.0]: https://github.com/garycli/garycli/compare/v0.1.0-alpha...V0.2.0
[0.1.0-alpha]: https://github.com/garycli/garycli/releases/tag/v0.1.0-alpha
