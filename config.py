"""
STM32 Agent 配置文件（云端优先）

说明：
1. server.py + compiler.py 依赖本文件中的服务器/编译配置。
2. 客户端硬件配置已迁移到 client/client_config.py。
3. 下面保留的少量“单机遗留参数”仅用于兼容旧版 stm32_agent.py 参考运行。
"""

import os
from pathlib import Path

# ================= 网络代理 =================
# 默认不强制代理。Google/OpenAI 这类海外接口在当前网络环境下可能需要代理；
# 需要时再填入 URL，或在启动前导出环境变量。
HTTP_PROXY_URL = ""
HTTPS_PROXY_URL = ""
GRPC_PROXY_URL = ""
_LEGACY_DEFAULT_PROXY_URLS = {
    "http://127.0.0.1:7890",
    "http://localhost:7890",
}


def _apply_optional_proxy(env_name: str, configured_value: str) -> None:
    """Only export proxy variables when the user explicitly configured them."""

    value = (configured_value or "").strip()
    if value:
        os.environ[env_name] = value
        return
    current = (os.environ.get(env_name) or "").strip()
    if current in _LEGACY_DEFAULT_PROXY_URLS:
        os.environ.pop(env_name, None)


_apply_optional_proxy("HTTP_PROXY", HTTP_PROXY_URL)
_apply_optional_proxy("HTTPS_PROXY", HTTPS_PROXY_URL or HTTP_PROXY_URL)
_apply_optional_proxy("GRPC_PROXY_EXP", GRPC_PROXY_URL or HTTPS_PROXY_URL or HTTP_PROXY_URL)

AI_TEMPERATURE = 1  # 低温度保证代码稳定性

# ================= 编译工具链 =================
ARM_GCC = "arm-none-eabi-gcc"
ARM_OBJCOPY = "arm-none-eabi-objcopy"
ARM_AR = "arm-none-eabi-ar"
ARM_SIZE = "arm-none-eabi-size"

# ================= 目录结构 =================
BASE_DIR = Path(__file__).parent
WORKSPACE = BASE_DIR / "workspace"
BUILD_DIR = WORKSPACE / "build"
PROJECTS_DIR = WORKSPACE / "projects"
HAL_DIR = WORKSPACE / "hal"
RTOS_DIR = WORKSPACE / "rtos"

# ================= 调试参数 =================
MAX_DEBUG_ATTEMPTS = 5
REGISTER_READ_DELAY = 0.3  # 读寄存器前等待时间（秒）
POST_FLASH_DELAY = 1.5  # 烧录后等待程序启动时间（秒）
UART_READ_TIMEOUT = 3  # 串口读取超时（秒）

# ================= 默认目标芯片 =================
DEFAULT_CHIP = "STM32F103C8T6"
DEFAULT_CLOCK = "HSI_internal"

AI_API_KEY = ""
AI_BASE_URL = ""
AI_MODEL = ""
