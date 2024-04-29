import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

data = [] #dictonary
n = 0

driver = webdriver.Chrome()
driver.get("https://www.magicbricks.com/property-for-sale/residential-commercial-agricultural-real-estate?bedroom=1,2,3,4,5,%3E5&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Warehouse-Godown,Industrial-Building,Industrial-Shed,Agricultural-Land&Locality=Adajan&cityName=Surat")
time.sleep(10)

def property_details(single_property, property_dict):
    try:
        property_summary = single_property.find_element(By.CLASS_NAME, "mb-srp__card__summary__list")
        property_lables = property_summary.find_elements(By.CLASS_NAME, "mb-srp__card__summary--label")
        property_values = property_summary.find_elements(By.CLASS_NAME, "mb-srp__card__summary--value")
    # print(len(property_lables), len(property_values))
        for e in range(len(property_lables)):
            p_lable = property_lables[e].text
            p_value = property_values[e].text
            property_dict[p_lable] = p_value
    
    except Exception as e:
        print("property_details:")
        
properties_div = driver.find_elements(By.CLASS_NAME, "mb-srp__card")

for element in properties_div:
    property_dict = {}
    try:
        property_dict["property_name"] = element.find_element(By.CLASS_NAME, "mb-srp__card--title").text
    except Exception as e:
        print("name")
    try:
        property_dict["property_price"] = element.find_element(By.CLASS_NAME, "mb-srp__card__price").text.strip().split('\n')[1]
    except Exception as e:
        print("price")
    try:
        property_dict["property_area"] = element.find_element(By.CLASS_NAME, "mb-srp__card__summary--value").text
    except Exception as e:
        print("area")
    try:
        property_dict["property_status"] = element.find_element(By.CLASS_NAME, "mb-srp__card__summary--value").text
    except Exception as e:
        print("status")
    property_details(element, property_dict)
    print(property_dict)
    data.append(property_dict)
    n += 1
    if n == 10:
        break



file = open("Properties.json", 'a')
file.write(json.dumps(data))
file.close()