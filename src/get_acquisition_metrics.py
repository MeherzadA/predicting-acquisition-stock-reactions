import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

# ||--------------------------------------------------------------------------------------------------------------------||
# || This script computes announcement-window return metrics used in the analysis (adjusted return, relative deal size) ||
# ||--------------------------------------------------------------------------------------------------------------------||

# ------------------------------
# 1. Load initial dataset
# ------------------------------
filename = "data/acquisitions_raw.csv"
df = pd.read_csv(filename)
num_rows = df.shape[0]

# S&P 500 ticker
sp500 = yf.Ticker("^GSPC")

# store results here (will be added as columns at the end)
acq_return_list = []
sp500_return_list = []
true_adj_return_list = []
mkt_cap_list = []
rel_size_list = []

print(f"Processing {num_rows} deals...\n")

# ------------------------------
# 2. Loop through each deal
# ------------------------------
for i in range(num_rows):
    acq_ticker = df["Acquirer_Ticker"][i]
    target_ticker = df["Target_Ticker"][i]
    announce_date_str = df["Announcement_Date"][i]
    deal_size = df["Deal_Size_B"][i]

    # get the dates (buffer)
    dt_obj = datetime.strptime(announce_date_str, "%Y-%m-%d")
    start_buf = (dt_obj - timedelta(days=20)).strftime("%Y-%m-%d")
    end_buf = (dt_obj + timedelta(days=10)).strftime("%Y-%m-%d")

    # get the pricing information and clean up data (Timezones, Index) (BOTH stock and S&P 500)
    curr_stock = yf.Ticker(acq_ticker)
    df_prices = curr_stock.history(start=start_buf, end=end_buf).reset_index()
    df_prices['Date'] = df_prices['Date'].dt.tz_localize(None)
    df_sp = sp500.history(start=start_buf, end=end_buf).reset_index()
    df_sp['Date'] = df_sp['Date'].dt.tz_localize(None)

    # create new list of prices where the rows are only the ones where date is equal or AFTER announcement date
    # first row of the list is the FIRST date that market was open following announcement 
    future_rows = df_prices[df_prices['Date'] >= pd.Timestamp(dt_obj)]
    reaction_idx = future_rows.index[0]

    # get the stock data and the specific dates we used (same date for the S&P 500 data as well) 
    row_today = df_prices.iloc[reaction_idx]
    row_yesterday = df_prices.iloc[reaction_idx - 1]
    date_today = row_today['Date']
    date_yesterday = row_yesterday['Date']

    # We filter the S&P dataframe to find the rows matching the dates we just found
    sp_today = df_sp[df_sp['Date'] == date_today]
    sp_yesterday = df_sp[df_sp['Date'] == date_yesterday]
    sp_close_today = sp_today['Close'].values[0]
    sp_close_yesterday = sp_yesterday['Close'].values[0]

    # MATH!!!!!!
    # calculate stock return
    acq_return = (row_today['Close'] - row_yesterday['Close']) / row_yesterday['Close']
    sp_return = (sp_close_today - sp_close_yesterday) / sp_close_yesterday
    true_adj_return = round(acq_return - sp_return, 4)

    acq_return_list.append(round(acq_return, 4))
    sp500_return_list.append(round(sp_return, 4))
    true_adj_return_list.append(true_adj_return)

    # ----- Market Cap & Relative Deal Size -----
    ticker = yf.Ticker(acq_ticker)

    # Strategy A: Quarterly statement
    q_stmt = ticker.quarterly_income_stmt
    shares_found = None
    if not q_stmt.empty:
        stmt_dates = q_stmt.columns
        stmt_dates_naive = [d.replace(tzinfo=None) for d in stmt_dates]
        time_diffs = [abs((d - dt_obj).days) for d in stmt_dates_naive]
        min_diff = min(time_diffs)
        if min_diff < 120:
            best_idx = time_diffs.index(min_diff)
            best_date = stmt_dates[best_idx]
            if 'Basic Average Shares' in q_stmt.index:
                shares_found = q_stmt.loc['Basic Average Shares', best_date]
            elif 'BasicAverageShares' in q_stmt.index:
                shares_found = q_stmt.loc['BasicAverageShares', best_date]

    # Strategy B: fallback historic shares
    if shares_found is None or np.isnan(shares_found):
        hist_shares = ticker.get_shares_full(start=announce_date_str)
        if not hist_shares.empty:
            shares_found = hist_shares.iloc[0]

    # Price at announcement
    hist_price = ticker.history(start=announce_date_str, end=(dt_obj + timedelta(days=5)).strftime("%Y-%m-%d"))
    price_at_deal = hist_price['Close'].iloc[0]

    # Market Cap and Relative Deal Size
    mkt_cap_b = (price_at_deal * shares_found) / 1_000_000_000
    rel_size = deal_size / mkt_cap_b

    mkt_cap_list.append(mkt_cap_b)
    rel_size_list.append(rel_size)

    # print each entry and results
    print(f"{i+1}/{num_rows} | {acq_ticker} acquires {target_ticker} ({announce_date_str})")
    print(f"   Acquirer Return: {acq_return:.4f} | S&P 500 Return: {sp_return:.4f} | Abnormal Return: {true_adj_return:.4f}")
    print(f"   Cap: ${mkt_cap_b:.2f}B | Rel Size: {rel_size:.3f}")
    print("-" * 30)

# ------------------------------
# 3. Save final CSV
# ------------------------------
df['Acquirer_Return'] = acq_return_list
df['SP500_Return'] = sp500_return_list
df['True_Adjusted_Return'] = true_adj_return_list
df['Acquirer_Market_Cap_B'] = mkt_cap_list
df['Relative_Deal_Size'] = rel_size_list


df.to_csv("data/acquisitions_processed.csv", index=False)
print("\nSuccess! Saved as acquisitions_processed.csv in data directory.")
