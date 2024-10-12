import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
import os
import numpy as np
POLYGON_API_KEY = "8qRtL2eVDbBDzynMep3X8rFb6c8dTCgt"

#POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
HEADERS = {
    'Authorization': 'Bearer ' + POLYGON_API_KEY
}
BASE_URL = 'https://api.polygon.io/v2/aggs/'


def get_fx_pairs_data(pg_tickers):
    start = '2023-01-01'
    end = '2023-01-31'
    multiplier = '1'
    timespan = 'hour'
    fx_url = f"range/{multiplier}/{timespan}/{start}/{end}?adjusted=true&sort=asc&limit=50000"
    fx_pairs_dict = {}
    for pair in pg_tickers:
        response = requests.get(
            f"{BASE_URL}ticker/{pair}/{fx_url}", 
            headers=HEADERS
        ).json()
        fx_pairs_dict[pair] = pd.DataFrame(response['results'])
    return fx_pairs_dict


def format_fx_pairs(fx_pair_dict):
    for pair in fx_pairs_dict.keys():
        fx_pairs_dict[pair]['t'] = pd.to_datetime(fx_pairs_dict[pair]['t'],unit='ms')
        fx_pairs_dict[pair] = fx_pairs_dict[pair].set_index('t')
    return fx_pairs_dict


def create_str_index(fx_pairs_dict):
    fx_pairs_str_ind = {}
    for pair in fx_pairs_dict.keys():
        fx_pairs_str_ind[pair] = fx_pairs_dict[pair].set_index(
            fx_pairs_dict[pair].index.to_series().dt.strftime(
                '%Y-%m-%d-%H-%M-%S'
            )
        )
    return fx_pairs_str_ind


def create_returns_series(fx_pairs_str_ind):
    for pair in fx_pairs_str_ind.keys():
        fx_pairs_str_ind[pair]['rets'] = fx_pairs_str_ind[pair]['c'].pct_change()
    return fx_pairs_str_ind 
import pandas as pd

def export_to_excel(formatted_fx_dict, file_name="fx_data.xlsx"):
    """
    Export formatted foreign exchange data to an Excel file.
    Replace invalid Excel characters in sheet names.

    Parameters:
    - formatted_fx_dict (dict): Dictionary containing formatted FX data.
    - file_name (str): Name of the Excel file to be created.
    """
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for pair, df in formatted_fx_dict.items():
            # Replace invalid characters with underscore
            valid_sheet_name = pair.replace(':', '_').replace('/', '_')
            # Limit sheet name to a maximum of 31 characters, which is an Excel limitation
            valid_sheet_name = valid_sheet_name[:31]
            # Write each dataframe to a different worksheet with a valid sheet name
            df.to_excel(writer, sheet_name=valid_sheet_name)

    print(f"Data exported successfully to {file_name}")


pg_tickers = ["C:EURUSD", "C:MXNZAR"]
fx_pairs_dict = get_fx_pairs_data(pg_tickers)
formatted_fx_dict = format_fx_pairs(fx_pairs_dict)
fx_pairs_str_ind = create_str_index(formatted_fx_dict)
fx_returns_dict = create_returns_series(fx_pairs_str_ind) 
#print(pg_tickers)
#print(fx_pairs_str_ind)
#print(fx_returns_dict)
#export_to_excel(fx_returns_dict)

def calculate_risk_metrics(fx_returns_dict):
    risk_metrics = {}
    for pair, df in fx_returns_dict.items():
        if 'rets' in df.columns:
            # Calculating Volatility
            volatility = df['rets'].std()

            # Assuming a risk-free rate (this is a placeholder, update with actual rate)
            risk_free_rate = 0.01
            mean_return = df['rets'].mean()
            excess_return = mean_return - risk_free_rate

            # Ratio de Sharpe
            sharpe_ratio = excess_return / volatility

            # Valor en Riesgo (VaR) - 95% confidence interval
            #var_95 = np.percentile(df['rets'], 5)

            # Drawdown Máximo
            cum_returns = (1 + df['rets']).cumprod()
            peak = cum_returns.expanding(min_periods=1).max()
            drawdown = (cum_returns / peak) - 1
            max_drawdown = drawdown.min()

            risk_metrics[pair] = {
                'Volatility': volatility,
                'Sharpe Ratio': sharpe_ratio,
                'VaR 95%': var_95,
                'Max Drawdown': max_drawdown
            }
    return risk_metrics

risk_metrics = calculate_risk_metrics(fx_returns_dict)
for pair, metrics in risk_metrics.items():
    print(f"{pair} Risk Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
