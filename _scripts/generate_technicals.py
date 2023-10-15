import os
import numpy as np
import pandas as pd

#------------------------------------------------------------------------------
# define main function
#------------------------------------------------------------------------------

def main():
    # create directory
    dir_name = "../_data/day/technicals"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # get list of all file names in ../_data/day/bars
    day_bar_files = os.listdir("../_data/day/bars")
    tickers = [x.replace(".csv", "") for x in day_bar_files]

    # calculate technicals for each ticker
    day_bars = {}
    day_technicals = {}
    for ticker in tickers:
        # load day bar data from ../_data/day/bars as a dict of dataframes ( key: ticker, value: dataframe of day bars )
        day_bars[ticker] = pd.read_csv(
            f"../_data/day/bars/{ticker}.csv", index_col=None, parse_dates=True
        )

        day_technicals[ticker] = pd.DataFrame(
            columns=[
                "date",
                "sma_10",
                "sma_20",
                "sma_50",
                "sma_100",
                "sma_200",
                "ema_12",
                "ema_26",
                "rsi_14",
                "macd",
                "macd_signal",
                "macd_hist",
            ]
        )

        print(f"Calculating technicals for {ticker}...")
        # calculate sma
        day_technicals[ticker]["sma_10"] = day_bars[ticker]["close"].rolling(10).mean()
        day_technicals[ticker]["sma_20"] = day_bars[ticker]["close"].rolling(20).mean()
        day_technicals[ticker]["sma_50"] = day_bars[ticker]["close"].rolling(50).mean()
        day_technicals[ticker]["sma_100"] = day_bars[ticker]["close"].rolling(100).mean()
        day_technicals[ticker]["sma_200"] = day_bars[ticker]["close"].rolling(200).mean()

        # calculate ema
        day_technicals[ticker]["ema_12"] = generate_ema_series(day_bars[ticker]["close"], 12)
        day_technicals[ticker]["ema_26"] = generate_ema_series(day_bars[ticker]["close"], 26)

        # calculate rsi
        # delta = day_bars[ticker]["close"].diff()
        # gain = delta.clip(lower=0)
        # loss = -1 * delta.clip(upper=0)
        # ema_gain = gain.ewm(com=13, adjust=False).mean()
        # ema_loss = loss.ewm(com=13, adjust=False).mean()
        # rs = ema_gain / ema_loss
        day_technicals[ticker]["rsi_14"] = generate_rsi_series(day_bars[ticker]["close"]) #100 - (100 / (1 + rs))

        # calculate macd
        day_technicals[ticker]["macd"] = (day_technicals[ticker]["ema_12"] - day_technicals[ticker]["ema_26"])
        day_technicals[ticker]["macd_signal"] = generate_ema_series(day_technicals[ticker]["macd"], 9) #(day_technicals[ticker]["macd"].ewm(span=9, adjust=False).mean())
        day_technicals[ticker]["macd_hist"] = (day_technicals[ticker]["macd"] - day_technicals[ticker]["macd_signal"])

        # add date column
        day_technicals[ticker]["date"] = day_bars[ticker]["date"]

        # save to csv
        # print(f"[ INFO ] Writing bar data to file for: {ticker}")
        with open(f"{dir_name}/{ticker}.csv", "w") as f:
            day_technicals[ticker].to_csv(f, index=False)

#------------------------------------------------------------------------------
# helper functions
#------------------------------------------------------------------------------

def generate_ema_series(data, period):
    ema_values = []
    fvi = data.first_valid_index()
    for i in range(len(data)):
        if i < fvi + period - 1:
            ema_values.append(pd.NA)
        elif i == fvi + period - 1:
            ema_values.append(data[fvi:fvi + period].mean())
        else:
            ema_values.append(calculate_next_ema(data[i], ema_values[i - 1], period, 2))
    return pd.Series(ema_values, index=data.index)

def calculate_next_ema(price, last_ema, period, smoothing):
    multiplier = smoothing / (period + 1)
    return price * multiplier + last_ema * (1 - multiplier)

def running_moving_average(x, period):
    a = np.full_like(x, np.nan)
    a[period] = x[1:period+1].mean()
    for i in range(period+1, len(x)):
        a[i] = (a[i-1] * (period - 1) + x[i]) / period
    return a

def generate_rsi_series(data, period=14):
    change = data.diff()
    gain = change.mask(change < 0, 0.0)
    loss = -change.mask(change > 0, -0.0)

    avg_gain = running_moving_average(gain.to_numpy(), period)
    avg_loss = running_moving_average(loss.to_numpy(), period)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

    # #import numba

    # df['change'] = df['close'].diff()
    # df['gain'] = df.change.mask(df.change < 0, 0.0)
    # df['loss'] = -df.change.mask(df.change > 0, -0.0)

    # #@numba.jit
    # def rma(x, n):
    #     """Running moving average"""
    #     a = np.full_like(x, np.nan)
    #     a[n] = x[1:n+1].mean()
    #     for i in range(n+1, len(x)):
    #         a[i] = (a[i-1] * (n - 1) + x[i]) / n
    #     return a

    # df['avg_gain'] = rma(df.gain.to_numpy(), 14)
    # df['avg_loss'] = rma(df.loss.to_numpy(), 14)

    # df['rs'] = df.avg_gain / df.avg_loss
    # df['rsi'] = 100 - (100 / (1 + df.rs))

    # delta = data.diff()
    # gain = delta.clip(lower=0)
    # loss = -1 * delta.clip(upper=0)
    # avg_gain = gain.rolling(period).mean()
    # avg_loss = loss.rolling(period).mean()

    # rsi_values = []
    # for i in range(len(data)):
    #     if i < period - 1:
    #         rsi_values.append(pd.NA)
    #     elif i == period - 1:
    #         rs = avg_gain[i] / avg_loss[i]
    #         rsi_values.append(100 - (100 / (1 + rs)))
    #     else:
    #         rs = (avg_gain[i-1] * (period-1) + gain[i]) / (avg_loss[i-1] * (period-1) + loss[i])
    #         rsi_values.append(100 - (100 / (1 + rs)))

    # return pd.Series(rsi_values, index=data.index)

#------------------------------------------------------------------------------
# run main function
#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()