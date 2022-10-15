# Strategies

My collection of strategies that have been tested on the [Freqtrade trading bot](https://www.freqtrade.io/en/stable/), together with their backtesting results and hyperopt files (when available). I have collected as much old backtesting information as possible to create this general repository of backtesting information. Some of the information was lost however, and some of the directories contain experimental stuff. Nonetheless I wanted to create a general publicly available repo of all the informaion I gathered. I hope you appreciate it!

# Sources

These strategies are gathered from sources like Github, Youtube and misc. websites. Some of them will also be completely new and developed by myself. 
I will try to add the source of each strategy so that the original authors get the credits they deserve for their hard work!

You can use all this information in your own strategies, just as long as you remember that **everything is at your own risk**!!

# Strategy League

Below the total strategy league of all tested strategies.  
Latest update: 28 sept 2022  
with the TenkanSen KijunSen crossover results


| Strategy                         | Best timeframe | End Balance | Profit % | Drawdown | Total trades | Wins | Draws | Losses | Win% | Draws% | Loss % | Average risk per trade | Risk of Ruin | # pairs with profit | # Pairs without profit | Pairs Profit ratio | Score |
|----------------------------------|----------------|-------------|----------|----------|--------------|------|-------|--------|------|--------|--------|------------------------|--------------|---------------------|------------------------|--------------------|-------|
| Nostalgia For Infinity X         | 15 Min         | 6420.82     | 542%     | 18%      | 1457         | 1360 | 0     | 97     | 93%  | 0%     | 7%     | 507.28                 | 1%           | 37                  | 13                     | 74%                | 236   |
| Keltner channel & Rsi            | 1 Day          | 57096.70    | 5610%    | 15%      | 463          | 180  | 0     | 283    | 39%  | 0%     | 61%    | 1915.9                 | 127%         | 37                  | 13                     | 74%                | 192   |
| Sma Rsi Strategy                 | 1 Day          | 51171.91    | 5017%    | 29%      | 515          | 266  | 0     | 249    | 52%  | 0%     | 48%    | 1817.48                | 96%          | 34                  | 15                     | 68%                | 180   |
| Rsi, Stochastics & MACD          | 1 Day          | 60524.29    | 5952%    | 24%      | 602          | 274  | 0     | 328    | 46%  | 0%     | 54%    | 1529.45                | 112%         | 31                  | 19                     | 62%                | 178   |
| Vulcan strategy                  | 4 hour         | 65391.25    | 6439%    | 42%      | 3577         | 1740 | 161   | 1676   | 49%  | 5%     | 47%    | 2481.41                | 102%         | 33                  | 17                     | 66%                | 153   |
| Riding Bollinger bands           | 1 Day          | 39140.48    | 3814%    | 36%      | 425          | 290  | 6     | 129    | 68%  | 1%     | 30%    | 1402.7                 | 58%          | 36                  | 14                     | 72%                | 150   |
| Scalp                            | 1 Day          | 2069.05     | 107%     | 19%      | 228          | 165  | 0     | 63     | 72%  | 0%     | 28%    | 125.68                 | 0%           | 37                  | 12                     | 74%                | 156   |
| GodStra                          | 1 Day          | 13703.51    | 1270%    | 30%      | 708          | 627  | 15    | 66     | 89%  | 2%     | 9%     | 358.66                 | 0%           | 8                   | 42                     | 16%                | 106   |
| SMA MACD Crossover               | 1 Day          | 39029.72    | 3803%    | 31%      | 990          | 348  | 0     | 642    | 35%  | 0%     | 65%    | 1142.9                 | 171%         | 38                  | 13                     | 76%                | 143   |
| Simple strategy                  | 1 Day          | 18301.95    | 1730%    | 33%      | 369          | 243  | 40    | 86     | 66%  | 11%    | 23%    | 722.14                 | 40%          | 33                  | 17                     | 66%                | 137   |
| SmoothScalp                      | 30 Min         | 2511.63     | 151%     | 23%      | 2486         | 1472 | 487   | 527    | 59%  | 20%    | 21%    | 158.89                 | 10%          | 36                  | 14                     | 72%                | 128   |
| Golden / Death Cross (HR)        | 1 hour         | 83828.73    | 8283%    | 40%      | 1334         | 481  | 0     | 853    | 36%  | 0%     | 64%    | 2430.07                | 127%         | 27                  | 23                     | 54%                | 137   |
| ADX Momentum                     | 1 Day          | 33142.05    | 3214%    | 42%      | 548          | 307  | 86    | 155    | 56%  | 16%    | 28%    | 1018.2                 | 79%          | 34                  | 16                     | 68%                | 130   |
| ReinforcedSmoothScalp            | 15m            | 20960.25    | 1996%    | 39%      | 7384         | 4646 | 585   | 2153   | 63%  | 8%     | 29%    | 852.95                 | 54%          | 39                  | 11                     | 78%                | 135   |
| Dema Sma Crossover               | 1 Day          | 46835.04    | 4584%    | 49%      | 4240         | 1801 | 0     | 2439   | 42%  | 0%     | 58%    | 1820.59                | 118%         | 35                  | 15                     | 70%                | 133   |
| HiLo & MACD                      | 1 Day          | 33070.37    | 3207%    | 43%      | 713          | 297  | 0     | 416    | 42%  | 0%     | 58%    | 1339.75                | 129%         | 32                  | 18                     | 64%                | 117   |
| Golden / Death Cross (LR)        | 1 hour         | 3685.57     | 269%     | 34%      | 1922         | 1206 | 0     | 716    | 63%  | 0%     | 37%    | 199.45                 | 7%           | 36                  | 14                     | 72%                | 113   |
| Huck loves her bucks             | 1 Day          | 3036.57     | 204%     | 18%      | 228          | 96   | 0     | 132    | 42%  | 0%     | 58%    | 203.5                  | 478%         | 33                  | 17                     | 66%                | 111   |
| Tenkan/Kijun crossover 'classic' | 1 Day          | 7197.30     | 620%     | 27%      | 560          | 217  | 0     | 343    | 39%  | 0%     | 61%    | 379.88                 | 334%         | 31                  | 19                     | 62%                | 106   |
| Bollinger band & Rsi             | 1 Day          | 1795.43     | 80%      | 38%      | 170          | 122  | 10    | 38     | 72%  | 6%     | 22%    | 98.91                  | 0%           | 29                  | 14                     | 58%                | 99    |
| ADX Sma's                        | 1 Day          | 6821.59     | 582%     | 42%      | 585          | 330  | 7     | 248    | 56%  | 1%     | 42%    | 365.84                 | 49%          | 31                  | 19                     | 62%                | 97    |
| Supertrend                       | 4 hour         | 6467.03     | 547%     | 60%      | 1715         | 909  | 333   | 473    | 53%  | 19%    | 28%    | 353.18                 | 71%          | 29                  | 21                     | 58%                | 85    |
| TD Sequential (bmoulkaf)         | 1 Day          | 3178.97     | 218%     | 23%      | 934          | 121  | 1     | 812    | 13%  | 0%     | 87%    | 160.2                  | 14594933%    | 32                  | 18                     | 64%                | 81    |
| Kumo breakout 'classic'          | 5 Min          | 10397.79    | 940%     | 42%      | 342          | 115  | 0     | 227    | 34%  | 0%     | 66%    | 209.28                 | 2577%        | 29                  | 21                     | 58%                | 71    |
| Heracles                         | 4 hour         | 1765.39     | 77%      | 39%      | 1255         | 614  | 457   | 184    | 49%  | 36%    | 15%    | 118.55                 | 144%         | 28                  | 22                     | 56%                | 65    |
| Swing High to Sky                | 5 Min          | 9038.69     | 804%     | 43%      | 801          | 511  | 43    | 247    | 64%  | 5%     | 31%    | 286.96                 | 14%          | 14                  | 36                     | 28%                | 55    |

# Support

If you like my work, consider subscribing to my [Youtube channel](https://www.youtube.com/c/DutchCryptoDad) or become my [Patreon](https://www.patreon.com/dutchcryptodad).

Another easy way of supporting me is to donate to one of my Tip Jars below:

* BTC 💰  : 12mjuhTzXuGt4uYPZbtNLgKxYvJG2RJTuo
* ETH 💰  : 0x8F874ead2eedF456Abb5C57cBE1501A56E3e826a
* USDT 💰 : 0x8F874ead2eedF456Abb5C57cBE1501A56E3e826a
* SOL 💰  : 97JHyYVjXus1LQQmw6WnidtKcDqMqCxNGEAFkJksdsm6

Thank you and enjoy!


Ps. And if I did use a strategy and I did not give you the credits, just take contact an i'll fix it.
