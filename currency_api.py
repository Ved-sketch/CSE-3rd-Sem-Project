import requests
import json
from datetime import datetime

class CurrencyAPI:
    """Real-time currency converter using ExchangeRate-API"""
    
    def __init__(self):
        # Free API for exchange rates (no key required for basic usage)
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.backup_url = "https://api.fxapi.com/latest?access_key=fxapi-your-key&base="
        
        # Fallback rates (in case API is down)
        self.fallback_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
            "JPY": 110.0,
            "CAD": 1.25,
            "AUD": 1.35,
            "CHF": 0.92,
            "CNY": 6.45,
            "INR": 83.2,
            "SGD": 1.35,
            "KRW": 1300.0,
            "BRL": 5.2,
            "MXN": 17.5,
            "RUB": 90.0,
            "ZAR": 15.8
        }
        
        self.currency_names = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "SGD": "Singapore Dollar",
            "KRW": "South Korean Won",
            "BRL": "Brazilian Real",
            "MXN": "Mexican Peso",
            "RUB": "Russian Ruble",
            "ZAR": "South African Rand"
        }
    
    def get_exchange_rates(self, base_currency="USD"):
        """Get live exchange rates"""
        try:
            response = requests.get(f"{self.base_url}{base_currency}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('rates', self.fallback_rates)
            else:
                print(f"API Error: {response.status_code}")
                return self.fallback_rates
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return self.fallback_rates
    
    def convert_currency(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another"""
        try:
            if from_currency == to_currency:
                return amount
            
            # Get rates based on USD
            usd_rates = self.get_exchange_rates("USD")
            
            # Convert to USD first, then to target currency
            if from_currency == "USD":
                usd_amount = amount
            else:
                usd_amount = amount / usd_rates.get(from_currency, 1)
            
            # Convert from USD to target currency
            if to_currency == "USD":
                converted_amount = usd_amount
            else:
                converted_amount = usd_amount * usd_rates.get(to_currency, 1)
            
            return converted_amount
        
        except Exception as e:
            print(f"Error converting currency: {e}")
            return 0
    
    def get_currency_info(self, currency_code):
        """Get currency name"""
        return self.currency_names.get(currency_code, currency_code)
    
    def get_popular_rates(self):
        """Get rates for popular currencies"""
        try:
            rates = self.get_exchange_rates("USD")
            popular = ["EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR"]
            return {curr: rates.get(curr, 1) for curr in popular if curr in rates}
        except:
            return {curr: self.fallback_rates.get(curr, 1) for curr in ["EUR", "GBP", "JPY", "INR"]}

# Test the API
if __name__ == "__main__":
    api = CurrencyAPI()
    print("Testing Currency API...")
    
    # Test conversion
    result = api.convert_currency(100, "USD", "INR")
    print(f"100 USD = {result:.2f} INR")
    
    # Test popular rates
    rates = api.get_popular_rates()
    print("\nPopular rates (vs USD):")
    for curr, rate in rates.items():
        print(f"1 USD = {rate:.4f} {curr}")