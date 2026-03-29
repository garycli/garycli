# Gary Member Memory

## Focus
- 这里只记录高价值、可复用、能提高成功率的经验。
- 自动写入：成功编译、成功运行闭环。
- 主动写入：遇到关键初始化顺序、硬件坑、寄存器判定经验、稳定模板时，调用 `gary_save_member_memory`。
- 经验必须短、具体、可执行，不要粘贴大段原始日志。

## Memories

### [Pinned] 启动标记优先
- UART 初始化后立刻打印 `Gary:BOOT`，再初始化 I2C/SPI/TIM/OLED 等外设。
- 这样即使后续外设卡死，也能先确认程序已启动。

### [Pinned] 裸机 HAL_Delay 依赖 SysTick_Handler
- 裸机代码必须定义 `void SysTick_Handler(void) { HAL_IncTick(); }`。
- 否则 `HAL_Delay()` 会永久阻塞。

### [Pinned] I2C 外设先探测再使用
- 初始化后先 `HAL_I2C_IsDeviceReady()` 检查从设备是否应答。
- 无应答优先怀疑接线或地址，不要盲改业务逻辑。

### [Pinned] 增量修改优先精确替换
- 修改已有工程时优先 `str_replace_edit` + `stm32_recompile`。
- 不要无必要地整文件重写。

### [Pinned] 裸机禁止 sprintf/printf/malloc
- 裸机项目优先手写轻量调试输出，避免 `_sbrk/end` 链接错误。

### [2026-03-28 17:45] 运行成功闭环 | STM32F103ZE | baremetal | UART串口测试
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- 需求: UART串口测试
- bin_size: 3836 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-28 17:49] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4324 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-28 17:51] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4208 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-28 17:52] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4488 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-28 17:55] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4548 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 09:41] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick
- bin_size: 2756 B
- 特征: baremetal, systick
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 09:41] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 3708 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 09:52] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 7488 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 09:52] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 7560 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 09:53] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5544 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 09:55] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5500 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 09:57] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick, oled
- bin_size: 4132 B
- 特征: baremetal, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 10:05] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4680 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:06] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4692 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:10] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4664 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:10] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 3844 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:12] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick, oled
- bin_size: 3696 B
- 特征: baremetal, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 10:15] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick, oled
- bin_size: 3916 B
- 特征: baremetal, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 10:16] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick
- bin_size: 1244 B
- 特征: baremetal, systick
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 10:19] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4940 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:20] 运行成功闭环 | STM32F103ZE | baremetal | OLED显示Hello OLED! SPI接口 PD3(SCL) PG13(SDA) PD6(RES) PG14(...
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: OLED显示Hello OLED! SPI接口 PD3(SCL) PG13(SDA) PD6(RES) PG14(...
- bin_size: 4940 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:30] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5092 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:37] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5128 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 10:47] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick, oled
- bin_size: 3596 B
- 特征: baremetal, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 10:51] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, systick
- bin_size: 2820 B
- 特征: baremetal, systick
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。

### [2026-03-29 11:03] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, oled
- bin_size: 3928 B
- 特征: baremetal, oled
- 当前代码已在本机工具链上成功编译通过。

