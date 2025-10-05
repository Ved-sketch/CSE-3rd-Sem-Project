#!/usr/bin/env python3
"""
Test script to verify stock data APIs are working
"""

import yfinance as yf
import requests

def test_stock_apis():
    """Test stock data APIs"""
    
    print("🔍 Testing Stock Data APIs...")
    print("=" * 60)
    
    # Test yfinance for individual stocks
    print("\n📊 Testing yfinance for individual stocks...")
    test_stocks = ["AAPL", "GOOGL", "MSFT"]
    
    for symbol in test_stocks:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d")
            info = stock.info
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                print(f"✅ {symbol}: ${current_price:.2f}")
            else:
                print(f"❌ {symbol}: No data available")
                
        except Exception as e:
            print(f"❌ {symbol}: Error - {str(e)}")
    
    # Test market indices
    print("\n🏛️ Testing market indices...")
    indices = {"^GSPC": "S&P 500", "^DJI": "Dow Jones", "^IXIC": "NASDAQ"}
    
    for symbol, name in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            
            if not hist.empty:
                current_value = hist['Close'].iloc[-1]
                if len(hist) >= 2:
                    prev_value = hist['Close'].iloc[-2]
                    change_percent = ((current_value - prev_value) / prev_value) * 100
                    arrow = "▲" if change_percent > 0 else "▼"
                    print(f"✅ {name}: {current_value:.2f} {arrow} {change_percent:+.2f}%")
                else:
                    print(f"✅ {name}: {current_value:.2f}")
            else:
                print(f"❌ {name}: No data available")
                
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Stock API Test Complete!")

if __name__ == "__main__":
    test_stock_apis()
