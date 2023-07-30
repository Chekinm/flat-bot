from requests import get
import json


async def get_yad2_data(request_params) -> dict:
    """make an api request to yad2 using request_params dict
    get back a dictionary with desired flats
    we need a link a number of room and photos urls list for a POC prototype
    """

    # some parameters are still hardcoded, need testing which one should be
    # tuned by users

    payload = {
            'cat': "2",
            'subcat': "2",
            'price': "1000-27000",  # will add price selection in next release
            'airConditioner': "1",  # don't think anybody need a flat whitout:)
            'balcony': f"{int(request_params[5])}",
            'longTerm': "1",
            'squaremeter': f"{request_params[6]}-{request_params[7]}",
            'z': "14",   # don't know what it means
            'center_point[]': f"{request_params[2]},{request_params[3]}",
            'distance[]': f"{request_params[4]}",
            'isMapView': '1',
            'page': '1',
        }

    print(payload)
    try:
        yad2_response = get('https://www.yad2.co.il/api/feed/get',
                            params=payload,
                            )
        if yad2_response.status_code == 200:
            print('yad2 is responding')
            yad2_response_dict = json.loads(yad2_response.content)
            # this json.loads will generate an exeption we will hanlde below
            # in case is yad2 will try to send us captha
        else:
            print('We are exireincing an unknown porblem with yad2 servers'
                  'Get to user a Rishon json instead.')
            with open('json_data.json', 'r') as data_file:
                yad2_response_dict = json.load(data_file)
    except json.JSONDecodeError as e:
        print(e,
              '\n',
              'Looks like yad2 banned us again by IP.',
              'Send to user a defult RishonLezion json instead.')
        with open('json_data.json', 'r') as data_file:
            yad2_response_dict = json.load(data_file)

    return yad2_response_dict
