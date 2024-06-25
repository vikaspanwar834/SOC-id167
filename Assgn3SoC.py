import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

df = pd.read_csv("C:\\Users\\ASUS\\Downloads\\FUTIDX_BANKNIFTY_01-Mar-2020_TO_01-Jun-2020.csv")

df.columns = df.columns.str.strip()

df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
df['Expiry'] = pd.to_datetime(df['Expiry'], format='%d-%b-%y')

df = df.sort_values('Date')

df['TimeToExpiry'] = (df['Expiry'] - df['Date']).dt.days / 365.25

r = 0.0440

df['ModelPrice'] = df['Underlying Value'] * np.exp(r * df['TimeToExpiry'])

output_df = df[['Date', 'Settle Price', 'Underlying Value']].copy()
output_df.columns = ['Date', 'Settle Price', 'Spot Price']
output_df['Model Price'] = df['ModelPrice']

output_df.to_csv('output.csv', index=False)

plt.figure(figsize=(12, 8))
plt.plot(range(len(df)), df['Settle Price'], 'b-o', label='Market Settle Price')
plt.plot(range(len(df)), df['ModelPrice'], 'r-x', label='Model Settle Price')
plt.plot(range(len(df)), df['Underlying Value'], 'g-o', label='Spot Price')

plt.title('BANKNIFTY Future Price Comparison')
plt.xlabel('Day')
plt.ylabel('Price')
plt.legend()  
plt.grid(True)
plt.tight_layout()

plt.savefig('price_comparison.png')
plt.show()

# Calculate mean interest rate
df['ImpliedRate'] = np.log(df['Settle Price'] / df['Underlying Value']) / df['TimeToExpiry']
mean_implied_rate = df['ImpliedRate'].mean()

print(f"Mean implied interest rate: {mean_implied_rate:.4f}")
print(f"Given interest rate: {r:.4f}")
print(f"Percentage error: {abs(mean_implied_rate - r) / r * 100:.2f}%")


print("\nPossible reason for steep decline in underlying price:")
print("The steep decline observed in March 2020 could be attributed to the global market crash caused by the onset of the COVID-19 pandemic and subsequent lockdowns.")

