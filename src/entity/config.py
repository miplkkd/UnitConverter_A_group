"""Entity 설정 로드 — JSON 파싱 (P1)."""

import json
from pathlib import Path

from entity.constants import DEFAULT_UNIT_RATIOS

class ConfigError(Exception):
    pass


_active_units: dict[str, float] | None = None


def load_config(path: str) -> dict:
    """D-CFG-01: JSON 파일 로드, 깨진 JSON → ConfigError."""
    try:
        text = Path(path).read_text(encoding="utf-8")
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {path}") from exc


def load_units_config(path: str) -> dict[str, float]:
    """D-CFG-02: flat units.json → meter 기준 배율 dict."""
    data = load_config(path)
    if not isinstance(data, dict):
        raise ConfigError(f"invalid units config in {path}")
    return {str(name): float(ratio) for name, ratio in data.items()}


def apply_units_config(path: str) -> None:
    """D-CFG-03: units.json 비율을 entity 변환 SSOT에 반영."""
    global _active_units
    _active_units = load_units_config(path)


def get_active_units() -> dict[str, float] | None:
    """적용된 units.json 비율 (없으면 None)."""
    return _active_units


def get_meter_to_unit_ratios() -> dict[str, float]:
    """REFACTOR 1.7: constants 기본값 또는 적용된 config SSOT."""
    active = get_active_units()
    if active:
        return dict(active)
    return dict(DEFAULT_UNIT_RATIOS)