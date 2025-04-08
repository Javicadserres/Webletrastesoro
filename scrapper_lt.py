import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Iniciamos las columnas del dataframe importantes a coger
data = pd.DataFrame(columns=[
    "Fecha Emisión",
    "Fecha de Vencimiento",
    "Saldo en circulación",
    "Precio Negociado"
])

# Lista de isins que queremos ver de las letras del tesoro. Fuente: https://tesoro.es/deuda-publica/valores-del-tesoro/valores-en-circulacion
isins = ["ES0L02504113", "ES0L02505094", "ES0L02506068", "ES0L02507041", "ES0L02508080", "ES0L02509054", "ES0L02510102", "ES0L02511076", "ES0L02512058", "ES0L02601166", "ES0L02602065", "ES0L02603063"]

# Inicializamos el driver del google chrome
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    for isin in isins:
        # Url de donde queremos sacar los datos de los ISINS
        url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Renta-Fija/Ficha-Emision/Let-Tesoro-Desc-04-2025-" + isin
        driver.get(url)
       
        # Esperamos 1 minuto a tenerlo
        time.sleep(1)
       
        # Diccionario que mapea el campo de los nombres con sus correspondientes XPath
        desired_fields = {
            "Fecha Emisión": '//*[@id="lbl-details-1-4"]',
            "Fecha de Vencimiento": '//*[@id="lbl-details-1-5"]',
            "Saldo en circulación": '//*[@id="root"]/div/div/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]',
            "Precio Negociado": '//*[@id="root"]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[2]/div',  
        }
   
        # Aquí creamos un diccionario con el que ir guardando los elementos
        row_data = {}
        for field, xpath in desired_fields.items():
            try:
                element = driver.find_element(By.XPATH, xpath)
                row_data[field] = element.text
            except Exception as e:
                row_data[field] = None
                print(f"Error al extraer {field} para el ISIN {isin}: {e}")
   
        # Añadimos los datos
        data.loc[isin] = row_data

finally:
    driver.quit()

# Printeamos los datos y los guardamos.
print(data)
data.to_csv('data.csv')
print('0')