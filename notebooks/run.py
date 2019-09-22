from src import portfolio, asset

if __name__ == '__main__':
    pe = portfolio.engine()
    ae = asset.engine()
    ae.get_combined_charts(['fut_gold', 'idx_us_spx'])
    #pe.get_percent_daily_returns(['fut_gold', 'idx_us_spx'])
