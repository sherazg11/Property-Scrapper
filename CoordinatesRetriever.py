import requests
import json

def get_coordinates(address):

    response = requests.get('https://www.google.com/search?tbm=map&authuser=0&hl=en&q=' + address)
    
    json_response = json.loads(response.text[4:])

    coordinates_part = json_response[0][1][0][14][9]

    coordinates = str(coordinates_part[2]) + "," + str(coordinates_part[3])

    return coordinates