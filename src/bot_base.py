import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
import os

load_dotenv()

class BasicBot:
    def __init__(self, testnet=True):
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        if not self.api_key or not self.api_secret:
            print("ERROR: Add API_KEY and API_SECRET to .env!")
            raise ValueError("Missing keys in .env")
        
        self.client = Client(self.api_key, self.api_secret, testnet=testnet)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        
        logging.basicConfig(
            filename='bot.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("=== Bot Initialized on Testnet ===")
        print("Bot connected! Check bot.log for details.")

    def safe_call(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            self.logger.info(f"SUCCESS: {func.__name__} -> {str(result)[:100]}...")
            return result
        except BinanceAPIException as e:
            msg = f"API ERROR in {func.__name__}: {e.message}"
            self.logger.error(msg)
            print(msg)
            return None
        except Exception as e:
            msg = f"UNEXPECTED ERROR in {func.__name__}: {str(e)}"
            self.logger.error(msg)
            print(msg)
            return None

if __name__ == "__main__":
    bot = BasicBot()
    print("Test complete – Bot ready!")