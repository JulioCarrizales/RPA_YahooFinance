import yfinance as yf
import time
from winotify import Notification, audio

def get_price(ticker):
     """
     Obtiene el último precio de cierre ajustado de una acción.

     Args:
         ticker (str): El símbolo de cotización de la acción.

     Returns:
         float: El último precio de cierre ajustado, o None si hay un error.
     """
     try:
         ticker_obj = yf.Ticker(ticker)
         data = ticker_obj.history(period="1d")
         return data['Close'].iloc[-1]
     except Exception as e:
         print(f"Error al obtener el precio de {ticker}: {e}")
         return None

def show_notification(ticker, price, condition):
     """
     Muestra una notificación de escritorio.

     Args:
         ticker (str): El símbolo de cotización de la acción.
         price (float): El precio actual de la acción.
         condition (str): La condición que se cumplió ("above" o "below").
     """
     action = "sell" if condition == "above" else "buy"
     toast = Notification(
         app_id="Price Alert",
         title=f"Price Alert for {ticker}",
         msg=f"{ticker} has reached a price of {price:.2f}. You might want to {action}.",
     )
     toast.add_actions(
         label="Go to Yahoo Finance",
         launch=f"https://finance.yahoo.com/quote/{ticker}",
     )
     toast.set_audio(audio.LoopingAlarm6, loop=True)  # Añade loop=True
     toast.show()

def main():
     """
     Función principal que monitorea el precio de una acción y muestra notificaciones.
     """
     ticker = input("Enter the stock ticker (e.g., AAPL, META, NVDA): ").upper()
     while True:
         try:
             upper_limit = float(input(f"Enter the upper price limit for {ticker}: "))
             lower_limit = float(input(f"Enter the lower price limit for {ticker}: "))
             if upper_limit <= lower_limit:
                 print("The upper limit must be greater than the lower limit. Please try again.")
             else:
                 break
         except ValueError:
             print("Invalid input. Please enter numeric values for the limits.")

     print(f"Monitoring {ticker}...")
     while True:
         price = get_price(ticker)
         if price:
             if price > upper_limit:
                 show_notification(ticker, price, "above")
                 print(f"{ticker} is above {upper_limit:.2f}")
             elif price < lower_limit:
                 show_notification(ticker, price, "below")
                 print(f"{ticker} is below {lower_limit:.2f}")
             else:
                 print(f"Current price for {ticker}: {price:.2f}")
         time.sleep(5)  # Puedes ajustar el intervalo de tiempo aquí

if __name__ == "__main__":
     main()