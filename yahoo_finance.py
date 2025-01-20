import yfinance as finanzas
import time
from winotify import Notification, audio

def obtener_precio(simbolo):
    try:
        accion = finanzas.Ticker(simbolo)
        datos = accion.history(period="1d")
        return datos['Close'].iloc[-1]
    except Exception as error:
        print(f"Error al obtener el precio de {simbolo}: {error}")
        return None

def mostrar_alerta(simbolo, precio, estado):
    accion = "vender" if estado == "superior" else "comprar"
    notificacion = Notification(
        app_id="Alerta de Acciones",
        title=f"Alerta para {simbolo}",
        msg=f"{simbolo} ha alcanzado un precio de {precio:.2f}. Considera {accion}.",
    )
    notificacion.add_actions(
        label="Ir a Yahoo Finanzas",
        launch=f"https://finance.yahoo.com/quote/{simbolo}",
    )
    notificacion.set_audio(audio.LoopingAlarm6, loop=True)
    notificacion.show()

def principal():
    simbolo = input("Introduce el símbolo de la acción (ej: AAPL, META, NVDA): ").upper()
    while True:
        try:
            limite_superior = float(input(f"Introduce el límite superior para {simbolo}: "))
            limite_inferior = float(input(f"Introduce el límite inferior para {simbolo}: "))
            if limite_superior <= limite_inferior:
                print("El límite superior debe ser mayor al límite inferior. Intenta de nuevo.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Por favor, introduce valores numéricos.")

    print(f"Monitorizando {simbolo}...")
    while True:
        precio = obtener_precio(simbolo)
        if precio:
            if precio > limite_superior:
                mostrar_alerta(simbolo, precio, "superior")
                print(f"{simbolo} está por encima de {limite_superior:.2f}")
            elif precio < limite_inferior:
                mostrar_alerta(simbolo, precio, "inferior")
                print(f"{simbolo} está por debajo de {limite_inferior:.2f}")
            else:
                print(f"Precio actual de {simbolo}: {precio:.2f}")
        time.sleep(5)

if __name__ == "__main__":
    principal()