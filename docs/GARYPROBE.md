# GaryProbe · Getting started / 用户上手

[English](#english) · [中文](#中文)

## English

### What GaryProbe is

GaryProbe is a companion instrument for the physical side of the GaryCLI embedded engineering workflow. A compatible host can communicate with it over USB or BLE to request supported target-facing operations and receive status or measurements. The goal is to bring observations from a real board into an engineering decision. Availability depends on the device firmware, host software, target, and wiring.

This guide describes the scope published in this repository. It does not provide a pinout, electrical ratings, a target compatibility list, or a GaryProbe-specific host command. Confirm those details for the particular hardware and software versions before connecting a target.

### Publicly described capabilities

| Path | What it can contribute when supported |
| --- | --- |
| USB / BLE host link | Requests for supported operations, device status, and captured measurements. |
| SWD target access / flashing | Target-side execution and a deployment result under compatible conditions. |
| PWM / digital output | A signal applied to a target circuit; its effect still needs observation. |
| UART observation | Runtime messages from the connected target. |
| ADC voltage / waveform sampling and digital-level observation | Electrical evidence at the connected point during the test. |

These are capability categories, not a promise that every path works with every target or from the public `gary` CLI. The [README platform table](../README.md#-supported-platforms) describes GaryCLI workflows; it is not a GaryProbe compatibility matrix.

### Before connecting a target

1. Identify the exact GaryProbe hardware and firmware, the matching host software, and the operation you intend to use. Check the version-specific pinout, signal direction, input/output limits, and supported target before wiring. If any of these are unknown, pause until they are confirmed.
2. Identify the target's power domain, ground, and the relevant signal pins from the target documentation. With power off, check the wiring for shorts, reversed connections, and conflicting supplies. Connect a common reference ground only as appropriate for the two circuits; do not assume GaryProbe powers the target or that any connector pin tolerates the target voltage.
3. For an output or flash operation, review the intended effect on the board and keep a recovery path. Apply conservative external limits and independent protection for power electronics, batteries, motors, heaters, or other consequential loads.
4. The ST-Link / J-Link wiring example in the [README](../README.md#-stm32-hardware-connection) is for the public CLI workflow. Do not use it as a GaryProbe connector pinout.

### First observation

1. Choose one known, low-risk target signal and a matching, supported observation mode. Establish the USB or BLE host link using the instructions for your device and host versions; confirm the device status before target operations.
2. With power off, wire the designated input and reference to the checked target points. Power the setup within its verified limits, then observe the signal. Do not drive a pin or flash a target as an incidental part of an observation test.
3. Record the target, firmware and host versions, connection, measurement point, test condition, and result. Compare that result with a specific expected signal. If it differs, inspect the setup and repeat before changing code or declaring a fault.

### What the result proves

GaryCLI separates code, build, deployment, runtime, and physical-behavior evidence. A successful flash establishes a deployment result, not correct operation. UART output is runtime evidence. A voltage, digital level, or waveform capture supports a claim about the connected point and conditions during that capture; it does not alone prove that an LED lit, a motor turned, or another unmeasured effect occurred. Use a suitable sensor, fixture, or direct observation for the physical effect you need to verify.

### Current limits

- GaryProbe-to-GaryCLI host integration and repeatable automated physical checks are still in development. The public `gary` commands describe SWD / UART / REPL workflows and should not be read as GaryProbe commands.
- This repository does not specify a GaryProbe connector pinout, electrical limits, versioned host setup, or validated target compatibility matrix. Use the documentation for your particular device and software before operating it.
- Treat generated code and hardware actions as engineering work requiring review. Do not rely on a single reading or an automated decision as a safety control.

For the broader software workflow, return to the [GaryCLI README](../README.md).

## 中文

### GaryProbe 是什么

GaryProbe 是 GaryCLI 嵌入式工程流程中面向真实硬件的配套仪器。在兼容条件下，主机可通过 USB 或 BLE 请求受支持的目标侧操作，并读取状态或测量结果，让板级观测参与下一步工程决策。实际可用范围取决于设备固件、主机软件、目标板和接线。

本文以本仓库公开说明为边界，不提供 GaryProbe 引脚定义、电气额定值、目标芯片兼容清单或专用主机命令。连接目标板前，请核对所用硬件和软件版本对应的资料。

### 目前公开说明的能力

| 路径 | 在受支持条件下可提供什么 |
| --- | --- |
| USB / BLE 主机链路 | 请求受支持的操作，获取设备状态和采样结果。 |
| SWD 目标访问 / 烧录 | 在兼容条件下执行目标操作并取得部署结果。 |
| PWM / 数字信号输出 | 向目标电路施加信号；实际效果仍需观测。 |
| UART 观测 | 获取目标板的运行消息。 |
| ADC 电压 / 波形采样、数字电平观测 | 获取测试期间接线位置的电气证据。 |

这些是能力类别，不表示每种目标板都适用，也不表示公开仓库的 `gary` 命令已经打通每条路径。[README 的平台表](../README_CN.md#-支持的平台)描述的是 GaryCLI 工作流，不是 GaryProbe 兼容清单。

### 连接目标板前

1. 确认 GaryProbe 硬件与固件版本、配套主机软件和计划使用的操作；按对应版本的资料核对引脚定义、信号方向、输入输出限制及目标兼容性。任何一项不明确时，先不要接线。
2. 根据目标板资料找出供电域、地和相关信号脚。断电检查短路、反接及电源冲突；仅在两个电路的设计允许时建立共地参考。不要推断 GaryProbe 会给目标板供电，也不要推断某个接口能承受目标板电压。
3. 准备输出或烧录时，先评估对目标板的影响并保留恢复通道。电机、加热器、电池、功率电路等负载应设置保守的外部限制和独立保护。
4. [README 中的 ST-Link / J-Link 接线示例](../README_CN.md#-stm32-硬件连接建议)属于公开 CLI 工作流，不能当作 GaryProbe 接口引脚图。

### 完成第一次观测

1. 选一个已知、低风险的目标信号，确认所需观测模式在当前版本可用。按设备与主机对应版本的说明建立 USB 或 BLE 连接；进行目标操作前先确认设备状态。
2. 断电后，将指定输入端和参考地接到已核对的测量点。在确认的限制内上电并观察信号。做观测时，不要顺带驱动引脚或烧录目标板。
3. 记录目标板、设备固件与主机版本、接线、测量点、测试条件和结果，并与具体的预期信号比较。如结果不符，先检查接线和条件，再重复测量，避免直接认定代码有错。

### 证据能说明什么

GaryCLI 将证据分为代码、构建、部署、软件运行和物理行为层。烧录成功说明完成了一次部署，不能证明程序运行正确。UART 输出属于运行证据。电压、数字电平或波形采样只能支持该次测试条件下、接线位置的电气结论；它本身不能证明 LED 已亮、电机已转或其他未测的物理效果。需要验证哪种实际效果，就用合适的传感器、测试夹具或直接观察取得证据。

### 目前的边界

- GaryProbe 与 GaryCLI 主机工具的集成、可重复的自动物理检查仍在开发中。公开仓库的 `gary` 命令描述的是 SWD / UART / REPL 工作流，不能直接当作 GaryProbe 命令使用。
- 本仓库未给出 GaryProbe 接口引脚图、电气限制、分版本主机安装步骤或已验证的目标兼容矩阵。操作前应取得与手中设备、软件匹配的资料。
- 生成的代码和硬件操作需要工程审核；单次读数或自动判断不能代替安全保护。

软件侧流程请参阅 [GaryCLI 中文 README](../README_CN.md)。
