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
