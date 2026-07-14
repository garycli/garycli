# 🔒 安全政策 · Security Policy

[🇬🇧 English](SECURITY.md)

---

## 支持的版本

我们对以下版本提供安全修复支持：

| 版本 | 支持状态 |
|------|----------|
| 最新 `main` 分支 | ✅ 持续维护 |
| 旧版本 tag | ❌ 不再提供安全补丁 |

建议始终使用最新版本。

---

## 报告安全漏洞

**请不要通过公开 Issue 报告安全漏洞。**

如果你发现了安全问题，请通过以下方式私下报告：

- **GitHub 私密安全报告**（推荐）：  
  前往 [Security → Report a vulnerability](https://github.com/garycli/garycli/security/advisories/new)
- **邮件**：如仓库 README 或 member.md 中有维护者联系方式，请直接邮件联系

报告时请尽量包含：

- 漏洞类型（如：代码执行、密钥泄露、权限提升等）
- 复现步骤（最小可复现案例）
- 潜在影响范围
- 如有，提供修复建议

我们承诺在 **7 个工作日内**回复你的报告，并在确认漏洞后协商公开披露时间。

---

## 本项目的安全注意事项

Gary CLI 是一个在本地运行的命令行工具，以下是使用过程中需要了解的安全边界。

### 🔑 API Key 管理

- Gary 将 API Key 存储在本地配置文件中（通常位于 `~/.gary/` 目录）
- **不要**将包含 API Key 的配置文件提交到任何版本控制系统
- **不要**在 Issue、PR 或公开讨论中粘贴你的 API Key
- 如果你怀疑 Key 已泄露，请立即前往对应 AI 服务商的控制台撤销并重新生成
- 建议为 Gary 单独创建一个权限受限的 API Key（如 DeepSeek / OpenAI 平台均支持按用量设置额度上限）

### 🧩 Skill 包安全

Skill 系统允许安装并执行任意 Python 代码，这是其灵活性所在，也带来了相应风险：

- **只安装你信任的 Skill 来源**：官方仓库、你自己编写的 Skill，或经过代码审查的第三方 Skill
- 安装前请阅读 Skill 的 `tools.py` 源码，确认其行为符合预期
- 通过 URL 或 Git 安装 Skill 时，请核实来源的可信度：

```bash
# 安装前先审查源码，不要盲目执行
/skill install https://github.com/unknown-user/gary-skill-xxx.git
```

- Gary 不对第三方 Skill 包的安全性提供任何保证

### ⚙️ 系统命令执行

Gary 在工作过程中会调用本地工具链（`arm-none-eabi-gcc`、`pyocd`、`stm32loader` 等）。这些调用：

- 仅使用当前用户权限执行，不会主动请求 root / 管理员权限
- 调用参数由 AI 生成，建议在不熟悉的环境中首次使用时关注终端输出

如果你在受限环境（如共享服务器、CI 环境）中使用 Gary，请确认工具链调用符合该环境的安全策略。

### 📦 安装脚本

Gary 提供了 `curl | bash` 和 `irm | iex` 形式的一键安装脚本。这类安装方式需要你信任脚本内容：

- 安装前可先查看脚本源码：
  - Linux / macOS: <https://www.garycli.com/install.sh>
  - Windows: <https://www.garycli.com/install.ps1>
- 或选择[手动安装](https://github.com/garycli/garycli#manual-installation)，完全掌控安装过程

### 🔌 硬件访问权限

Gary 通过串口（`/dev/ttyUSB*`）和 SWD 调试器访问硬件：

- Linux 上需要将用户加入 `dialout` 组（`sudo usermod -aG dialout $USER`），这是标准的串口访问权限
- Gary 仅访问用户主动配置的端口，不会扫描或自动接管其他设备
- 在多用户共享的开发机上，请注意串口设备的访问控制

### 🤖 AI 生成内容

Gary 使用 AI 生成 STM32 代码并自动编译、烧录。请注意：

- AI 生成的代码在烧录前会经过 GCC 编译，编译失败会阻止烧录
- 对于生产环境或安全关键系统，请在烧录前人工审查生成的代码
- Gary 定位于开发与调试阶段，不建议将其用于直接生成量产固件

---

## 负责任披露

我们遵循负责任披露（Responsible Disclosure）原则：

1. 你私下报告漏洞
2. 我们确认并修复
3. 在修复发布后，双方协商披露细节和致谢方式
4. 你获得公开致谢（如你愿意）

感谢所有帮助提升 Gary 安全性的贡献者。

---

[返回主页](https://github.com/garycli/garycli) · [提交漏洞报告](https://github.com/garycli/garycli/security/advisories/new) · [官网](https://www.garycli.com)
