# ==============================================================================================
# Tenkan sen / Kijun sen crossover strategy
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
# Version : 1.0 Final
# Date    : 2022-9-22
# Remarks :
#    As published, explained and tested in my Youtube video's:
#    - https://youtu.be/Tp3z1IFHidU
#    - 
# ==============================================================================================
# --- Used commands for later reference ---
# source .env/bin/activate
# freqtrade --version
# freqtrade new-config
# freqtrade new-strategy --strategy ts-ks-crossover
# freqtrade download-data -c config.json --days 999 -t 1d
# cp /config/workspace/github_repos/notebooks/DCD/Ichimoku-kinko-hyo/ts-ks-crossover.py user_data/strategies/
# freqtrade backtesting -c config.json -s ts_ks_crossover --export signals
# freqtrade backtesting-analysis
# 

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


class ts_ks_crossover(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '1d'

    # Can this strategy go short?
    can_short: bool = False

    minimal_roi = {
        "0": 1.0
    }

    stoploss = -0.10
    trailing_stop = False
    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 5

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
        """
        Add the functions and indicators here.
        """

        # Create the Ichimoku kinko hyo indicators

        # These are the 'old style values' (comment if you want to use crypto style settings)
        TS = 9
        KS = 26
        SS = 52
        CS = 26
        OS = 0

        # These are the 'Crypto style values' (uncomment if you want to use these)
        # TS = 20
        # KS = 60
        # SS = 120
        # CS = 60
        # OS = 0


        # Then add a column for each Ichimoku indicator output to that dataset.
        # Each column represents the output of the First Ichimoku Variable tuple and its specific column.
        dataframe['tenkan'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ITS_{TS}']
        dataframe['kijun'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'IKS_{KS}']
        dataframe['senkanA'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ISA_{TS}']
        dataframe['senkanB'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ISB_{KS}']
        dataframe['chiko'] = pta.ichimoku(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], tenkan=TS, kijun=KS, senkou=SS, offset=OS)[0][f'ICS_{KS}']

        def trade_condition(dataframe):
            """
            This function returns the position the close price has in comparison to TS and KS.
            """
            signal_position = []

            for i in range(len(dataframe)):
                if (dataframe['close'][i] > dataframe['tenkan'][i]) & (dataframe['close'][i] > dataframe['kijun'][i]):
                    # Check if the close price is above the TS AND also above the KS
                    # Then append a entry to the signal_position list.
                    signal_position.append('long')
                elif  (dataframe['close'][i] < dataframe['tenkan'][i]) & (dataframe['close'][i] < dataframe['kijun'][i]):
                    # If first condition is not met, check if price is below TS AND KS
                    # Then append a entry to the signal_position list.
                    signal_position.append('short')
                else:
                    # Apparently price is not above, nor below TS and KS (somewhere in between)
                    signal_position.append('neutral')

            return signal_position

        # Create a dataframe column with the output of the trade_condition function
        dataframe['position'] = trade_condition(dataframe)

        def trade_crossover(dataframe):
            """ 
            This function creates two columns that indicate if there is a crossover of TS and KS and returns the prices in the
            respective long or short crossover column.
            """
            long_crossover = []
            short_crossover = []

            # Create a marker that can help us determining the previous state of this function.
            # This way we will prevent double crossovers.
            marker = 0

            for i in range(len(dataframe)):
                if dataframe['tenkan'][i] > dataframe['kijun'][i]:
                    if (marker != 1):
                        long_crossover.append(dataframe['close'][i])
                        short_crossover.append(np.NaN)
                        marker = 1
                        # print([i], 'LONG', dataframe['date'][i], marker)
                    else:
                        long_crossover.append(np.NaN)
                        short_crossover.append(np.NaN)

                elif dataframe['tenkan'][i] < dataframe['kijun'][i]:
                    if (marker != -1):
                        short_crossover.append(dataframe['close'][i])
                        long_crossover.append(np.NaN)
                        marker = -1
                        # print([i], 'SHORT', dataframe['date'][i], marker)
                    else:
                        long_crossover.append(np.NaN)
                        short_crossover.append(np.NaN)
                else:
                    long_crossover.append(np.NaN)
                    short_crossover.append(np.NaN)


            return long_crossover, short_crossover

        # Create the two dataframe columns that indicate a long or short TS / KS crossover
        dataframe['long_crossover'] = trade_crossover(dataframe)[0]
        dataframe['short_crossover'] = trade_crossover(dataframe)[1] 

        def create_signal(dataframe):
            """
            This function will create the definitive buy or sell signal based on the position and the long or short crossover column.
            """
            signal = []

            for i in range(len(dataframe)):
                # For each not null value in the long_crossover field AND when position advise is long... 
                if pd.notnull(dataframe['long_crossover'][i]) & (dataframe['position'][i] == 'long'):
                    # Then signal is to buy
                    signal.append('buy')
                # Also when the short_crossover cell has a value (= a crossover signal) AND the advice is dhort, then...
                elif pd.notnull(dataframe['short_crossover'][i]) & (dataframe['position'][i] == 'short'):
                    # add the sell signal to the signal list.
                    signal.append('sell')
                else:
                    # Else you just hold your current position (which is no trade or stay in market)
                    signal.append('hold')

            return signal

        # Create our final column that indicates the signal to act on with this bot.
        dataframe['signal'] = create_signal(dataframe)

        # print(dataframe.tail(60))
        # print(dataframe[['date','close','position','long_crossover','signal']][dataframe['signal']=='buy'].tail(25))
        # print(dataframe[['date','close','position','short_crossover','signal']][dataframe['signal']=='sell'].tail(25))
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['signal'] == 'buy')
            ),
            ['enter_long','enter_tag']] = (1,'TS_KS_long_crossover')
        dataframe.loc[
            (
                (dataframe['signal'] == 'sell')
            ),
            ['enter_short','enter_tag']] = (1,'TS_KS_short_crossover')

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['tenkan'])
            ),
            ['exit_long','exit_tag']] = (1,'Closeprice_below_KS')
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['tenkan'])
            ),
            ['exit_short','exit_tag']] = (1,'Closeprice_above_KS')
        return dataframe
