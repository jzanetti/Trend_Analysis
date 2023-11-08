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


def download_ww(workdir: str, data_src: str, start_t, end_t, force=False, use_covered_pop=False) -> DataFrame:

    if data_src is None:
        data_to_download = {
            "nation": {
                "local": join(workdir, "ww_nation.csv"),
                "remote": None
            },
            "region": {
                "local": join(workdir, "ww_region.csv"),
                "remote": WW_DATA_REGION_PATH
            }
        }
    else:
        data_to_download = {
            "nation": {
                "local": data_src.format(type="national"),
                "remote": None
            },
            "region": {
                "local": data_src.format(type="regional"),
                "remote": None
            }
        }

    ww_nation = None
    ww_region = None
    for data_type in data_to_download:

        if data_to_download[data_type]["remote"] is not None:
            if force or (not exists(data_to_download[data_type]["local"])):
                response = requests_get(data_to_download[data_type]["remote"])

                with open(data_to_download[data_type]["local"], "wb") as fid:
                    fid.write(response.content)
        
        if data_type in ["customized_national", "nation"]:

            ww_nation = pandas_read_csv(data_to_download[data_type]["local"])[["week_end_date", "copies_per_day_per_person", "national_pop"]]
            ww_nation['week_end_date'] = to_datetime(ww_nation['week_end_date'])
            ww_nation.set_index('week_end_date', inplace=True)
            if use_covered_pop:
                ww_nation["data"] = ww_nation["copies_per_day_per_person"] * ww_nation["national_pop"]
            else:
                ww_nation["data"] = ww_nation["copies_per_day_per_person"]
            ww_nation = ww_nation.drop(columns=["copies_per_day_per_person", "national_pop"])
            ww_nation["region"] = "nation"
        
        elif data_type == "region":
            try:
                ww_region = pandas_read_csv(data_to_download[data_type]["local"])[["week_end_date", "Region", "copies_per_day_per_person", "population_covered"]]
            except KeyError:
                ww_region = pandas_read_csv(data_to_download[data_type]["local"])[["week_end_date", "region", "copies_per_day_per_person", "population_covered"]]
            ww_region['week_end_date'] = to_datetime(ww_region['week_end_date'])
            ww_region.set_index('week_end_date', inplace=True)
            if use_covered_pop:
                ww_region["data"] = ww_region["copies_per_day_per_person"] * ww_region["population_covered"]
            else:
                ww_region["data"] = ww_region["copies_per_day_per_person"] 
            ww_region.rename(columns={"Region": "region"}, inplace=True)
            ww_region = ww_region.drop(columns=["copies_per_day_per_person", "population_covered"])

    data = []

    if ww_nation is not None:
        data.append(ww_nation)

    if ww_region is not None:
        data.append(ww_region)
    
    data = concat(data, axis=0)
    if start_t is None:
        start_t = "1977-01-01"
    if end_t is None:
        end_t = "2030-01-01"
    filtered_df = data[(data.index >= start_t) & (data.index <= end_t )]
    return filtered_df