### [2026-03-29 11:05] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4792 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:05] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4112 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:08] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4884 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:15] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4584 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:15] 运行成功闭环 | STM32F103ZE | baremetal | OLED SPI模式显示 HELLO PD3(SCL) PG13(SDA) PD6(RES) PG14(DC) P...
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: OLED SPI模式显示 HELLO PD3(SCL) PG13(SDA) PD6(RES) PG14(DC) P...
- bin_size: 4584 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:21] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5216 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:21] 运行成功闭环 | STM32F103ZE | baremetal | OLED 双模式测试 SPI+I2C PD3(SCL) PG13(SDA) PD6(RES) PG14(DC) P...
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: OLED 双模式测试 SPI+I2C PD3(SCL) PG13(SDA) PD6(RES) PG14(DC) P...
- bin_size: 5216 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:35] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4560 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:39] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, systick
- bin_size: 3644 B
- 特征: baremetal, uart, debug_print, systick
- 当前代码已在本机工具链上成功编译通过。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 11:42] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4452 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:02] 编译成功模板 | STM32F103ZETB | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4584 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:02] 运行成功闭环 | STM32F103ZETB | baremetal | OLED 显示 HELLO，SPI模式，PD3/PG13/PD6/PG14/PG15
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: OLED 显示 HELLO，SPI模式，PD3/PG13/PD6/PG14/PG15
- bin_size: 4584 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:06] 编译成功模板 | STM32F103ZETB | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4588 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:08] 编译成功模板 | STM32F103ZETB | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4576 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:12] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4304 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:13] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2832 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:14] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2928 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:14] 运行成功闭环 | STM32F103ZE | baremetal | DHT11温湿度传感器测试 PG11引脚
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- 需求: DHT11温湿度传感器测试 PG11引脚
- bin_size: 2928 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:19] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2920 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:19] 运行成功闭环 | STM32F103ZE | baremetal | DHT11温湿度传感器测试 PG11引脚
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- 需求: DHT11温湿度传感器测试 PG11引脚
- bin_size: 2920 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:20] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2924 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:20] 运行成功闭环 | STM32F103ZE | baremetal | DHT11温湿度传感器测试 PG11引脚
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- 需求: DHT11温湿度传感器测试 PG11引脚
- bin_size: 2924 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:21] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2952 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:22] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2980 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:23] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2916 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 12:24] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2876 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:04] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2940 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:05] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2944 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:07] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2996 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:08] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2900 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:09] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2852 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:10] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2736 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:11] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2828 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:12] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2744 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:14] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2808 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:16] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2788 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:17] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2896 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:28] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2988 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:30] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2912 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:31] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 3132 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:32] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 2860 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:37] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- bin_size: 4484 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:37] 运行成功闭环 | STM32F103ZE | baremetal | DHT11温湿度传感器测试 PG11引脚
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick
- 需求: DHT11温湿度传感器测试 PG11引脚
- bin_size: 4484 B
- 特征: baremetal, uart, debug_print, boot_marker, systick
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:41] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5792 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:47] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5860 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 13:58] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5844 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 14:47] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4836 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 14:52] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4868 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 15:49] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 4780 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 15:59] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5420 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 15:59] 运行成功闭环 | STM32F103ZE | baremetal | OLED 8080并口显示爱心图案
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: OLED 8080并口显示爱心图案
- bin_size: 5420 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:11] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5104 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:11] 运行成功闭环 | STM32F103ZE | baremetal
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5104 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:15] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5136 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:33] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5716 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:33] 运行成功闭环 | STM32F103ZE | baremetal
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5716 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:53] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5764 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:56] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5768 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:57] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5876 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 16:58] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5892 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:09] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5824 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:09] 运行成功闭环 | STM32F103ZE | baremetal
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5824 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:10] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5816 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:15] 正点原子DHT11温湿度传感器Skill封装
- importance: high
- source: model
- tags: dht11, skill, atomic, sensor, temperature
- 已创建 `dht11_atomic` Skill，包含：
- 1. `dht11_atomic_get_driver_code(port, pin)` - 获取标准DHT11驱动代码
- 2. `dht11_atomic_get_full_main(port, pin, display)` - 获取完整main.c示例
- 关键修复：延时函数使用 `__IO uint32_t count = us * 8` 保证时序精度。
- 支持任意GPIO配置，返回值：0=成功, 1=无响应, 2=校验失败。

### [2026-03-29 17:19] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5796 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:19] 运行成功闭环 | STM32F103ZE | baremetal | 正点原子OLED 8080并口 + DHT11温湿度传感器显示
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: 正点原子OLED 8080并口 + DHT11温湿度传感器显示
- bin_size: 5796 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:22] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5812 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:29] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 5944 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 17:29] 运行成功闭环 | STM32F103ZE | baremetal | 正点原子OLED 8080并口 + DHT11温湿度显示
- importance: critical
- source: runtime_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- 需求: 正点原子OLED 8080并口 + DHT11温湿度显示
- bin_size: 5944 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 烧录、启动、串口/寄存器验证通过，无 HardFault、无硬件缺失。
- 串口已看到 Gary:BOOT，启动链路正常。
- 运行时已回读关键寄存器: RCC_APB1ENR, RCC_APB2ENR, GPIOA_CRL, GPIOA_CRH, GPIOA_IDR, GPIOA_ODR
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 19:32] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 6172 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 19:38] DS18B20温度传感器Skill封装
- importance: high
- source: model
- tags: ds18b20, skill, atomic, sensor, temperature
- 已创建 `ds18b20_atomic` Skill，包含：
- 1. `ds18b20_atomic_get_driver_code(port, pin)` - 获取DS18B20驱动代码核心片段
- 2. `ds18b20_atomic_get_full_main(port, pin, display)` - 获取完整main.c示例
- 关键特性：
- 支持任意GPIO配置（默认PG11）
- 单总线协议，精度0.1°C
- 返回值：温度×10（如255=25.5°C）
- 转换时间必须≥750ms

### [2026-03-29 19:47] 编译成功模板 | STM32F103C8T6 | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 6588 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 19:52] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 6608 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。

### [2026-03-29 19:53] 编译成功模板 | STM32F103ZE | baremetal
- importance: high
- source: compile_success
- tags: baremetal, uart, debug_print, boot_marker, systick, oled
- bin_size: 6648 B
- 特征: baremetal, uart, debug_print, boot_marker, systick, oled
- 当前代码已在本机工具链上成功编译通过。
- UART 初始化后会尽早打印 Gary:BOOT，启动链路更容易确认。
- 裸机代码显式定义 SysTick_Handler，HAL_Delay 不会卡死。
- 代码保留了轻量串口调试输出，便于运行时定位问题。
