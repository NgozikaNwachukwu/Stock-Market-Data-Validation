import yfinance as yf
import pandas as pd

# Function to fetch stock data
def fetch_stock_data(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="7d")  # Fetch last 7 days of data
        return hist
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Function to validate stock data
def validate_stock_data(data, stock_symbol):
    issues = []
    
    if data.isnull().values.any():
        issues.append("Missing values found in stock data.")

    # Check for sudden price drop of more than 5% in one day
    data['Price Change %'] = data['Close'].pct_change() * 100
    if (data['Price Change %'].abs() > 5).any():
        issues.append("Sudden large price change detected!")

    # Save results to CSV
    data.to_csv(f"{stock_symbol}_validated.csv")

    return issues

# Main execution
if __name__ == "__main__":
    stock_symbol = input("Enter a stock symbol (e.g., AAPL, TSLA): ").upper()
    stock_data = fetch_stock_data(stock_symbol)

    if stock_data is not None:
        validation_issues = validate_stock_data(stock_data, stock_symbol)
        if validation_issues:
            print(f"⚠️ Issues found in {stock_symbol}:")
            for issue in validation_issues:
                print(f"- {issue}")
        else:
            print(f"✅ Data for {stock_symbol} is clean. No issues found.")

        print(f"📁 Report saved: {stock_symbol}_validated.csv")
