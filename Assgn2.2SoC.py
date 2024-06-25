import datetime

def calculate_ytm(PD, rC, m, PT, T, t, recent_coupon_date):
    def bond_price(r):
        n = m * (T - t).days / 365
        return PT * (1 + r/m)**-n + (rC * PT / m) * ((1 - (1 + r/m)**-n) / (r/m)) - PD

    def bond_price_derivative(r):
        n = m * (T - t).days / 365
        return -n * PT * (1 + r/m)**(-n-1) / m - \
               (rC * PT / m) * (n * (1 + r/m)**(-n-1) / (r/m) - \
               ((1 - (1 + r/m)**-n) / (r/m)**2))

    r = rC  # Initial guess
    for _ in range(10):
        r = r - bond_price(r) / bond_price_derivative(r)

    return r

# Example usage for Assignment 2.2 from Accrued Interest pdf and examples 3.4 and 3.5
PD = 1032  # Last traded (dirty) price
rC = 0.1275  # Coupon rate (12.75%)
m = 1  # Annual coupon frequency
PT = 1000  # Face Value
T = datetime.datetime(2019, 4, 1)  # Maturity date
t = datetime.datetime(2014, 7, 14)  # Current date
recent_coupon_date = datetime.datetime(2014, 4, 1)  # Recent past coupon payment date

ytm = calculate_ytm(PD, rC, m, PT, T, t, recent_coupon_date)
print(f"\nYield to Maturity: {ytm:.6f}")