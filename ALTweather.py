from ALTconnection import *

################# UTILS ######################
def _captilize_first_letter(s):
    """
    Capitilizes the first letter of each word in a given sentence.

    Parameters
    ----------
    s : str
        The sentence we want to capitalize.

    Returns
    -------
    s : str
        The modified sentence.
    """
    lst = [word[0].upper() + word[1:] for word in s.split()]
    s = " ".join(lst)
    return s

################# TIME #######################
_NULL_TIME = '00:00'
_NULL_DATE_TIME = '01 Jan 00:00'

def _get_month(month):
    """
    Returns the appropriate 3 letters of a given number of a month.

    Parameters
    ----------
    month : int
        A number between 1-12.

    Returns
    -------
    : str
        3 letters describing a month if 'month' is between 1-12 and None otherwise.
    """
    dictionary = {1 : 'Jan', 2 : 'Feb', 3 : 'Mar', 4:'Apr', 5:'May', 6:'Jun',
                  7 : 'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12: 'Dec'}
    return dictionary.get(month, None)

def _add_left_zero(s):
    """
    Adds '0' to the left of a string.

    Parameters
    ----------
    s : str
        The string we want to modify.

    Returns
    -------
    : str
        The string with a '0' concatentated to its left.
    """
    if len(s) == 1:
        return '0' + s
    else:
        return s

# Fetches the exact time from host: time.google.com
def fetch_time(timezone = 3, host = 'time.google.com'):
    """
    Fetches the time from a given host.

    Parameters
    ----------
    timezone : int
        The timezone wanted.
    host : str
        The host ntp server used.

    Returns
    -------
    : str
        The string of the current time.
        The format of the output is : XX:XX.
        Where X is a digit.
    """
    try:
        check_connection()
    except Exception as e:
        return _NULL_TIME
    rtc.settime('ntp', host=host, tzone=3)
    time_info = rtc.datetime()
    return str(time_info[4]) + str(":") + str(time_info[5])

def fetch_date_time(timezone = 3, host = 'time.google.com'):
    """
    Fetches the time and date from a given host.

    Parameters
    ----------
    timezone : int
        The timezone wanted.
    host : str
        The host ntp server used.

    Returns
    -------
    : str
        The string of the current time and date.
        The format of the output is : XX LLL XX:XX.
        Where X is a digit and LLL are the three letters that define a month.
    """
    try:
        check_connection()
    except Exception as e:
        return _NULL_DATE_TIME
    rtc.settime('ntp', host=host, tzone=3)
    time_info = rtc.datetime()
    res = _add_left_zero(str(time_info[2])) + str(' ') + _get_month(time_info[1]) + str(' ') + _add_left_zero(str(time_info[4])) + str(":") + _add_left_zero(str(time_info[5]))
    return res

import urequests
import ujson

################# WEATHER FROM API #######################
# Fetches weather from: https://openweathermap.org

def _get_curr_ip():
    """
    Returns
    -------
    ip : str
        The current device's IP address.
        
    """
    ip = urequests.get('https://api.ipify.org').content.decode('utf8')
    return ip

def _get_lat_long_from_curr_ip():
    """
    Returns
    -------
    latlong : str list
        A list that contains the current longtitude and latitude of the device,
        according to the device's IP address.
        The format: ['latitude', 'longtitude']
        
    """
    ip = _get_curr_ip()
    latlong = urequests.get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
    return latlong

def _get_city_from_curr_ip():
    """
    Returns
    -------
    city : str
        The city according to the device's IP address.
        
    """
    ip = _get_curr_ip()
    city = urequests.get('https://ipapi.co/{}/city/'.format(ip)).text
    return city

def _parse_units(units):
    """
    In the site we fetch the weather from, the dictionary is:
    'standard' = 'Kelvin'
    'imperial' = 'Fahrenheit'
    'metric' = 'Celsius'
    
    Parameters
    -------
    units
        units are either {K, C, F}
    
    Returns
    -------
    : str
        the appropriate units string to be used in the site
        
    """
    dictionary = {'K' : 'standard', 'C' : 'metric', 'F' : 'imperial'}
    return dictionary.get(units, None)
    
    

def _get_weather_json_from_api(apikey, units_string):
    """
    Gets all weather information from API in JSON format.
    
    Parameters
    -------
    apikey
        The API key which the user gets after creating an account in https://openweathermap.org.
    units_string
        The temperature units. Could be either K,C,F
    
    Returns
    -------
    json data : JSON 
        All the needed weather in JSON format.
        
    Raises
    -------
        Exception in case of failure in retrieving JSON data.
        
    """
    check_connection()
    latlong = _get_lat_long_from_curr_ip()
    req = urequests.get('https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric&cnt=1'
                        .format(latlong[0], latlong[1], apikey)).text
    try:
        json_data = ujson.loads((req))
    except Exception as e:
        raise Exception(__name__ + ': Error fetching info from API')
    return json_data

def _fetch_icon_url_from_id(icon_id):
    """
    Parameters
    -------
    icon_id : int
        The ID of the weather icon.
        
        
    Returns
    -------
    A full url of a weather icon.
    The format: https://openweathermap.org/img/wn/{id}@2x.png
    
    """
    return 'https://openweathermap.org/img/wn/{}@2x.png'.format(icon_id)

def fetch_local_weather_from_api(apikey, units):
    """
    Parameters
    -------
    apikey
        The API key which the user gets after creating an account in https://openweathermap.org.
    units_string
        The temperature units. Could be either K,C,F
    
    Returns
    -------
    A dictionary that contains:
    [city, date, pressure (hPa units), temperature, humidity (%), wind speed (if imperial: miles/hour else meter/second), discription, icon-id]
    Note: The API doesn't return uv-index, therefore the value is always 'N/A'.
    With valid values, and in case of failure in retrieving the information, a dictionary with 'N/A' values will be returned. 
    
    """
    units_string = _parse_units(units)
    if units_string is None:
        raise Exception(__name__ + ': Units must either be : K, F, C')
    try:
        json_data = _get_weather_json_from_api(apikey, units)
    except Exception as e:
        return {'city' : 'N/A', 'date' : 'N/A', 'pressure' : 'N/A', 'temperature' : 'N/A',
            'humidity' : 'N/A', 'wind' : 'N/A', 'description' : 'N/A', 'icon-url' : 'res/error.png',
            'uv-index' : 'N/A', 'error-msg' : str(e)}
    return {'city' : json_data["city"]["name"], 'date' : str(json_data["list"][0]["dt_txt"]),
            'pressure' : str(json_data["list"][0]["main"]["pressure"]), 'temperature' : str(round(json_data["list"][0]["main"]["temp"])),
            'humidity' : str(json_data["list"][0]["main"]["humidity"]), 'wind' : str(json_data["list"][0]["wind"]["speed"]),
            'description' : _captilize_first_letter(json_data["list"][0]["weather"][0]["description"]), 'icon-url' : _fetch_icon_url_from_id(json_data["list"][0]["weather"][0]["icon"]),
            'uv-index' : 'N/A', 'error-msg' : ''}



################# WEATHER FROM wttr.in #######################
# Fetches the weather from : https://wttr.in/{city}

def _get_weather_json_from_web(city):
    """
    Gets all weather information from API in JSON format.
    
    Parameters
    -------
    city
        The city of which we want to get the weather information.
    
    Returns
    -------
    json data : JSON 
        All the needed weather of the city in JSON format.
        
    Raises
    -------
        Exception in case of failure in retrieving JSON data.
        
    """
    # Spaces are replaced by '+' to make the url legal according to the websites' rules.
    city_m = city.replace(' ', '+')
    req_text = urequests.get("https://wttr.in/{}?format=j2".format(city_m)).text
    try:
        json_data = ujson.loads((req_text))
    except Exception as e:
        raise Exception(__name__ + ": https://wttr.in is currently down, can't fetch weather data.")
    return json_data

def _get_temp_id(units):
    """
    In the wesite we fetch the weather from, the dictionary is:
    'temp_C' = 'Celsius'
    'temp_F' = 'Fahrenheit'
    
    Parameters
    -------
    units
        units are either {C, F}
    
    Returns
    -------
    : str
        the appropriate units string to be used in the website
        
    """
    dictionary = {'C' : 'temp_C', 'F' : 'temp_F'}
    return dictionary.get(units, None)

# TODO: Implement this function, need to check all possible descriptions and maybe create a dictionary!
def _fetch_icon_url_from_desc(desc):
    return None

# TODO: Function is kinda slow, because json is too big.. try and make it faster!
def fetch_local_weather_from_web(units):
    """
    Parameters
    -------
    units
        The temperature units. Could be either C,F.
    
    Returns
    -------
    A dictionary that contains:
    [city, date, pressure (hPa units), temperature, humidity (%), wind speed (meter/second), description, icon-id] 
    With valid values, and in case of failure in retrieving the information, a dictionary with 'N/A' values will be returned. 
    
    """
    temp_id = _get_temp_id(units)
    if temp_id is None:
        raise Exception(__name__ + ': Units must either be : F, C')
    try:
        check_connection()
        city = _get_city_from_curr_ip()
        json_data = _get_weather_json_from_web(city)
    except Exception as e:
        return {'city' : 'N/A', 'date' : 'N/A', 'pressure' : 'N/A', 'temperature' : 'N/A',
            'humidity' : 'N/A', 'wind' : 'N/A', 'description' : 'N/A', 'icon-url' : 'res/error.png',
            'uv-index' : 'N/A', 'error-msg' : str(e)}
    weather = json_data['weather'][0]
    json_data = json_data['current_condition'][0]
    return {'city' : city, 'date' : json_data["localObsDateTime"],
            'pressure' : str(json_data["pressure"]), 'temperature' : str(json_data[temp_id]),
            'humidity' : str(json_data["humidity"]), 'wind' : str(round(float(json_data["windspeedKmph"])*0.277778, 2)),
            'description' : _captilize_first_letter(json_data["weatherDesc"][0]["value"]), 'icon-url' : _fetch_icon_url_from_desc(json_data["weatherIconUrl"][0]["value"]),
            'uv-index' : str(weather["uvIndex"]), 'error-msg' : ''}
    