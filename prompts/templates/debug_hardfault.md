## HardFault 专项诊断

- 先读取 `SCB_CFSR`、`SCB_HFSR`、`SCB_BFAR`、`PC`，再下结论，禁止凭感觉猜。
- `PRECISERR + BFARVALID`：优先怀疑非法外设访问、外设时钟未开，或 FreeRTOS 场景下的启动/FPU 问题。
- `IACCVIOL`：优先检查函数指针、跳转地址和向量表。
- `UNDEFINSTR`：优先检查 Thumb/ARM 模式、FPU 指令使用条件和编译目标。
- `PC` 落在 `Default_Handler`：优先怀疑中断处理函数缺失。
- FreeRTOS 场景若 `CFSR=0x8200`、`BFAR` 垃圾地址：先检查是否误定义了 `SysTick_Handler`，再检查 BSP / startup 是否为最新。
- 若程序在 `Gary:BOOT` 之前就崩溃，优先怀疑初始化顺序、阻塞式外设初始化、总线锁死。
- 诊断结论必须包含：根因、证据寄存器、最小修复动作。
- 若证据指向硬件未接或总线错误，直接说明不是业务逻辑 bug。
