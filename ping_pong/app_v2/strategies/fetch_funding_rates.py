import requests
import pandas as pd
import time
from datetime import datetime

# Function to fetch funding rate data from Binance API
def fetch_funding_rate(symbol, start_time=None, end_time=None):
    """
    Fetch historical funding rates for a given symbol from Binance.
    """
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": symbol,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000  # Binance limit per request
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []
    
def fibonacci_sequence(data):
    """Fibonacci ratios could be used: dentify potential support and resistence levels. This could work tied with momentum.
    Potential areas where the price could retrace finding a new floor up or down, depending by many factors. 

    Price may retrace or consolidate at this particular levels.
    Key Retracement Levels: 23.6%, 38.2%, 50%, 61.8%, 78.6%


    Example patterns: retrace to 50%, then bounces off => Sig of trend continuation
    its going up, down then refilled => BULLISH SIGNAL

    Example 2:  breaks below fibonacci level => indicates reversal or weakening of the trend
    """
    return 0

def ichimoku_cloud():

    """
    Ichimoku Kinko Hyo.

    Can provide insight about trend indication, support and resistence levels and momentum (Goichi Hosoda)

    CONVERSION LINE     (conversion_line): 9-period moving average
    BASE LINE           (kijun_sen) (base_line): 26-period moving average
    LEADING SPAN A      (senkou_span_a): the moving average of the Conversion(9-periods) and Base(26-periods) Lines projected 26 periods in the future
    LEADING SPAN B      (senkou_span_b): the 52-period moving average projected 26 periods in the future
    
    LAGGING SPAN        (chinkou_span): closing price of the current period projected 26 periods in the past

    Provide an holistic view of price actions and market conditions.

    Cloud: feature of the indicator: area of support and resistence.

    TWO CASES
    price above the cloud -> bullish kumo
    price below the cloud -> bearish kumo
    
    - - - 
    tenkan_sen e kijun_sen
    - calculated on HIGHEST_HIGH, LOWEST_LOW
    - dynamic support and resistance levels
    - - -
    chinkou_span
    current closing price plotted backwards (9-26-52) periods in the past

    - identify potential trends reversal
    - traders prefer it without lagging span
    - cleaner view of other elements
    - - -
    (senkou_span_a): (senkou_span_b): 
    the 52-period moving average projected 26 periods in the future
    the moving average of the Conversion(9-periods) and Base(26-periods) Lines projected 26 periods in the future
    POTENTIAL CHANGES IN TREND DIRECTION CAN BE IDENTIFIED WHEN WE MOVE AROUND SENKOU
    alsao by kumo twist
    entry and exist points
    - they are the edges of the cloud, indicating support and resistance levels
    - space betweens spans gives color to clouds

    CROSSOVER + BREAK ABOVE => ENTRY Signal
    """

# Function to save data locally
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main script to fetch and save funding rate data
def main():
    # Example: Fetch funding rate for BTCUSDT
    symbol = "BTCUSDT"

    # Specify a start and end time (e.g., last 30 days)
    end_time = int(time.time() * 1000)  # Current timestamp in ms
    start_time = end_time - 30 * 24 * 60 * 60 * 1000  # 30 days ago in ms

    print(f"Fetching funding rate data for {symbol} from {datetime.fromtimestamp(start_time / 1000)} to {datetime.fromtimestamp(end_time / 1000)}")

    # Fetch data
    data = fetch_funding_rate(symbol, start_time=start_time, end_time=end_time)

    # Convert to DataFrame and save to CSV
    if data:
        save_to_csv(data, f"funding_rate_{symbol}.csv")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    main()
