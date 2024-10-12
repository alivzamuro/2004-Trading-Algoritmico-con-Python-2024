import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

def find_support_resistance(df, window=10):
    supports = []
    resistances = []
    for i in range(window, len(df) - window):
        is_support = np.min(df['Low'][i-window:i+window+1]) == df['Low'][i]
        is_resistance = np.max(df['High'][i-window:i+window+1]) == df['High'][i]
        if is_support:
            supports.append((df['Date'][i], df['Low'][i]))
        if is_resistance:
            resistances.append((df['Date'][i], df['High'][i]))
    return supports, resistances

# Fetch historical data for Tesla (TSLA)
data = yf.download('TSLA', start='2020-01-01', end='2023-01-01')
data.reset_index(inplace=True)

# Detect support and resistance levels
supports, resistances = find_support_resistance(data)

# Plot candlestick chart
fig, ax = plt.subplots(figsize=(12, 8))
mpf.plot(data.set_index('Date'), type='candle', ax=ax, style='charles')

# Plot support and resistance levels
for support in supports:
    plt.axhline(y=support[1], color='g', linestyle='--', lw=1)
for resistance in resistances:
    plt.axhline(y=resistance[1], color='r', linestyle='--', lw=1)

plt.title('TSLA Support and Resistance Levels')
plt.show()
