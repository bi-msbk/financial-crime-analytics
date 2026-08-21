from __future__ import annotations

from typing import Final

import numpy as np
import pandas as pd


UK_GEOGRAPHIES: Final[list[tuple[str, str, str, str, str]]] = [
    ("London", "London", "London", "51N", "0W"),
    ("South East", "England", "Brighton", "50N", "0W"),
    ("South West", "England", "Bristol", "51N", "2W"),
    ("East of England", "England", "Cambridge", "52N", "0E"),
    ("West Midlands", "England", "Birmingham", "52N", "1W"),
    ("East Midlands", "England", "Nottingham", "53N", "1W"),
    ("Yorkshire and the Humber", "England", "Leeds", "53N", "1W"),
    ("North West", "England", "Manchester", "53N", "2W"),
    ("North East", "England", "Newcastle", "55N", "1W"),
    ("Wales", "Wales", "Cardiff", "51N", "3W"),
    ("Scotland", "Scotland", "Edinburgh", "56N", "3W"),
    ("Northern Ireland", "Northern Ireland", "Belfast", "54N", "6W"),
]


REQUIRED_COLUMNS: Final[list[str]] = [
    "geography_key",
    "geography_id",
    "country",
    "region",
    "city",
    "latitude_band",
    "longitude_band",
]


def generate_geography(
    count: int = 12,
    seed: int = 20260817,
) -> pd.DataFrame:
    """
    Generate a deterministic synthetic UK geography reference dataset.

    Grain:
        One row per geographic reference entity.

    Parameters
    ----------
    count:
        Number of geography records to generate.
    seed:
        Random seed used for deterministic selection.

    Returns
    -------
    pandas.DataFrame
        Synthetic geography dimension.
    """
    if count <= 0:
        raise ValueError("count must be greater than zero")

    rng = np.random.default_rng(seed)

    base = pd.DataFrame(
        UK_GEOGRAPHIES,
        columns=[
            "region",
            "_country_area",
            "city",
            "latitude_band",
            "longitude_band",
        ],
    )

    if count <= len(base):
        selected = base.iloc[
            rng.choice(len(base), size=count, replace=False)
        ].copy()
    else:
        extra_indices = rng.choice(
            len(base),
            size=count - len(base),
            replace=True,
        )

        extra = base.iloc[extra_indices].copy()
        selected = pd.concat([base, extra], ignore_index=True)

    selected = selected.reset_index(drop=True)

    selected.insert(
        0,
        "geography_key",
        np.arange(1, len(selected) + 1, dtype=np.int64),
    )

    selected.insert(
        1,
        "geography_id",
        [
            f"GEO{i:06d}"
            for i in range(1, len(selected) + 1)
        ],
    )

    selected.insert(
        2,
        "country",
        "United Kingdom",
    )

    selected = selected[
        [
            "geography_key",
            "geography_id",
            "country",
            "region",
            "city",
            "latitude_band",
            "longitude_band",
        ]
    ]

    return selected
