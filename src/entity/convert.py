"""Entity 변환 — RED stub. GREEN에서 meter 경유·SSOT 비율 구현."""


def to_meter(value: float, unit: str) -> float:
    return 0.0


def convert_all(value: float, unit: str) -> dict[str, float]:
    # RED stub — GREEN에서 meter 경유 일관 구현
    if unit == "feet":
        return {"meter": 0.0, "feet": value, "yard": 0.5}
    return {"meter": value, "feet": 0.0, "yard": -1.0}
