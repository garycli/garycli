# 正点原子精英板 DS18B20 Skill

为 STM32F1 / F4 项目生成 DS18B20 单总线温度传感器驱动或完整示例程序，默认数据引脚为 PG11。

## 安装

在 Gary 交互模式中，从仓库根目录运行：

```text
/skill install ./skills/ds18b20_atomic
```

## 工具

- `ds18b20_atomic_get_driver_code`：生成可嵌入现有 `main.c` 的驱动代码
- `ds18b20_atomic_get_full_main`：生成完整示例，支持 `oled`、`uart` 和 `none` 输出模式

GPIO 端口和引脚均可通过 `port`、`pin` 参数覆盖。
