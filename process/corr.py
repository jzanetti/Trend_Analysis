from sklearn.preprocessing import StandardScaler
from numpy import gradient as numpy_gradient

from copy import deepcopy

def cal_ww_case_corr(ww_all, case_all, rolling_window: int = 12, if_norm: bool = False, if_gradient: bool = False, area: str = "national"):

    case_all2 = deepcopy(case_all)
    ww_all2 = deepcopy(ww_all)

    case_all2 = case_all2[case_all2["region"] == area]
    ww_all2 = ww_all2[ww_all2["region"] == area]

    scaler = StandardScaler()
    case_all2 = case_all2.sort_index()
    ww_all2 = ww_all2.sort_index()
    
    if if_norm:
        case_all2['case_7d_avg'] = scaler.fit_transform(case_all2[['case_7d_avg']])
        ww_all2['data'] = scaler.fit_transform(ww_all2[['data']])

    if if_gradient:
        case_all2['case_7d_avg'] = numpy_gradient(case_all2['case_7d_avg'])
        ww_all2['data'] = numpy_gradient(ww_all2['data'])

    rolling_corr = case_all2['case_7d_avg'].rolling(window=rolling_window).corr(ww_all2['data'])

    return rolling_corr
