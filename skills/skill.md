# Bundled Skills

This directory contains Skill source packages that can be installed from Gary's interactive mode.

| Skill | Target | Purpose |
| --- | --- | --- |
| `dht11_atomic` | STM32F1 / F4 正点原子精英板 | DHT11 driver and complete examples |
| `dht11_discovery` | STM32F407ZG 正点原子探索版 | DHT11 with OLED or UART output |
| `ds18b20_atomic` | STM32F1 / F4 正点原子精英板 | DS18B20 driver and complete examples |
| `oled_8080_discovery` | STM32F407ZG 正点原子探索版 | 8080 OLED and optional DS18B20 display |
| `oled_8080_elite` | STM32F103 正点原子精英板 | 8080 OLED text, geometry, and bitmap demos |

Install a bundled Skill from the repository root:

```text
/skill install ./skills/<skill-name>
```

Each package keeps its metadata in `skill.json`, schemas in `schemas.json`, implementation in `tools.py`, and runtime guidance in `prompt.md`.
