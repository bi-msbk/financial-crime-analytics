from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(Exception):
    """Raised when project configuration cannot be loaded or validated."""


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and return its root mapping."""

    if not path.exists():
        raise ConfigurationError(f"Configuration file not found: {path}")

    if not path.is_file():
        raise ConfigurationError(f"Configuration path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Invalid YAML in {path}: {exc}"
        ) from exc

    if data is None:
        raise ConfigurationError(f"Configuration file is empty: {path}")

    if not isinstance(data, dict):
        raise ConfigurationError(
            f"Configuration root must be a mapping: {path}"
        )

    return data


def load_project_config(project_root: Path) -> dict[str, Any]:
    return load_yaml(
        project_root
        / "00_Project_Control"
        / "01_Project_Config"
        / "project_config.yaml"
    )


def load_metric_definitions(project_root: Path) -> dict[str, Any]:
    return load_yaml(
        project_root
        / "00_Project_Control"
        / "01_Project_Config"
        / "metric_definitions.yaml"
    )


def load_validation_rules(project_root: Path) -> dict[str, Any]:
    return load_yaml(
        project_root
        / "00_Project_Control"
        / "02_Validation"
        / "validation_rules.yaml"
    )


def load_all_configurations(project_root: Path) -> dict[str, dict[str, Any]]:
    """Load all authoritative project configuration files."""

    return {
        "project": load_project_config(project_root),
        "metrics": load_metric_definitions(project_root),
        "validation": load_validation_rules(project_root),
    }
