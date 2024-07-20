from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException, ConnectionError

def scrap_stock_data(symbol, exchange):
    stock_response = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    if exchange == "NASDAQ":
        url = f"https://finance.yahoo.com/quote/{symbol}/"
    elif exchange == "National Stock Exchange":
        symbol = f"{symbol}.NS"
        url = f"https://finance.yahoo.com/quote/{symbol}/"
    else:
        print("Stock Exchange not supported.")
        return stock_response

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except (RequestException, ConnectionError) as e:
        print(f"Failed to retrieve data for {symbol}. Error: {e}")
        return stock_response

    soup = BeautifulSoup(response.content, 'html.parser')

    stock_response = {}
    
    try:
        stock_response["current_price"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketPrice'})['data-value']
    except Exception as e:
        stock_response["current_price"] = None
        print(f"Error retrieving current price: {e}")

    try:
        stock_response["previous_close"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketPreviousClose'})['data-value']
    except Exception as e:
        stock_response["previous_close"] = None
        print(f"Error retrieving previous close: {e}")

    try:
        stock_response["price_change"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketChange'})['data-value']
    except Exception as e:
        stock_response["price_change"] = None
        print(f"Error retrieving price change: {e}")

    try:
        stock_response["percentage_change"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketChangePercent'})['data-value']
    except Exception as e:
        stock_response["percentage_change"] = None
        print(f"Error retrieving percentage change: {e}")

    try:
        week_52_range = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'fiftyTwoWeekRange'})['data-value']
        stock_response["week_52_low"], stock_response["week_52_high"] = week_52_range.split(' - ')
    except Exception as e:
        stock_response["week_52_low"] = stock_response["week_52_high"] = None
        print(f"Error retrieving 52-week range: {e}")

    try:
        stock_response["pe_ratio"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'trailingPE'})['data-value']
    except Exception as e:
        stock_response["pe_ratio"] = None
        print(f"Error retrieving PE ratio: {e}")

    try:
        stock_response["market_cap"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'marketCap'})['data-value']
    except Exception as e:
        stock_response["market_cap"] = None
        print(f"Error retrieving market cap: {e}")

    try:
        stock_response["avg_volume"] = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'averageVolume'})['data-value']
    except Exception as e:
        stock_response["avg_volume"] = None
        print(f"Error retrieving average volume: {e}")

    return stock_response

