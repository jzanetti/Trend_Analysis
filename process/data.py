from requests import get as requests_get
from process import DATA_PATH
from os.path import join, exists
from pandas import read_csv as pandas_read_csv
from pandas import DataFrame, to_datetime, concat
from yaml import safe_load


def read_cfg(cfg_path: str):
    with open(cfg_path, "r") as fid:
        return safe_load(fid)


def read_ww(ww_all: dict, levels: str or list) -> DataFrame:
    return ww_all[ww_all["region"]== levels]


def get_data_path(workdir: str, data_src: str, data_type: str, data_area: str, force: bool):
    if data_src is None:
        local_data = join(workdir, f"downloaded_data_{data_type}_{data_area}.csv")
        data_to_download = {
            "local": local_data,
            "remote": DATA_PATH.format(data_type=data_type, data_area=data_area)
        }
    else:
        data_to_download = {
            "local": data_src,
            "remote": None
        }

    if data_to_download["remote"] is not None:
        if force or (not exists(data_to_download["local"])):
            response = requests_get(data_to_download["remote"])

            with open(data_to_download["local"], "wb") as fid:
                fid.write(response.content)

    return data_to_download

def download_data(
        workdir: str, 
        start_t: str, 
        end_t: str, 
        force=False, 
        use_covered_pop=False, 
        data_type: str = "ww",
        data_src: dict or list = None,
        data_areas: list = ["national"]) -> DataFrame:
    """Download and read data

    Args:
        workdir (str): Working directory
        data_src (str): If existing local data path
        start_t (str): Start time
        end_t (str): End time
        force (bool, optional): If force redownload. Defaults to False.
        use_covered_pop (bool, optional): Use covered population. Defaults to False.
        data_type (str, optional): data type [ww, cases]. Defaults to "ww".
        data_area (str, optional): data area [national, regional]. Defaults to "national".

    Returns:
        DataFrame: _description_
    """

    if data_src is None:
        data_src = []
        for i in range(len(data_areas)):
            data_src.append(None)
    
    all_data = []
    if data_type == "cases":
        all_data = []
        for i, data_area in enumerate(data_areas):

            data_to_download = get_data_path(workdir, data_src[i], data_type, data_area, force)

            if data_area == "national":
                data = pandas_read_csv(data_to_download["local"])
                data['week_end_date'] = to_datetime(data['week_end_date'])
                data.set_index('week_end_date', inplace=True)
                data["region"] = data_area
            elif data_area == "regional":
                try:
                    data = pandas_read_csv(data_to_download["local"])[["week_end_date", "Region", "case_7d_avg"]]
                except KeyError:
                    data = pandas_read_csv(data_to_download["local"])[["week_end_date", "region", "case_7d_avg"]]
                data['week_end_date'] = to_datetime(data['week_end_date'])
                data.set_index('week_end_date', inplace=True)
                data.rename(columns={"Region": "region"}, inplace=True)
            all_data.append(data)
    
    elif data_type == "ww":
        for i, data_area in enumerate(data_areas):
            data_to_download = get_data_path(workdir, data_src[i], data_type, data_area, force)
            if data_area == "national":
                data = pandas_read_csv(data_to_download["local"])[["week_end_date", "copies_per_day_per_person", "national_pop"]]
                data['week_end_date'] = to_datetime(data['week_end_date'])
                data.set_index('week_end_date', inplace=True)
                if use_covered_pop:
                    data["data"] = data["copies_per_day_per_person"] * data["national_pop"]
                else:
                    data["data"] = data["copies_per_day_per_person"]
                data = data.drop(columns=["copies_per_day_per_person", "national_pop"])
                data["region"] = data_area
        
            elif data_area == "regional":
                try:
                    data = pandas_read_csv(data_to_download["local"])[["week_end_date", "Region", "copies_per_day_per_person", "population_covered"]]
                except KeyError:
                    data = pandas_read_csv(data_to_download["local"])[["week_end_date", "region", "copies_per_day_per_person", "population_covered"]]
                data['week_end_date'] = to_datetime(data['week_end_date'])
                data.set_index('week_end_date', inplace=True)
                if use_covered_pop:
                    data["data"] = data["copies_per_day_per_person"] * data["population_covered"]
                else:
                    data["data"] = data["copies_per_day_per_person"] 
                data.rename(columns={"Region": "region"}, inplace=True)
                data = data.drop(columns=["copies_per_day_per_person", "population_covered"])
            all_data.append(data)

    all_data = concat(all_data, ignore_index=False)
    if start_t is None:
        start_t = "1977-01-01"
    if end_t is None:
        end_t = "2030-01-01"
    filtered_df = all_data[(all_data.index >= start_t) & (all_data.index <= end_t )]

    filtered_df.index.name = None

    return filtered_df
