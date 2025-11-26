import requests
import json

response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo")

# print(response.ok)
# print(response.status_code)
# print(response.content)
# print(response.json())

data = response.json()
info = data["Meta Data"]["3. Last Refreshed"]
price = data["Time Series (5min)"][info]["1. open"]
symbol = "IBM"
print(symbol,price)

url = "https://data.gov.lv/dati/dataset/8f9d7452-3c64-4a0c-bb50-489fa0335f22/resource/277165b4-1a1c-4ebf-a7f4-364f36347128/download/venta_aizsargjoslu-kategorijas_gala.csv"

info = requests.get(url).text.splitlines()
for line in info:
     if line.strip() == "500; 37824; Skujupīte; L;  ; 14222; 3; 0;  ; 3; Venta; 3,7824E+11":
        print(line.strip())
        
info = requests.get("https://api.thecatapi.com/v1/breeds")

print(response.text)