from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import re
import json
import time

class MeliApi:
    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        self.brs = webdriver.Chrome(executable_path=r"C:\Users\guilherme.aleixo\G.shop\chromedriver.exe", options=chrome_options)

    def open_mlm(self, n, option):

        driver = self.brs

        if option != 3:
            if 'click1' not in n and 'www' not in n:
                finder_1 = (n.find('-'))
                finder_2 = n.find('-', finder_1+1)
                finder_3 = (n.find('MLM'))
                n = n[int(finder_3):int(finder_2)]
                n = n.replace('-','')
        
            elif 'click1' in n:
                driver.get(n)
                n = driver.current_url
                finder_1 = (n.find('-'))
                finder_2 = n.find('-', finder_1+1)
                finder_3 = (n.find('MLM'))
                n = n[int(finder_3):int(finder_2)]
                n = n.replace('-','')

        if option == 2:
            driver.get(f'https://api.mercadolibre.com/items/{n}?include_attributes=all#json')

        elif option == 1:
            driver.get(n)

        elif option == 3:
            driver.get(f'https://api.mercadolibre.com/categories/{n}')

    def data_flow(output_file, title, price, sold_quantity, start_time, gtin, seller_id, category_id, product_link):

        data_ready = []

        table_description = { 'title': title, 'price': price, 'sold_quantity': sold_quantity, 'start_time':start_time, 'gtin':gtin, 'seller_id':seller_id, 'category_id':category_id, 'product_link':product_link}
        data_ready.append(table_description)
        df_table = pd.DataFrame(data_ready)
        df_table.drop_duplicates()
        df_table.to_csv(fr'C:\Users\guilherme.aleixo\Documents\API Meli\data\{output_file}.csv', mode='a', index=False, header=False)
        data_ready.clear()

    def sku_data(self, n):

        driver = self.brs

        output_file = 'output'

        expand = driver.find_element(By.XPATH, f'/html/body/div/div/section[1]/p/a[2]')
        expand.click()

        time.sleep(1)

        product_data = driver.find_element(By.XPATH, f'/html/body/div/div/section[1]/div').text

        regex_error = re.compile(r'"(?:\w+(?:\s+\w+)*|\w*?\d+\w*?|\w*?\d+\.?\d*\w*?)\s?"{2}(?!")')

        error = regex_error.findall(product_data)

        regex_error_2 = re.compile(r'"{3}')

        error_2 = regex_error_2.findall(product_data)

        if len(error_2) != 0:
            for i in error_2:
                product_data = product_data.replace(i,'"x"')

        if len(error) != 0:
            for i in error:
                product_data = product_data.replace(i,'"x"')

        try:
            sku = json.loads(product_data)
            
            try:
                title = sku['title']
            except:
                title = 'no_data'

            try:
                product_link = sku["id"]
            except:
                product_link = 'no_data'
                
            try:
                price = sku['price']
            except:
                price = 'no_data'

            try: 
                sold_quantity = sku['sold_quantity']
            except:
                sold_quantity = 'no_data'

            try:
                start_time = sku['start_time']
                finder_time = (start_time.find('T'))
                start_time = start_time[0:int(finder_time)]
            except:
                start_time = 'no_data'

            try:
                seller_id = sku['seller_id']
            except:
                seller_id = 'no_data'

            try:
                category_id = sku['category_id']
            except:
                category_id = 'no_data'
                
            value_name = ''

            try:
                for x in range(0,15):
                    for attribute in sku['variations'][x]['attributes']:
                        if attribute['id'] == 'GTIN':
                            value_name = attribute['value_name']
                        else:  
                            for attribute in sku['attributes']:
                                if attribute['id'] == 'GTIN':
                                    value_name = attribute['value_name']

            except:
                for attribute in sku['attributes']:
                    if attribute['id'] == 'GTIN':
                        value_name = attribute['value_name']

            MeliApi.data_flow(output_file, title, price, sold_quantity, start_time, value_name, seller_id, category_id, product_link)

        except:

            title = 'error'
            price = 'error'
            sold_quantity = 'error'
            start_time = 'error'
            seller_id = 'error'
            category_id = 'error'
            value_name = 'error'
            product_link = n

            MeliApi.data_flow(output_file, title, price, sold_quantity, start_time, value_name, seller_id, category_id, product_link)

    def category_data(self, n):

        driver = self.brs

        product_ref = n

        output_file = 'category_output'

        expand = driver.find_element(By.XPATH, f'/html/body/div/div/section[1]/p/a[2]')
        expand.click()

        time.sleep(1)

        category_data = driver.find_element(By.XPATH, f'/html/body/div/div/section[1]/div').text

        category = json.loads(category_data)

        print(category)

        x = 0

        for attribute in category['path_from_root']:

            x += 1

            if x == 1:
                category_1 = attribute['name']
            elif x == 2:
                category_2 = attribute['name']
            elif x == 3:
                category_3 = attribute['name']
            elif x == 4:
                category_4 = attribute['name']

        data_ready = []
        table_description = {'mlb_original':product_ref, 'category_1':category_1, 'category_2':category_2, 'category_3':category_3, 'category_4':category_4}
        data_ready.append(table_description)
        df_table = pd.DataFrame(data_ready)
        df_table.drop_duplicates()
        df_table.to_csv(fr'C:\Users\guilherme.aleixo\Documents\API Meli\data\{output_file}.csv', mode='a', index=False, header=False)
        data_ready.clear()













        


        



