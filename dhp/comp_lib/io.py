from __future__ import annotations

from os import PathLike

import pandas as pd


def read_test_file(file: str | PathLike):

    return pd.read_hdf(file)
