from main import MeliApi
import time
import pandas as pd

meliapi = MeliApi()

df = pd.read_csv(r'C:\Users\guilherme.aleixo\Documents\API Meli\data\category_id.csv')
products_list = df['data'].values.tolist()

for i in products_list:
    meliapi.open_mlm(i, option=3)
    time.sleep(1)
    meliapi.category_data(i)
