# Merger Announcement Returns

This project analyzes short-term stock price reactions to merger and acquisition
announcements, focusing on whether deal characteristics explain abnormal returns
for acquiring firms.

## Research Questions
- Do acquiring firms earn abnormal returns around merger announcements?
- Can deal characteristics explain short-term market reactions?

## Data
- Publicly available merger and acquisition deal data
- Daily stock returns for acquiring firms
- Market benchmark returns (e.g., S&P 500)

## Methodology
- Event-study framework
- Market-adjusted returns
- Logistic regression to predict positive announcement-window returns

## Key Findings
- Average adjusted returns are close to zero
- Deal-level characteristics have very limited predictive power
- Results are consistent with semi-strong market efficiency

## Repository Structure
data/
acq_raw.csv
acq_processed.csv
src/
get_acq_metrics.py
analysis/
merger_analysis.ipynb
report/
merger_final_report.pdf


## Files
- `get_acq_metrics.py`: Cleans raw deal data and computes announcement-window returns
- `merger_analysis.ipynb`: Exploratory analysis and modeling
- `merger_final_report.pdf`: Final written report

## Notes
This project is intended as an independent research-style analysis rather than a
trading strategy. Weak predictive performance is expected given market efficiency.
