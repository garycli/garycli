<div align="center">

# 🗡️ GaryCLI

### AI 原生嵌入式工程执行系统

**从自然语言需求出发，推进到代码、编译、烧录、运行证据、诊断与修复。**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Platforms](https://img.shields.io/badge/Targets-STM32%20%7C%20RP2040%20%7C%20ESP%20%7C%20CanMV_K230-0A7EA4.svg)](#-支持的平台)
[![Website](https://img.shields.io/badge/Website-garycli.com-111111.svg)](https://www.garycli.com)

**GaryCLI 不只是一个 AI 代码生成器。它面向真实嵌入式工程流程设计，目标是在工具链和已连接硬件可验证的范围内，尽可能把一次开发任务真正执行完成。**

[快速开始](#-快速开始) · [为什么是 GaryCLI](#-为什么是-garycli) · [执行闭环](#-执行闭环) · [支持的平台](#-支持的平台) · [命令](#-命令) · [Skills](#-skills) · [参与贡献](#-参与贡献)

[English README](./README.md)

</div>

---

## ⚡ 为什么是 GaryCLI？

很多 AI 编程工具擅长生成源代码，但在嵌入式开发里，“写出一份看起来正确的 `main.c`”通常只完成了很小一部分工作。

一次真实任务往往是：

```text
需求
  ↓
理解板卡 / 芯片 / 引脚 / 外设
  ↓
生成或修改工程文件
  ↓
调用真实工具链编译
  ↓
烧录 / 部署到目标硬件
  ↓
观察串口 / 日志 / 寄存器 / 运行状态
  ↓
定位故障
  ↓
修改 → 再编译 → 再烧录 → 再验证
```

GaryCLI 围绕的就是这条链路。

它不把大模型当成一个“会输出 shell 命令的聊天机器人”，而是尽量把职责拆开：

- **模型负责推理**：理解目标、判断错误、分析矛盾、决定下一步动作。
- **工具负责确定性执行**：编译、烧录、串口监控、寄存器读取、工程检查、部署等。
- **真实证据驱动下一轮决策**：只要当前环境能够提供可观察结果，就尽量基于结果继续推进。

目标可以概括为一句话：

> **从“AI 帮你写嵌入式代码”，走向“AI 帮你完成可验证的嵌入式工程任务”。**

---

## 🔄 执行闭环

典型的硬件连接工作流如下：

```text
自然语言任务
    │
    ▼
生成 / 修改工程
    │
    ▼
编译 ───────────────┐
    │ 成功           │ 失败
    ▼                │
烧录 / 部署          └──► 分析编译错误 ─► 修改
    │
    ▼
运行观测
（串口 / 日志 / 寄存器 / Traceback）
    │
    ├── 证据符合预期 ─► 完成
    │
    └── 异常 / 不一致 ─► 分析 ─► 修改 ─► 重建
```

### 不同层级的“成功”并不相同

GaryCLI 更强调证据层级：

1. **代码层**：工程文件已经按要求生成或修改。
2. **构建层**：真实编译器 / 工具链接受了这个工程。
3. **部署层**：固件或文件已经成功写入目标设备。
4. **软件运行层**：串口、日志、寄存器、Traceback 等软件侧证据符合预期。
5. **物理行为层**：外部实际现象被仪器、探针、传感器、测试夹具或用户明确观察到。

因此，**编译成功 ≠ 烧录后物理功能一定正确**。如果任务涉及真实电压、电流、PWM、转速、温度、显示内容、执行器动作等，最终物理验证仍然需要可观察信号、测量工具或用户确认。

---

## 🎯 GaryCLI 能做什么

### 自然语言 → 工程动作

```bash
gary do "PA0 接了 LED，做一个 1kHz PWM 呼吸灯"
gary do "用 I2C 读取 MPU6050 加速度数据，并通过 UART 输出"
gary --connect --do "烧录当前工程，并分析为什么串口没有输出"
```

适合的任务类型包括：

- GPIO、PWM、ADC、EXTI、UART、I2C、SPI、定时器
- OLED、传感器、蜂鸣器、显示器、编码器、电机
- 工程创建与增量修改
- 交叉编译与编译错误诊断
- 固件烧录 / 板端部署
- 串口监控与运行日志分析
- 支持场景下的 STM32 寄存器 / Fault 辅助分析
- 支持板卡上的 MicroPython 部署与 Traceback 修复

### 自动修复闭环

GaryCLI 的重点不是“第一遍一定写对”，而是失败后还能继续：

```text
编译失败
→ 读取编译器错误
→ 定位代码 / 配置问题
→ 修改工程
→ 重新编译

固件启动，但设备无响应
→ 读取当前可用运行证据
→ 检查地址 / 初始化顺序 / 引脚假设 / 外设状态
→ 修改
→ 重新烧录
→ 再次观察
```

### 确定性工具层

仓库中包含或组合了多类工程工具与工作流，例如：

- 编译器与工程检查
- 支持 STM32 目标的 SWD / UART ISP 部署
- 串口发现与串口监控
- 可用场景下的寄存器与 Fault 状态检查
- MicroPython raw REPL 同步与运行日志采集
- I2C 扫描与外设最小验证
- 引脚冲突检查
- PWM 参数计算
- Flash / RAM 分析
- PID 相关分析工具
- 字模 / 位图生成
- 可扩展 Skills

---

## 🚀 快速开始

GaryCLI 需要 **Python 3.10+**。

### 一键安装

Linux / macOS / WSL：

```bash
curl -fsSL https://www.garycli.com/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://www.garycli.com/install.ps1 | iex
```

### 手动安装

```bash
git clone https://github.com/garycli/garycli.git
cd garycli
python3 setup.py --auto
python3 stm32_agent.py --doctor
```

### 配置 AI 后端

```bash
gary config
```

GaryCLI 支持仓库当前实现中的多种后端接入方式，包括 OpenAI-compatible API、Anthropic Messages 风格接口、Gemini 集成，以及本地模型 / 其他兼容服务配置。

### 检查本地环境

```bash
gary doctor
```

该命令会检查已配置的 AI 接口、编译资源、Python 依赖、串口 / 调试工具，以及当前可检测到的硬件环境。

---

## 💻 使用方式

### 单次任务

```bash
gary do "写一个 8 颗 WS2812 的彩虹灯效果"
```

### 连接硬件执行

```bash
gary --connect --do "让 LED 每 500ms 闪烁，并通过串口验证启动"
```

### 指定芯片

```bash
gary --chip STM32F407VET6 --connect --do "读取 ADC 电压并通过 UART 打印"
```

### 交互模式

```bash
gary
gary --connect
gary --chip STM32F103C8T6
```

然后可以持续增量修改：

```text
Gary > 用 I2C1 做一个 SSD1306 时钟。
Gary > 屏幕没有显示，用当前硬件证据排查。
Gary > 把 I2C 地址改成 0x3D，再试一次。
Gary > 再接一个 AHT20，第二行显示温度。
```

GaryCLI 会尽量沿用当前工程上下文，不在每一轮都无意义地整份重写。

---

## 📋 命令

### 终端命令

| 命令 | 用途 |
| --- | --- |
| `gary` | 启动交互模式 |
| `gary do "任务"` | 执行一次性任务 |
| `gary --connect --do "任务"` | 在启用硬件连接的情况下执行任务 |
| `gary --chip <型号>` | 指定目标芯片 |
| `gary --connect` | 启动时启用硬件连接 |
| `gary config` | 配置 AI 后端 |
| `gary doctor` | 检查环境 |

### 交互命令

| 命令 | 用途 |
| --- | --- |
| `/connect [芯片]` | 连接调试器 / 初始化目标硬件上下文 |
| `/disconnect` | 断开硬件 |
| `/serial [端口] [波特率]` | 连接串口监控 |
| `/serial list` | 列出串口 |
| `/chip [型号]` | 查看或切换芯片 |
| `/flash [bin]` | 部署最近产物或指定固件 |
| `/probes` | 列出调试探针 |
| `/status` | 查看硬件 / 运行状态 |
| `/config` | 重新配置 AI 后端 |
| `/projects` | 查看历史项目 |
| `/member [path\|reload]` | 查看或重新加载项目记忆 |
| `/language [en\|zh]` | 切换 CLI 语言 |
| `/skill list` | 查看已安装 Skills |
| `/skill install <来源>` | 安装 Skill |
| `/skill create <名称>` | 创建 Skill 模板 |
| `/clear` | 清空对话历史 |
| `/exit` / `/quit` | 退出 |

---

## 📟 支持的平台

公开仓库当前主要包含以下工作流：

| 平台 | 典型目标 | 当前工作流 |
| --- | --- | --- |
| **STM32F0 / F1 / F3 / F4** | F030F4、F103C8T6、F303RCT6、F407VET6、F411CEU6 | HAL C 生成、GCC 编译、pyOCD/SWD 烧录、UART ISP 可选、寄存器辅助调试 |
| **RP2040** | RP2040、Pico、Pico W | MicroPython 检查、USB 串口/raw REPL 同步、启动日志与 Traceback 调试 |
| **ESP32 系列** | ESP32、S2、S3、C3、C6 及常见开发板 | MicroPython 检查、raw REPL 同步、启动日志与 Traceback 调试 |
| **ESP8266 系列** | ESP8266、NodeMCU、D1 Mini、ESP-01 | MicroPython 检查、raw REPL 同步、启动日志与 Traceback 调试 |
| **CanMV K230 系列** | CanMV K230、K230D | MicroPython 检查、`/sdcard` 部署、文件检查、运行日志调试 |

不同平台的支持深度不同。表格中“支持某平台”不代表该平台的所有 SDK、框架、板卡版本、调试器、外设以及物理验证场景都已覆盖。

---

## 🔌 STM32 硬件连接建议

对于 STM32 闭环调试，通常最有价值的是 **SWD + UART**：

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

- **SWD**：烧录、目标控制、寄存器读取、Fault 分析。
- **UART**：运行日志与应用层证据。

没有调试器时，支持的 STM32 目标也可以使用 UART ISP，但可获得的诊断信息通常少于 SWD。

---

## 🧩 Skills

Skills 用于给 GaryCLI 增加新的确定性工具和领域说明。

```bash
/skill list
/skill install ~/Downloads/skill.zip
/skill install https://github.com/example/gary-skill.git
/skill create motor_driver "电机控制辅助工具"
/skill reload
/skill export motor_driver
```

一个 Skill 可以包含：

```text
skill.json
├── tools.py          # 可执行工具函数
├── schemas.json      # Function schemas
├── prompt.md         # 领域任务说明
└── requirements.txt  # 可选依赖
```

它延续了 GaryCLI 的核心设计思路：把烧录、测量、编译、读取等工程动作封装成明确工具，让模型决定“什么时候调用、为什么调用、下一步做什么”。

---

## 🏗️ 架构

```text
┌────────────────────────────────────────────────────────────┐
│                         GaryCLI                            │
│                     CLI / 交互式 TUI                      │
├────────────────────────────────────────────────────────────┤
│                       Agent 推理层                         │
│              任务规划 · 故障判断 · 工具选择                │
├───────────────────────┬────────────────────────────────────┤
│ 工程 / 构建层          │ 硬件 / 运行层                       │
│ 代码 · 编译器           │ SWD · UART ISP · 串口 · REPL        │
│ workspace · 修复       │ 寄存器 · 日志 · 部署                  │
├───────────────────────┴────────────────────────────────────┤
│                         Skills                             │
│                  确定性工程工具 + schemas                 │
└────────────────────────────────────────────────────────────┘
```

仓库结构：

```text
garycli/
├── ai/                 # AI 服务商客户端与工具注册
├── compiler/           # 编译 / 构建逻辑
├── core/               # Agent、项目、平台状态
├── hardware/           # SWD、串口、ISP、MicroPython 传输
├── prompts/            # 系统 / 平台提示词
├── tui/                # 交互终端与命令
├── skills/             # 内置 Skill 源码
├── tests/              # 自动化测试
├── stm32_agent.py      # CLI 入口
├── gary_skills.py      # Skill 管理器
├── setup.py            # 安装与资源初始化
└── config.py           # 运行路径与默认配置
```

---

## 🧪 实战任务示例

```text
Gary > PA0 接了一个 LED，用 PWM 做呼吸灯。

Gary > I2C1 读取 AHT20，并通过 UART 打印温湿度。

Gary > 固件烧录成功，但串口完全没有输出，帮我定位问题。

Gary > 扫描 I2C 总线，告诉我哪些地址有设备响应。

Gary > 做一个 PWM 输出 + 编码器反馈的 PID 电机速度控制示例。

Gary > 把这个 MicroPython 工程部署到连接的 ESP32，并修复启动 Traceback。
```

---

## ⚠️ 硬件安全与验证边界

GaryCLI 可以对真实连接的硬件执行命令，因此生成代码和自动化操作仍然应该被视为需要工程审核的输出。

如果涉及功率器件、电机、加热器、电池、执行机构、大电流负载、安全相关设备或贵重样机，建议：

- 预先设置保守的电压、电流、转速等限制；
- 使用必要的独立硬件保护；
- 再次确认引脚映射和电源域；
- 保留可靠的恢复 / 重新烧录通道；
- 不要把“编译成功”或“烧录成功”直接等同于“物理功能正确”。

---

## 🗺️ 路线图

公开仓库已经完成：

- [x] STM32F0/F1/F3/F4 基础工作流
- [x] SWD 烧录与寄存器辅助调试
- [x] UART ISP 可选烧录
- [x] Skill 系统
- [x] RP2040 / Pico MicroPython 工作流
- [x] ESP32 / ESP8266 MicroPython 工作流
- [x] CanMV K230 / K230D MicroPython 工作流
- [x] AI / compiler / core / hardware / prompts / TUI 模块化

持续推进方向：

- [ ] 更广的原生 SDK 与芯片系列覆盖
- [ ] 更强的自动硬件验证能力
- [ ] 更丰富的串口 / 信号可视化
- [ ] 更完善的工程导入与迁移工作流
- [ ] 社区 Skill 发现与分发
- [ ] IDE / GUI 集成

---

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request。尤其欢迎：

- 可复现的硬件 / 工具链问题；
- 新芯片、新板卡支持；
- 确定性工程工具与 Skills；
- 编译 / 部署诊断能力；
- 测试与 CI 改进；
- 文档、示例与翻译。

参与前请阅读 [CONTRIBUTING_CN.md](./CONTRIBUTING_CN.md)、[CODE_OF_CONDUCT_CN.md](./CODE_OF_CONDUCT_CN.md) 和 [SECURITY_CN.md](./SECURITY_CN.md)。

安全敏感问题请按照安全策略报告，不要直接公开提交 Issue。

---

## 📜 开源协议

GaryCLI 使用 [Apache-2.0 License](./LICENSE)。

---

<div align="center">

**🗡️ Just Gary Do It.**

[官网](https://www.garycli.com) · [Issues](https://github.com/garycli/garycli/issues) · [贡献指南](./CONTRIBUTING_CN.md) · [更新日志](./CHANGELOG.md)

</div>
