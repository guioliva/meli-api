from main import MeliApi
import time
import pandas as pd

df = pd.read_csv(r'C:\Users\guilherme.aleixo\Documents\API Meli\data\mlm.csv')
products_list = df['data'].values.tolist()

meliapi = MeliApi()

for i in products_list:

    meliapi.open_mlm(i, option=2)

    time.sleep(1)

    meliapi.sku_data(i)


