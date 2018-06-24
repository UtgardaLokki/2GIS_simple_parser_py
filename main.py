# Parser of 2GIS that takes list of addresses and converts it to geo coordinates

from selenium import webdriver
import pandas as pd
from time import sleep
import constant

# Setting Chrome webdriver
chrome_driver = constant.chrome_driver_path
option = webdriver.ChromeOptions()
option.add_argument(constant.chrome_profile_path)
driver = webdriver.Chrome(chrome_driver, chrome_options=option)

url_2gis = "https://2gis.com.cy/cyprus"  # url if 2GIS

coordinate_dict = {}

# Reading Billing address report
df = pd.read_excel(constant.addr_df_path)

# Adding columns with a clean address that needs to be typed in search input
df["full_address"] = df['Улица'].astype(str) + ', ' + df['Дом'].astype(str)
df['address'] = df['full_address'].str.split('(', expand=True)

# Setting variables for webdriver
input_addr = driver.find_element_by_css_selector('#module-1-3-1 > div > input')
search_button = driver.find_element_by_css_selector("#module-1-3 > div.searchBar__forms >\
                                                     div > form > button.searchBar__submit._directory")

driver.get(url_2gis) # Open 2GIS site

def get_coordinates(address, bill, zip_code_d):
    input_addr.send_keys(address)
    search_button.click()
    cur_url = driver.current_url
    if "/geo/" in cur_url:
        coordinates = [i[1:] for i in cur_url.split("center")[1].split("%2")[1:3]]
        coordinate_dict[bill] = coordinates
    else:
        links = driver.find_elements_by_class_name('miniCard__headerTitleLink')
        for link in links:
            link.click()
            zip_code = driver.find_element_by_class_name('_purpose_drilldown').text.split(', ')[-1]
            if zip_code_d == zip_code:
                driver.find_element_by_class_name('card__addressLink').click()
                coordinates = [i[1:] for i in cur_url.split("center")[1].split("%   2")[1:3]]
                if coordinate_dict.get(bill) is None:
                    coordinate_dict[bill] = coordinates
                else:
                    dict[bill].append(coor)
                driver.back()
                driver.back()
                break
            else:
                driver.back()

get_coordinates(address="tzon kennenty 10", bill="BILL0000423", zip_code_d="3106")

