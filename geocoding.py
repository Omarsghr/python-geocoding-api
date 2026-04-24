import urllib.request
import urllib.parse
import json
import ssl


def get_location_data(address):
    """
    Handles the API request logic for a given address string.
    Returns a dictionary of data or None if an error occurs.
    """
    serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    parms = dict()
    parms['q'] = address.strip()
    url = serviceurl + urllib.parse.urlencode(parms)

    print(f'Retrieving {url}')

    try:
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        js = json.loads(data)

        # Basic validation of the response
        if 'features' not in js or len(js['features']) == 0:
            return None
        return js
    except Exception as e:
        print(f"Error connecting to service: {e}")
        return None


def main():
    """
    Handles the user input loop and displays the results.
    """
    while True:
        address = input('Enter location (or press Enter to quit): ')
        if len(address) < 1:
            break

        js = get_location_data(address)

        if not js:
            print('==== Download error or object not found ====')
            continue

        # Extracting details from the first feature
        feature = js['features'][0]
        props = feature['properties']

        plus_code = props.get('plus_code', 'N/A')
        lat = props.get('lat')
        lon = props.get('lon')
        formatted_address = props.get('formatted')

        print(f'plus_code: {plus_code}')
        print(f'Latitude: {lat}, Longitude: {lon}')
        print(f'Location: {formatted_address}\n')


if __name__ == "__main__":
    main()
