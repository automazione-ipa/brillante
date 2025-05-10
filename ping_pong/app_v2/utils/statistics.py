from datetime import datetime
import time
import pandas as pd


def group_by_day(df):
    df['Funding'] = df['Funding'].astype(float)
    df['Funding by day'] = df.groupby(df['Time'].dt.date)['Funding'].transform('sum')
    df['Yield by day'] = df.groupby(df['Time'].dt.date)['Yield'].transform('sum')

    df = df[['Time', 'Symbol', 'Funding by day', 'Yield by day']].drop_duplicates().reset_index(drop=True)

    df['Time'] = df['Time'].dt.date

    df_daily = df.groupby(['Time', 'Symbol', 'Funding by day', 'Yield by day']).sum().reset_index()

    dtf_final = re_order_dtf(df_daily, False)

    dtf_final['Total by day'] = dtf_final['Funding by day'] + dtf_final['Yield by day']

    dtf_final = re_order_dtf(dtf_final, True)

    total = 0.0
    final_list = []
    for index, row in dtf_final.iterrows():
        total = total + float(row['Total by day'])
        row['Total'] = total
        final_list.append(row)

    dtf_enriched_final = pd.DataFrame(final_list)

    return re_order_dtf(dtf_enriched_final, False), total


def get_list_timestamp(timestamp_inizio):
    timestamp_attuale = int(time.time() * 1000)

    settimana_in_millisecondi = 7 * 24 * 60 * 60 * 1000

    timestamp_millisecondi = []

    timestamp = timestamp_inizio
    while timestamp < timestamp_attuale:
        timestamp_millisecondi.append(timestamp)
        timestamp += settimana_in_millisecondi

    return timestamp_millisecondi


def beautify_dataframe(dict_from_bybit: dict, prc_steth: float):
    list_temp = []
    list_temp_2 = []
    for item in dict_from_bybit:

        if isinstance(item['Time'], int):
            time = item['Time'] / 1000
            data_ora = datetime.fromtimestamp(time)
            item['Time'] = data_ora

            feeRate = round(float(item['FeeRate']) * 100, 4)
            item['FeeRate'] = str(feeRate) + " %"

            list_temp.append(item)

    dtf_new = pd.DataFrame(list_temp)

    dtf_ascending = re_order_dtf(dtf_new, True)

    funding_temp = 0.0
    yield_temp = 0.0
    for index, itm in dtf_ascending.iterrows():
        funding_temp = funding_temp + float(itm['Funding'])
        itm['Somma Funding'] = funding_temp

        yield_temp_2 = (prc_steth / 3 * 0.0001082191781) * float(itm['execPrice'])
        fee = yield_temp_2 * 0.001
        itm['Yield'] = yield_temp_2 - fee

        yield_temp = itm['Yield'] + yield_temp

        itm['Somma Yield'] = yield_temp

        list_temp_2.append(itm)
    dtf_enriched = pd.DataFrame(list_temp_2)

    dtf_to_group = re_order_dtf(dtf_enriched, False)

    return dtf_to_group, yield_temp


def re_order_dtf(df, value):
    df['Time'] = pd.to_datetime(df['Time'])
    df_sorted = df.sort_values(by='Time', ascending=value)

    return df_sorted


def calculate_apr(funding_bfx, funding_gmx, leverage):
    """
    Calculate the APR given funding rates and leverage.
    """
    diff = -(funding_bfx - abs(funding_gmx))
    apr = diff * leverage * 365  # Assume funding is daily
    return apr
