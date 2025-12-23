# Stock Market Reactions to Merger Announcements

This project analyzes how the stock prices of acquiring firms react to merger and
acquisition announcements, and whether observable deal characteristics help explain
or predict these short-term market reactions.

The focus is exclusively on the acquiring firm, not the target company.

## Research Focus
The analysis focuses on:
- Do acquiring firms experience abnormal stock returns on announcement dates?
- Are announcement-day returns associated with deal characteristics such as:
  - Relative deal size
  - Industry sector
  - Business type (consumer vs B2B)
  - Regulatory scrutiny

The goal is not to predict stock prices, but to assess whether standard deal-level
information contains useful signal about investor reactions.

## Data
- 91 acquisition announcements across multiple sectors
- Publicly traded acquiring firms
- Daily stock prices for acquirers and the S&P 500

Returns are measured on the announcement date (or next trading day if markets were
closed).

## Methodology
- Event-study framework
- Market-adjusted returns:
  
  Adjusted Return = Acquirer Return − S&P 500 Return

- Statistical analysis:
  - Descriptive statistics and visualizations
  - Sector comparisons and hypothesis testing
  - Logistic regression to model the probability of a positive return
- Machine learning models:
  - Prediction-oriented logistic regression
  - Random forest classifier  
  (both used to see if we can predict if the stock will have a positive or negative return/reaction based on our previously mentioned characteristics).

## Key Findings
- Average announcement-day adjusted returns are close to zero
- Most deals result in small stock price movements
- Relative deal size shows the strongest association with return direction
- Sector, deal type, and regulatory scrutiny provide limited explanatory power
- Logisitic regression model offers prediction no better than random classification, and random forest model offers only modest improvement over baseline methods

Overall, short-term market reactions are difficult to explain using observable deal
characteristics alone, consistent with efficienct market theory and previous studies (sources of which are provided below and in the full pdf report).

## Repository Structure
data/
    acquisitions_raw.csv
    acquisitions_processed.csv
src/
    get_acquisition_metrics.py
analysis/
    M&A Analysis.ipynb
report/
    Market Reaction to Acquirers in Merger and Acquisition Announcements.pdf


## Files
- `get_acq_metrics.py`: Cleans raw deal data and computes adjusted returns
- `merger_analysis.ipynb`: Full analysis, modeling, and visualizations
- `final_report.pdf`: Complete written report with methodology, results, and discussion

## Notes
This project is intended as an analytical and research-style study rather than a
trading strategy. Weak predictive performance is an expected result given market
efficiency and lack of deal/context specific information.

## References
[1] Andrade, G., Mitchell, M., & Stafford, E. (2001). New evidence and perspectives on mergers.
Journal of Economic Perspectives, 15(2), 103–120. https://doi.org/10.1257/jep.15.2.103  

[2] Intellizence. Largest merger and acquisition deals. https://intellizence.com/insights/
merger-and-acquisition/largest-merger-acquisition-deals/  

[3] Wikipedia contributors. (2025, December 21). List of largest mergers and acquisitions.
Wikipedia. https://en.wikipedia.org/wiki/List_of_largest_mergers_and_acquisitions
