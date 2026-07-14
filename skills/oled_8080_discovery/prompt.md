# 正点原子探索版 OLED 8080 Skill

当用户需要在 STM32F407ZG 正点原子探索版上驱动 8080 并口 OLED，或结合 DS18B20 显示温度时，使用此 Skill。

## 工具选择

- `oled_8080_discovery_get_driver_code`：只生成 OLED 初始化与显示驱动
- `oled_8080_discovery_get_ds18b20_code`：只生成可配置 GPIO 的 DS18B20 驱动
- `oled_8080_discovery_get_full_main`：生成完整 `main.c`，支持 `oled`、`uart` 和 `none` 输出模式

## 默认硬件

- 目标芯片：STM32F407ZG
- OLED：探索版 8080 并口
- DS18B20：PG9（可配置）

生成完整程序时，优先调用 `oled_8080_discovery_get_full_main`；已有工程只缺某个驱动时，调用对应的代码生成工具。
