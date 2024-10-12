import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Define stock symbols and date range
apple_symbol = 'AAPL'
sp500_symbol = '^GSPC'
start_date = '2020-01-01'
end_date = '2023-12-31'

# Download historical data
apple_data = yf.download(apple_symbol, start=start_date, end=end_date)
sp500_data = yf.download(sp500_symbol, start=start_date, end=end_date)

# Calculate daily returns
apple_data['Returns'] = apple_data['Adj Close'].pct_change()
sp500_data['Returns'] = sp500_data['Adj Close'].pct_change()
#print(sp500_data)
#print(apple_data)

# Calculate volatility
apple_volatility = np.std(apple_data['Returns'])
sp500_volatility = np.std(sp500_data['Returns'])

# Calculate beta
cov_matrix = np.cov(apple_data['Returns'][1:], sp500_data['Returns'][1:])
beta = cov_matrix[0, 1] / np.var(sp500_data['Returns'][1:])


# Calculate Sharpe ratio
sharpe_ratio = apple_data['Returns'].mean() / apple_volatility

# Visualize daily and weekly returns
apple_data['Weekly Returns'] = apple_data['Returns'].rolling(window=7).mean()
apple_data['Monthly Returns'] = apple_data['Returns'].rolling(window=30).mean()

plt.figure(figsize=(14, 7))
plt.plot(apple_data['Returns'], label='Daily Returns', color='blue', alpha=0.6)
plt.plot(apple_data['Weekly Returns'], label='Weekly Returns', color='red', alpha=0.6)
plt.title('Apple Daily and Weekly Returns')
plt.legend()
plt.show()

# Calculate cumulative returns
cumulative_returns = (1 + apple_data['Returns']).cumprod()

plt.figure(figsize=(14, 7))
plt.plot(cumulative_returns, label='Cumulative Returns', color='green')
plt.title('Apple Cumulative Returns')
plt.legend()
plt.show()

# Additional metrics
alpha = apple_data['Returns'].mean() - beta * sp500_data['Returns'].mean()
treynor_ratio = apple_data['Returns'].mean() / beta
max_drawdown = (cumulative_returns.cummax() - cumulative_returns).max()

# Display results
print(f"Volatility: {apple_volatility:.4f}")
print(f"Beta: {beta:.4f}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Alpha: {alpha:.4f}")
print(f"Treynor Ratio: {treynor_ratio:.4f}")
print(f"Max Drawdown: {max_drawdown:.4f}")
