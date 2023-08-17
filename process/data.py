from requests import get as requests_get
from process import WW_DATA_PATH
from os.path import join, exists
from pandas import read_csv as pandas_read_csv
from pandas import DataFrame, to_datetime


def download_ww(workdir: str, force=False) -> DataFrame:

    local_path = join(workdir, "ww.csv")

    if force or (not exists(local_path)):
        response = requests_get(WW_DATA_PATH)

        with open(local_path, "wb") as fid:
            fid.write(response.content)

    ww = pandas_read_csv(local_path)[["week_end_date", "copies_per_day_per_person"]]

    ww['week_end_date'] = to_datetime(ww['week_end_date'])
    ww.set_index('week_end_date', inplace=True)

    return ww