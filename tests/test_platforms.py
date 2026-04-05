"""Tests for target-platform helpers."""

from __future__ import annotations

from core.platforms import canonical_target_name, detect_target_platform, source_filename_for_target


def test_detect_target_platform_for_rp2040_aliases():
    """Common Pico aliases should route to the RP2040 workflow."""

    for value in ("RP2040", "PICO", "PICO_W", "rpi pico", "rpi_pico_w"):
        assert detect_target_platform(value) == "rp2040"


def test_canonical_target_name_normalizes_rp2040_aliases():
    """RP2040 aliases should collapse to stable stored names."""

    assert canonical_target_name("rpi pico") == "PICO"
    assert canonical_target_name("raspberry-pi-pico-w") == "PICO_W"


def test_source_filename_for_target_matches_platform():
    """STM32 projects use main.c while MicroPython targets use main.py."""

    assert source_filename_for_target("STM32F103C8T6") == "main.c"
    assert source_filename_for_target("PICO_W") == "main.py"
    assert source_filename_for_target("ESP32") == "main.py"


def test_detect_target_platform_for_esp_aliases():
    """Common ESP aliases should route to the ESP MicroPython workflow."""

    for value in (
        "ESP32",
        "ESP32-S3",
        "esp32_c3",
        "ESP8266",
        "nodemcu",
        "wemos d1 mini",
        "NodeMCU-32S",
        "LOLIN32",
        "ESP-01",
    ):
        assert detect_target_platform(value) == "esp"


def test_canonical_target_name_normalizes_esp_aliases():
    """ESP aliases should collapse to stable stored names."""

    assert canonical_target_name("ESP32-S3") == "ESP32S3"
    assert canonical_target_name("nodemcu") == "ESP8266"
    assert canonical_target_name("NodeMCU-32S") == "ESP32"
    assert canonical_target_name("LOLIN32") == "ESP32"
    assert canonical_target_name("ESP-01") == "ESP8266"
