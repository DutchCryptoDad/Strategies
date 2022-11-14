# ==============================================================================================
# The Slope is Dope strategy
#
# Made by:
# ______         _         _      _____                      _         ______            _
# |  _  \       | |       | |    /  __ \                    | |        |  _  \          | |
# | | | | _   _ | |_  ___ | |__  | /  \/ _ __  _   _  _ __  | |_  ___  | | | | __ _   __| |
# | | | || | | || __|/ __|| '_ \ | |    | '__|| | | || '_ \ | __|/ _ \ | | | |/ _` | / _` |
# | |/ / | |_| || |_| (__ | | | || \__/\| |   | |_| || |_) || |_| (_) || |/ /| (_| || (_| |
# |___/   \__,_| \__|\___||_| |_| \____/|_|    \__, || .__/  \__|\___/ |___/  \__,_| \__,_|
#                                               __/ || |
#                                              |___/ |_|
# Version : 1.0
# Date    : 2022-10031
# Remarks :
#    As published, explained and tested in my Youtube video:
#    - https://youtu.be/UvS3ixWG2zs
#    -
# ==============================================================================================

# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from scipy.spatial.distance import cosine
import numpy as np

class slope_is_dope2(IStrategy):
    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.6
    }

    stoploss = -0.9

    timeframe = '4h'
    
    # Trailing stoploss
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.28

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=7)
        dataframe['marketMA'] = ta.SMA(dataframe, timeperiod=200)
        dataframe['fastMA'] = ta.SMA(dataframe, timeperiod=21)
        dataframe['slowMA'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['entryMA'] = ta.SMA(dataframe, timeperiod=3)
        # Calculate slope of slowMA
        # See: https://www.wikihow.com/Find-the-Slope-of-a-Line
        dataframe['sy1'] = dataframe['slowMA'].shift(+11)
        dataframe['sy2'] = dataframe['slowMA'].shift(+1)
        sx1 = 1
        sx2 = 11
        dataframe['sy'] = dataframe['sy2'] - dataframe['sy1']
        dataframe['sx'] = sx2 - sx1
        dataframe['slow_slope'] = dataframe['sy']/dataframe['sx']
        dataframe['fy1'] = dataframe['fastMA'].shift(+11)
        dataframe['fy2'] = dataframe['fastMA'].shift(+1)
        fx1 = 1
        fx2 = 11
        dataframe['fy'] = dataframe['fy2'] - dataframe['fy1']
        dataframe['fx'] = fx2 - fx1
        dataframe['fast_slope'] = dataframe['fy']/dataframe['fx']
        # print(dataframe[['date','close', 'slow_slope','fast_slope']].tail(50))

        # ==== Trailing custom stoploss indicator ====
        dataframe['last_lowest'] = dataframe['low'].rolling(10).min().shift(1)

        return dataframe

    plot_config = {
        "main_plot": {
            # Configuration for main plot indicators.
            "fastMA": {"color": "red"},
            "slowMA": {"color": "blue"},
        },
        "subplots": {
            # Additional subplots
            "rsi": {"rsi": {"color": "blue"}},
            "fast_slope": {"fast_slope": {"color": "red"}, "slow_slope": {"color": "blue"}},
        },
    }


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Only enter when market is bullish (this is a choice)
                (
                (dataframe['close'] > dataframe['marketMA']) &
                # Only trade when the fast slope is above 0
                (dataframe['fast_slope'] > 0) &
                # Only trade when the slow slope is above 0
                (dataframe['slow_slope'] > 0) &
                # Only buy when the close price is higher than the 3day average of ten periods ago
                # (dataframe['close'] > dataframe['entryMA'].shift(+11)) &
                # Or only buy when the close price is higher than the close price of 3 days ago (this is a choice)
                (dataframe['close'] > dataframe['close'].shift(+11)) &
                # Only enter trades when the RSI is higher than 55
                (dataframe['rsi'] > 55) &
                # Only trade when the fast MA is above the slow MA
                (dataframe['fastMA'] > dataframe['slowMA'])
                # Or trade when the fase MA crosses above the slow MA (This is a choice...)
                # (qtpylib.crossed_above(dataframe['fastMA'], dataframe['slowMA']))
                )
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (

                # Close or do not trade when fastMA is below slowMA
                (dataframe['fastMA'] < dataframe['slowMA'])
                # Or close position when the close price gets below the last lowest candle price configured
                # (AKA candle based (Trailing) stoploss) 
                | (dataframe['close'] < dataframe['last_lowest'])
                # | (dataframe['close'] < dataframe['fastMA'])
            ),
            'sell'] = 1
        return dataframe

