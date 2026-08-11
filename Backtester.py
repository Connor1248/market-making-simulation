import yfinance as yf
import pandas
import numpy as np

tickers = [
    "^GSPC",  # S&P 500
    "SPY",    # S&P 500 ETF
    "QQQ",    # Nasdaq-100
    "IWM",    # Russell 2000
    "GLD",    # Gold
    "TLT",    # Bonds
    "AAPL",   # Apple
    "NVDA",   # NVIDIA
]

differences = []
def moving_avg(ticker):
    data = yf.download(ticker, start='2010-01-01', end='2026-01-01')
    data.columns = data.columns.get_level_values(0)

    data['returns'] = data['Close'].pct_change()

    total_increase = (1 + data['returns']).cumprod().iloc[-1]

    avg_yearly_profit = total_increase**(1/((data.index[-1] - data.index[0]).days / 365.25))-1

    data['short_ma'] = data['Close'].rolling(window=50).mean()
    data['long_ma'] = data['Close'].rolling(window=200).mean()
    data['short>long'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)

    data['my_returns'] = data['short>long'].shift(1) * data['returns']

    my_total_increase = (1 + data['my_returns']).cumprod().iloc[-1]

    my_avg_yearly_profit = my_total_increase**(1/((data.index[-1] - data.index[0]).days / 365.25))-1

    differences.append(my_avg_yearly_profit - avg_yearly_profit)
    print(my_avg_yearly_profit - avg_yearly_profit)
    print(np.mean(differences))

def RSI(ticker):
    data = yf.download(ticker, start='2010-01-01', end='2026-01-01')
    data.columns = data.columns.get_level_values(0)

    data['returns'] = data['Close'].pct_change()
    
    total_increase = (1 + data['returns']).cumprod().iloc[-1]

    avg_yearly_profit = total_increase**(1/((data.index[-1] - data.index[0]).days / 365.25))-1

    data['gains'] = np.where(data['returns'] > 0 , data['returns'], 0)
    data['losses'] = np.where(data['returns'] < 0 , -data['returns'], 0)

    data['avg_gains'] = data['gains'].rolling(window=14).mean()
    data['avg_losses'] = data['losses'].rolling(window=14).mean()

    data['RSI'] = (100 - 100/(1 + data['avg_gains']/data['avg_losses'])).shift(1)

    in_position = False
    price = 0
    in_positions = []
    
    for t in range(len(data['RSI'])):
        
        if in_position == True:
            in_positions.append(1)
            
        elif in_position == False:
            in_positions.append(0)
            
        if data['RSI'].iloc[t] < 30 and in_position == False:
            in_position = True
            price = data['Close'].iloc[t]
            in_positions[-1] = 1
            
        elif data['RSI'].iloc[t] > 70 and in_position == True:
            in_position = False
            price = 0
            in_positions[-1] = 1
            
    data['in_position'] = in_positions
    data['my_returns'] = data['returns']*data['in_position']
    
    my_total_increase = (1 + data['my_returns']).cumprod().iloc[-1]

    my_avg_yearly_profit = my_total_increase**(1/((data.index[-1] - data.index[0]).days / 365.25))-1

    print(my_avg_yearly_profit)
    print(data['my_returns'].std() * np.sqrt(252))


for ticker in tickers:
    RSI(ticker)
    
    
