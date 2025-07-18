import yfinance as yf

def get_stock_summary(ticker="TCS.NS"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="7d")
        current_inr = hist['Close'].iloc[-1]

        usd_inr = yf.Ticker("USDINR=X").history(period="1d")['Close'].iloc[-1]
        current_usd = current_inr / usd_inr

        change_percent = ((current_inr - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100

        return f"{ticker} is currently ${current_usd:.2f}, changed {change_percent:.2f}% in the past week (converted from ₹{current_inr:.2f})."
    except Exception as e:
        return f"Unable to fetch stock data for {ticker}: {str(e)}"
