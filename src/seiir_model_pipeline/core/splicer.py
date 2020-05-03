import pandas as pd
import numpy as np

from seiir_model_pipeline.core.versioner import INFECTION_COL_DICT


IFR_TOL = 1e-7


class DissimilarRatioError(Exception):
    raise Exception("The death to infection ratios are not the same.")


class Splicer:
    def __init__(self):
        self.col_loc_id = INFECTION_COL_DICT['COL_LOC_ID']
        self.col_date = INFECTION_COL_DICT['COL_DATE']

        self.col_cases = INFECTION_COL_DICT['COL_CASES']
        self.col_deaths = INFECTION_COL_DICT['COL_DEATHS']

        self.col_id_lag = INFECTION_COL_DICT['COL_ID_LAG']
        self.col_obs_deaths = INFECTION_COL_DICT['COL_OBS_DEATHS']
        self.col_obs_cases = INFECTION_COL_DICT['COL_OBS_CASES']

    def splice_draw(self, infection_data, component_fit, component_forecasts):

        # Extract data
        infections = infection_data[self.col_obs_cases]
        deaths = infection_data[self.col_obs_deaths]

        dates = infection_data[self.col_date]

        i_obs = infection_data[self.col_obs_cases].astype(bool)
        d_obs = infection_data[self.col_obs_deaths].astype(bool)

        # Get the lag
        lag = infection_data[self.col_id_lag]
        lag = lag.unique()
        assert len(lag == 1)
        lag = lag[0]

        # Get the IFRs
        ratios = (deaths / infections.shift(lag))

        # Quality control check
        differences = ratios - ratios[np.isfinite(ratios)].mean()
        if not (differences[~differences.isnull()] < IFR_TOL).all():
            raise DissimilarRatioError

        ratio = ratios.mean()

        # Observed infections
        obs_infect = infections[i_obs]
        obs_infect_date = dates[i_obs]

        predict_infect_date = dates[~i_obs]



        return pd.DataFrame()
