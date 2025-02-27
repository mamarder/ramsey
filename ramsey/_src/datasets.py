import os
from collections import namedtuple
from dataclasses import dataclass
from typing import ClassVar, List, Tuple
from urllib.parse import urlparse
from urllib.request import urlretrieve

import pandas as pd

dset = namedtuple("dset", ["name", "urls"])


__M4_HOURLY = dset(
    "hourly",
    [
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Train/Hourly-train.csv",  # pylint: disable=line-too-long
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Test/Hourly-test.csv",  # pylint: disable=line-too-long
    ],
)

__M4_DAILY = dset(
    "daily",
    [
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Train/Daily-train.csv",  # pylint: disable=line-too-long
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Test/Daily-test.csv",  # pylint: disable=line-too-long
    ],
)

__M4_WEEKLY = dset(
    "weekly",
    [
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Train/Weekly-train.csv",  # pylint: disable=line-too-long
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Test/Weekly-test.csv",  # pylint: disable=line-too-long
    ],
)

__M4_MONTHLY = dset(
    "monthly",
    [
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Train/Monthly-train.csv",  # pylint: disable=line-too-long
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Test/Monthly-test.csv",  # pylint: disable=line-too-long
    ],
)

__M4_QUARTERLY = dset(
    "quarterly",
    [
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Train/Quarterly-train.csv",  # pylint: disable=line-too-long
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Test/Quarterly-test.csv",  # pylint: disable=line-too-long
    ],
)

__M4_YEARLY = dset(
    "yearly",
    [
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Train/Yearly-train.csv",  # pylint: disable=line-too-long
        "https://github.com/Mcompetitions/M4-methods/raw/master/Dataset/Test/Yearly-test.csv",  # pylint: disable=line-too-long
    ],
)

_M4_DATA_SETS = {
    "hourly": {
        "key": __M4_HOURLY,
        "n_observations": 700,
        "n_forecasts": 48,
        "series_prefix": "H",
    },
    "daily": {
        "key": __M4_DAILY,
        "n_observations": 93,
        "n_forecasts": 14,
        "series_prefix": "D",
    },
    "weekly": {
        "key": __M4_WEEKLY,
        "n_observations": 80,
        "n_forecasts": 13,
        "series_prefix": "W",
    },
    "monthly": {
        "key": __M4_MONTHLY,
        "n_observations": 42,
        "n_forecasts": 18,
        "series_prefix": "M",
    },
    "quarterly": {
        "key": __M4_QUARTERLY,
        "n_observations": 16,
        "n_forecasts": 8,
        "series_prefix": "Q",
    },
    "yearly": {
        "key": __M4_YEARLY,
        "n_observations": 13,
        "n_forecasts": 6,
        "series_prefix": "Y",
    },
}


# pylint: disable=too-few-public-methods
@dataclass
class M4Dataset:
    """A wrapper class to load M4 data"""

    __INTERVALS__: ClassVar[List[str]] = [
        "hourly",
        "daily",
        "weekly",
        "monthly",
        "yearly",
    ]
    data_dir: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".data")
    )

    def load(self, interval: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load an M4 data set

        Parameters
        ----------
        interval: str
            either of "hourly", "daily", "weekly", "monthly", "yearly"

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            a tuple of data frames where the first is the training data and
            the last the testing data used during the M4 competition
        """

        if interval not in self.__INTERVALS__:
            raise ValueError(
                f"'interval' should be one of: '{'/'.join(self.__INTERVALS__)}'"
            )
        os.makedirs(self.data_dir, exist_ok=True)
        dataset = _M4_DATA_SETS[interval]["key"]
        train_csv_path = os.path.join(
            self.data_dir, f"{interval.capitalize()}-train.csv"
        )
        test_csv_path = os.path.join(
            self.data_dir, f"{interval.capitalize()}-test.csv"
        )
        train, test = self._load(dataset, train_csv_path, test_csv_path)
        return train, test

    def _download(self, dataset):
        for url in dataset.urls:
            file = os.path.basename(urlparse(url).path)
            out_path = os.path.join(self.data_dir, file)
            if url.lower().startswith("https"):
                if not os.path.exists(out_path):
                    urlretrieve(url, out_path)
            else:
                raise ValueError(f"{url} does not start with https")

    def _load(
        self, dataset, train_csv_path: str, test_csv_path: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self._download(dataset)
        train_df = pd.read_csv(train_csv_path, sep=",", header=0, index_col=0)
        test_df = pd.read_csv(test_csv_path, sep=",", header=0, index_col=0)
        return train_df, test_df
