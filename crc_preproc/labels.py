"""Load slide-level labels from CSV."""

from pathlib import Path

import pandas as pd

from .io_utils import slide_key


def build_labels(labels_csv):
    """Build dictionary mapping slide_id -> label from CSV."""
    if not labels_csv or not labels_csv.exists():
        return {}

    L = pd.read_csv(labels_csv)

    name_col = next(
        (c for c in ("filename", "slide_name", "slide", "wsi", "id") if c in L.columns),
        None,
    )
    lab_col = next(
        (
            c
            for c in ("label", "slide_label", "Label", "class", "Class")
            if c in L.columns
        ),
        None,
    )

    if not name_col or not lab_col:
        return {}

    L["_key"] = L[name_col].astype(str).map(slide_key)
    return (
        L.dropna(subset=["_key"])
        .drop_duplicates("_key")
        .set_index("_key")[lab_col]
        .astype("Int64")
        .to_dict()
    )
