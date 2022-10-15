# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame  # noqa
from datetime import datetime  # noqa
from typing import Optional, Union  # noqa

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class kumo_breakout(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '1d'

    # Can this strategy go short?
    can_short: bool = False

    minimal_roi = {
        "0": 1.0
    }

    stoploss = -0.25
    trailing_stop = False
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 15

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Crypto trading bot strategy indicators

        # Variables
        TS = 9
        KS = 26
        SS = 52
        CS = 26
        OS = 0

        # Ichimoku indicator
        dataframe['tenkan'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ITS_{TS}']
        dataframe['kijun'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'IKS_{KS}']
        dataframe['senkou_a'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ISA_{TS}']
        dataframe['senkou_b'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ISB_{KS}']
        dataframe['chikou'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ICS_{KS}']

        # No LONG entries when price is below Senkou A, Senkou B and Kijun sen
        dataframe['long_signal'] = (dataframe['close'] > dataframe['senkou_a']) & (dataframe['close'] > dataframe['senkou_b']) & (dataframe['close'] > dataframe['kijun'])

        # No SHORT entries when price is above Senkou A, Senkou B and Kijun sen
        dataframe['short_signal'] = (dataframe['close'] < dataframe['senkou_a']) & (dataframe['close'] < dataframe['senkou_b']) & (dataframe['close'] < dataframe['kijun'])

        # Exit indicators
        dataframe['long_exit'] = (dataframe['close'] < dataframe['kijun']) & (dataframe['long_signal'] == True)
        dataframe['short_exit'] = (dataframe['close'] > dataframe['kijun']) & (dataframe['short_signal'] == True)

        # Uncomment this if you use this strategy for real/dummy trading
        # print(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['long_signal'] == True)
            ),
            ['enter_long','enter_tag']] = (1,'kumo_breakout_long')
        dataframe.loc[
            (
                (dataframe['short_signal'] == True)
            ),
            ['enter_short','enter_tag']] = (1,'kumo_breakout_short')

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['long_exit'] == True)
            ),
            ['exit_long','exit_tag']] = (1,'closeprice_below_ks')
        dataframe.loc[
            (
                (dataframe['short_exit'] == True)
            ),
            ['exit_short','exit_tag']] = (1,'closeprice_above_ks')
        return dataframe

