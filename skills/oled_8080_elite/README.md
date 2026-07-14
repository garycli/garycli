# 正点原子 STM32F103 精英板 OLED 8080 Skill

为正点原子 STM32F103 精英板生成 OLED 8080 并口驱动、位图代码或完整演示程序。

## 安装

在 Gary 交互模式中，从仓库根目录运行：

```text
/skill install ./skills/oled_8080_elite
```

## 工具

- `oled_8080_elite_get_driver_code`：生成 OLED 初始化、文字显示和几何绘图驱动
- `oled_8080_elite_draw_bitmap`：生成预定义或自定义位图绘制代码
- `oled_8080_elite_get_full_main`：生成 `string`、`geometry`、`bitmap` 或 `clear` 完整演示
