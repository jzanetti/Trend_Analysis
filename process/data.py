from requests import get as requests_get
from process import WW_DATA_NATIONAL_PATH, WW_DATA_REGION_PATH
from os.path import join, exists
from pandas import read_csv as pandas_read_csv
from pandas import DataFrame, to_datetime, concat
from yaml import safe_load

def read_cfg(cfg_path: str):
    with open(cfg_path, "r") as fid:
        return safe_load(fid)



def read_ww(ww_all: dict, levels: str or list) -> DataFrame:
    return ww_all[ww_all["region"]== levels]
    if isinstance(levels, str):
        if levels == "nation":
            ww_all["nation"]["region"] = "nation"
            return ww_all["nation"]
        else:
            return ww_all["region"][ww_all["region"]["region"] == levels]
    else:
        return ww_all["region"][ww_all["region"]["region"].isin(levels)]


def download_ww(workdir: str, force=False) -> DataFrame:

    data_to_download = {
        "nation": {
            "local": join(workdir, "ww_nation.csv"),
            "remote": WW_DATA_NATIONAL_PATH
        },
        "region": {
            "local": join(workdir, "ww_region.csv"),
            "remote": WW_DATA_REGION_PATH
        }
    }

    for data_type in data_to_download:
        if force or (not exists(data_to_download[data_type]["local"])):
            response = requests_get(data_to_download[data_type]["remote"])

            with open(data_to_download[data_type]["local"], "wb") as fid:
                fid.write(response.content)
        
        if data_type == "nation":

            ww_nation = pandas_read_csv(data_to_download[data_type]["local"])[["week_end_date", "copies_per_day_per_person", "national_pop"]]
            ww_nation['week_end_date'] = to_datetime(ww_nation['week_end_date'])
            ww_nation.set_index('week_end_date', inplace=True)
            ww_nation["data"] = ww_nation["copies_per_day_per_person"] * ww_nation["national_pop"]
            ww_nation = ww_nation.drop(columns=["copies_per_day_per_person", "national_pop"])
            ww_nation["region"] = "nation"
        
        elif data_type == "region":
            ww_region = pandas_read_csv(data_to_download[data_type]["local"])[["week_end_date", "Region", "copies_per_day_per_person", "population_covered"]]
            ww_region['week_end_date'] = to_datetime(ww_region['week_end_date'])
            ww_region.set_index('week_end_date', inplace=True)
            ww_region["data"] = ww_region["copies_per_day_per_person"] * ww_region["population_covered"]
            ww_region.rename(columns={"Region": "region"}, inplace=True)
            ww_region = ww_region.drop(columns=["copies_per_day_per_person", "population_covered"])

    return concat([ww_nation, ww_region], axis=0)
    """
    ww_nation["region"] = ww_nation["region"].astype(str)
    ww_region["region"] = ww_region["region"].astype(str)
    z = ww_nation.merge(ww_region, left_index=True, right_index=True, how='outer', suffixes=('_x', '_y'))
    z['region'] = z['region_y'].fillna(z['region_x'])

    return {"nation": ww_nation, "region": ww_region}
    """