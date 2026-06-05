"""Entity 설정 로드 — JSON 파싱 (P1)."""

import json
from pathlib import Path


class ConfigError(Exception):
    pass


def load_config(path: str) -> dict:
    """D-CFG-01: JSON 파일 로드, 깨진 JSON → ConfigError."""
    try:
        text = Path(path).read_text(encoding="utf-8")
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {path}") from exc