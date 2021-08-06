import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Parameters for stock bot
START_DATE = '2003-01-02'
UPDATE_XLSX = True

OUTPUT_FILENAME = "IWMDaily.xlsx"
# MOVING_AVERAGES = list(range(25, 30))  #DO 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100
# VOLUME_MOVING_AVERAGES = list(range(1, 200))

tickers_list = ['IWM']


def fetch_data():
    if UPDATE_XLSX:
        data = yf.download(tickers_list, START_DATE)
        data.to_excel(OUTPUT_FILENAME)

    return pd.read_excel(OUTPUT_FILENAME)


def algorithm():
    # Downloading data
    original_data = fetch_data()
    data = fetch_data()
    cp_values = []

    # Add SMA columns
    print("Generating SMA Columns...")
    for MOVING_AVERAGE in MOVING_AVERAGES:
        data['SMA_' + str(MOVING_AVERAGE)] = original_data['Adj Close'].rolling(MOVING_AVERAGE).mean()

    # Add SMA columns
    print("Generating SMA VOLUME Columns...")
    for VOLUME_MOVING_AVERAGE in VOLUME_MOVING_AVERAGES:
        data['VSMA_' + str(VOLUME_MOVING_AVERAGE)] = original_data['Volume'].rolling(VOLUME_MOVING_AVERAGE).mean()

    # Editing df
    data.set_index('Date', inplace=True)
    data['SPY∆'] = data.pct_change()['Adj Close'] + 1

    data['OWNED'] = True

    # Generate Data
    for MOVING_AVERAGE in MOVING_AVERAGES:
        print("Testing at SMA = " + str(MOVING_AVERAGE))

        SMA_COL = 'SMA_' + str(MOVING_AVERAGE)

        for VOLUME_MOVING_AVERAGE in VOLUME_MOVING_AVERAGES:
            print("Testing at volume SMA = " + str(VOLUME_MOVING_AVERAGE))

            VOL_SMA_COL = 'SMA_' + str(VOLUME_MOVING_AVERAGE)

            data['MAX'] = 0
            data['MIN'] = 10000000
            data['OWNED'] = True

            for i in range(1, len(data) - 1):  # for each row in the dataframe
                # if not data.iloc[i]['OWNED']:
                if data.iloc[i]['Volume'] < data.iloc[i]['VSMA_' + str(VOLUME_MOVING_AVERAGE)]:
                    data.iloc[i + 1, data.columns.get_loc('OWNED')] = True
                elif ((data.iloc[i]['Adj Close'] < data.iloc[i]['SMA_' + str(MOVING_AVERAGE)]) and (
                        data.iloc[i]['Adj Close'] < data.iloc[i - 1]['Adj Close'])):
                    data.iloc[i + 1, data.columns.get_loc('OWNED')] = True
                else:
                    data.iloc[i + 1, data.columns.get_loc('OWNED')] = False

            data['Final'] = np.where(data['OWNED'], data['SPY∆'], 1)
            data['FinalCP_' + str(VOLUME_MOVING_AVERAGE) + '_' + str(MOVING_AVERAGE)] = data['Final'].cumprod(
                skipna=True)

            cp_values.append([MOVING_AVERAGE, VOLUME_MOVING_AVERAGE,
                              data['FinalCP_' + str(VOLUME_MOVING_AVERAGE) + '_' + str(MOVING_AVERAGE)].iat[-1]])

    data.to_excel('all_values.xlsx')
    print(data)

    print(cp_values)
    # data.plot()
    # plt.show(block=True)


fetch_data()
# Execution of stock bot
# algorithm()
