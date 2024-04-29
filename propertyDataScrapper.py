import csv
import requests
from bs4 import BeautifulSoup
from CoordinatesRetriever import get_coordinates

data = [] #dictonary
n = 0

response = requests.get("https://www.magicbricks.com/property-for-sale/residential-commercial-agricultural-real-estate?bedroom=1,2,3,4,5,%3E5&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Warehouse-Godown,Industrial-Building,Industrial-Shed,Agricultural-Land&Locality=Adajan&cityName=Surat")

soup = BeautifulSoup(response.text, 'html.parser')

property_labels = set()

property_labels.add('Name')

property_labels.add('Price')

property_labels.add('Address')

property_labels.add('Coordinates')

def property_details(single_property, property_dict):

    try:
    
        property_summary = single_property.find('div',{'class': 'mb-srp_card_summary'})

        property_lables = property_summary.find_all('div', {'class':'mb-srp_card_summary--label'})
        property_values = property_summary.find_all('div', {'class': 'mb-srp_card_summary--value'})
    
    
        for e in range(len(property_lables)):
    
            p_lable = property_lables[e].text.capitalize()
            p_value = property_values[e].text
            property_dict[p_lable] = p_value
            property_labels.add(p_lable)
    
    except Exception as e:
        print(e)
        
properties_div = soup.find_all('div', {'class': 'mb-srp__card'})

for element in properties_div:

    property_dict = {}
    
    try:
        property_dict["Name"] = element.find('h2', {'class':'mb-srp__card--title'}).text
    except Exception as e:
        print("name")
    
    try:
        property_dict["Price"] = element.find('div',{'class': 'mb-srp_card_price--amount'}).text.strip()[1:]
    except Exception as e:
        print("price")

    try:
        property_dict["Address"] = property_dict["Name"].split("for Sale in ")[-1] + ", India"
    except Exception as e:
        print('Address')

    try:
        property_dict["Coordinates"] = get_coordinates(property_dict["Address"])
    except Exception as e:
        print("Coordinates")
        
    property_details(element, property_dict)
    
    data.append(property_dict)
    
    n += 1
    if n == 10:
        break

# Filling missing values in property dicts so that each property dict have same number of values
# which will allows us to store data in csv with same number of columns preventing any errors

for property_dict in data:

    property_dict_labels = set(property_dict.keys())

    remaaining_lables = property_labels - property_dict_labels

    for r_label in remaaining_lables:

        property_dict[r_label] = '' # Filling with empty value

# Storing data in csv

with open('Properties.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    for row in data:
        writer.writerow(row)