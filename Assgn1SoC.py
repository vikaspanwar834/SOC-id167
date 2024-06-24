import pandas as pd
import numpy as np

nifty = pd.read_csv('^NSEI.csv', parse_dates=['Date'], index_col='Date')
tata = pd.read_csv('TATAMOTORS.NS.csv', parse_dates=['Date'], index_col='Date')

nifty['Returns'] = nifty['Close'].pct_change()
tata['Returns'] = tata['Close'].pct_change()

nifty = nifty.dropna()
tata = tata.dropna()
data = pd.concat([nifty['Returns'], tata['Returns']], axis=1).dropna()
data.columns = ['NIFTY', 'TATA']

covariance = data.cov().iloc[0,1]
market_variance = data['NIFTY'].var()
beta = covariance / market_variance

risk_free_rate = 0.07015  
average_return_tata = data['TATA'].mean() * 252  
average_return_market = data['NIFTY'].mean() * 252  
alpha = average_return_tata - (risk_free_rate + beta * (average_return_market - risk_free_rate))

excess_return_tata = data['TATA'] - (risk_free_rate / 252)
sharpe_ratio_tata = np.sqrt(252) * excess_return_tata.mean() / excess_return_tata.std()

excess_return_nifty = data['NIFTY'] - (risk_free_rate / 252)
sharpe_ratio_nifty = np.sqrt(252) * excess_return_nifty.mean() / excess_return_nifty.std()

def calculate_max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min()

max_drawdown_tata = calculate_max_drawdown(data['TATA'])
max_drawdown_nifty = calculate_max_drawdown(data['NIFTY'])

print(f"Beta of TATA MOTORS: {beta:.4f}")
print(f"Alpha of TATA MOTORS: {alpha:.4f}")
print(f"Sharpe Ratio of TATA MOTORS: {sharpe_ratio_tata:.4f}")
print(f"Sharpe Ratio of NIFTY50: {sharpe_ratio_nifty:.4f}")
print(f"Max Drawdown of TATA MOTORS: {max_drawdown_tata:.4f}")
print(f"Max Drawdown of NIFTY50: {max_drawdown_nifty:.4f}")