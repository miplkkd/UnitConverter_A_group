"""D-CFG-01 (P1 / EXT-01): load_config — 깨진 JSON → ConfigError."""


def test_d_cfg_01_corrupt_json_raises_config_error():
    """D-CFG-01: 깨진 파일 → ConfigError."""
    from entity.config import ConfigError, load_config

    # Given
    corrupt_path = "units_corrupt.json"

    # When / Then
    try:
        load_config(corrupt_path)
    except ConfigError:
        pass
    else:
        raise AssertionError("RED: D-CFG-01 — corrupt JSON must raise ConfigError")
