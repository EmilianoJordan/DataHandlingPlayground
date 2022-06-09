from enum import Enum, auto, unique

import pandas as pd


def pandas_reader(file):
    return pd.read_hdf(file)


@unique
class DataIO(Enum):
    PANDAS_HDF = auto()


DATA_READERS = {DataIO.PANDAS_HDF.name: pandas_reader}
