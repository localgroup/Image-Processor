import requests
from image_processor import processor
import pandas as pd


def get_hex_code():
    """
    Returns the hex value and the name of the rgb values through an API call!
    :return:
    """
    file_path = processor.open_file() 

    if file_path:
        print('Please wait, the image is being processed...')
        rgb_values = processor.detect_color(file_location=file_path)
        color_response = []

        for rgb_value in rgb_values:
            if rgb_value:
                url = f'https://www.thecolorapi.com/id?rgb={rgb_value}'
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    hex_value = data['hex']['value']
                    name = data['name']['value']
                    color_response.append({'Hex': hex_value, 'Name': name})

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching hex code: {e}")
            else:
                print('Failed to detect color.')

        df = pd.DataFrame(color_response)
        print(df.head(20))

    else:
        print('No file selected.')


get_hex_code()
