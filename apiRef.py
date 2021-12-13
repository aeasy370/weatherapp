from genericpath import exists
import sys, os, requests, json, datetime
from statecode import getstatecode
import geocoder
# import grequests
from copy import deepcopy
from geopy.geocoders import Nominatim


def refresh(x):
    apikey = ''
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(x['lat'])
    url += '&lon=' + str(x['lon']) + '&exclude=minutely,alerts' + '&units=imperial'  + '&appid=' + apikey
    x['url'] = url
    response = requests.get(url)
    response = response.json()

    response = json.dumps(response)
    response = json.loads(response)

    x['hourly'] = response['hourly']
    x['weekly'] = response['daily']
    x['current'] = response['current']

    return x


def singleapiref(Info, city):
    x = getsinglecoords(city)
    if not x:
        return 0, 0
    apikey = '2901e1eca64d892114265c998c218830'
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(x['lat'])
    url += '&lon=' + str(x['lon']) + '&exclude=minutely,alerts' + '&units=imperial'  + '&appid=' + apikey
    response = requests.get(url)
    response = response.json()

    response = json.dumps(response)
    response = json.loads(response)

    x['current'] = response['current']
    x['hourly'] = response['hourly']
    x['weekly'] = response['daily']
    x['current'] = response['current']
    Info['Location'].insert(0, x)
    return Info, 1

def myapiref(citylist):
    apikey = ''
    #print('\n\n\n\n\n\n\n\n\n')
    #print(citylist)
    for x in citylist['Location']:
        #print(x)
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(x['lat'])
        url += '&lon=' + str(x['lon']) + '&exclude=minutely,alerts' + '&units=imperial'  + '&appid=' + apikey
        x['url'] = url
        response = requests.get(url)
        response = response.json()

        response = json.dumps(response)
        response = json.loads(response)
        x['current'] = response['current']
        x['hourly'] = response['hourly']
        x['weekly'] = response['daily']
        x['current'] = response['current']
    return citylist
    
    
def getsinglecoords(cityname):
    city = cityname.split()
    city[1] = getstatecode(city[1])
    #print(city[1])
    cityname = ''.join(city)
    ret = {
        'City': '',
        'State': '',
        'lat' : 0.0,
        'lon' : 0.0,
        'url' : '',
        'current': {},
        'hourly': {},
        'weekly': {}
    }
    http = 'http://api.openweathermap.org/geo/1.0/direct?q=' + cityname + '&appid=' + ''
    print(http)
    Newresponse = requests.get(http)
    if not Newresponse:
        return 0
    Newresponse = Newresponse.json()
    if Newresponse == []:
        return 0
    Newresponse = Newresponse[0]
    


# NEEDS TO INSERT TO A LIST


# print(Newresponse)
    
    ret['City'] = Newresponse['name']
    ret['State'] = Newresponse['state']
    ret['lat'] = Newresponse['lat']
    ret['lon'] = Newresponse['lon']
    ret['url'] = ''
    return ret
    
def getcoords(cityname):
    if cityname == 'Current Location':
        g = 0
        while not g:
            g = geocoder.ip('me')
        lat = g.latlng[0]
        lon = g.latlng[1]
        ret = dict()
        ret = {
            'City': 'Current Location',
            'State': '',
            'lat' : lat,
            'lon' : lon,
            'url' : '',
            'current': {},
            'hourly': {},
            'weekly': {}
        }
        return ret
    city = cityname.split()
    city[1] = getstatecode(city[1])
    #print(city[1])
    cityname = ''.join(city)
    l = []
    for _ in cityname:
        http = 'http://api.openweathermap.org/geo/1.0/direct?q=' + cityname['name'] \
                + '&appid=' + ''
        newresponse = requests.get(http)
        if not newresponse:
            return 0
        
        Newresponse = newresponse.json()
        Newresponse = Newresponse[0]


    # NEEDS TO INSERT TO A LIST


    # print(Newresponse)
        ret = {
            'name': Newresponse['name'],
            'lat': Newresponse['lat'],
            'lon': Newresponse['lon'],
            'url': ''
        }
        l.append(ret)
    return l

def getlocation(city):
    url = 'http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit={}&appid={}'.format(city['lat'], city['lon'], 1, '')
    response = requests.get(url)
    response = response.json()
    response = json.loads(json.dumps(response))
    response = response[0]
    city = response['name']
    state = response['state']
    return city + ', ' + state

def refresh_weather(city):
    # Onecall api call for hourly
    # jsonDict = myapiref(city)
    # # Write contents of new api call to api.json
    # with open(os.path.join(sys.path[0], 'api.json'), 'w') as f:
    #     json.dump(newresponse, f, indent=4 )
    return
    

def read_cache():
    if exists(os.path.join(sys.path[0],'data.json')) == False:
        data = {
            'Location': [],
            "settings": {
               "degrees": "farenheit",
                "windspeed": "mph",
                "language": "English"
            }
        }
        return data
    if os.stat(os.path.join(sys.path[0],'data.json')).st_size == 0:
        data = {
            'Location': [],
            "settings": {
               "degrees": "farenheit",
                "windspeed": "mph",
                "language": "English"
            }
        }
        return data
    with open(os.path.join(sys.path[0],'data.json')) as f:
        
        try:
            data = json.load(f)
            #print(data["Location"])
            if len(data["Location"]) == 0:
                data = {
                    'Location': [],
                    "settings": {
                        "degrees": "farenheit",
                        "windspeed": "mph",
                        "language": "English"
                    }
                }
                return data
        except:
            return data
    f.close()
    if data == False:
        data = {
            'Location': [],
            "settings": {
               "degrees": "farenheit",
                "windspeed": "mph",
                "language": "English"
            }
        }
    return data

def read_state():
    if exists(os.path.join(sys.path[0],'state.json')) == False:
        return False
    if os.stat(os.path.join(sys.path[0],'state.json')).st_size == 0:
        return False
    with open(os.path.join(sys.path[0],'state.json')) as f:
        try:
            data = json.load(f)
        except ValueError as e:
            return False
    f.close()
    return data

def write_cache(cityname):
    loc = dict()
    num = dict()
    data = dict()
    di = dict()
    di = {
        'degrees': 'farenheit',
        'windspeed': 'mph',
        'language': 'English'
    }
    data = {'Location': [], 'settings': di}
    #print(cityname)
    copy = {}
    copy = deepcopy(cityname)
    with open(os.path.join(sys.path[0],'data.json'), 'w') as f:
        end = len(copy['Location'])
        i = 0
        while i < end:
            if copy['Location'][i]['City'] == "Current Location":
                # swap last and current location
                temp = copy['Location'][i]
                copy['Location'][i] = copy['Location'][len(copy['Location']) - 1]
                copy['Location'][len(copy['Location']) - 1] = temp

                # delete last object
                copy['Location'].remove(copy['Location'][len(copy['Location']) - 1])
                end -= 1
            else:
                copy['Location'][i]['hourly'] = {}
                copy['Location'][i]['current'] = {}
                copy['Location'][i]['weekly'] = {}
                i += 1

        # print(json.dumps(copy, indent=4))
        json.dump(copy, f, indent=4)

def cache_weather():
    data = read_cache()
    data['Location'].append(getcoords('Current Location'))
    data = myapiref(data)


def hourlyapi(lat, lon, state):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={},alerts&appid='.format(lat,lon)
    jsonResponse = requests.get(url)
    jsonParse1 = jsonResponse.json()
    jsonDict = json.loads(json.dumps(jsonParse1))
    hourlyInfo = []
    i = 0
    hourlydict = jsonDict['hourly']
    #print(hourlydict)
    
    for j in hourlydict:
        temp = []
        temp.append(datetime.datetime.fromtimestamp(hourlydict[i]['dt']).strftime('%c'))
        if(state == 1):
            temp.append (round(((hourlydict[i]['temp'] - 273.15) * 9/5) + 32))
                
        else:
            temp.append (round(hourlydict[i]['temp'] - 273.15))
        
        temp.append(hourlydict[i]['weather'][0]['main'])
        hourlyInfo.append(temp)
        i = i + 1
    return hourlyInfo

def weeklyapi(lat,lon, state):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid='.format(lat,lon)
    jsonResponse = requests.get(url)
    jsonParse1 = jsonResponse.json()
    jsonDict = json.loads(json.dumps(jsonParse1))
    weeklyInfo = []
    i = 0
    weeklydict = jsonDict['daily']
    #print(hourlydict)
    
    for j in weeklydict:
        temp = []
        temp.append(datetime.datetime.fromtimestamp(j['dt']).strftime('%c'))
        if(state == 1):
            temp.append (round(((j['temp']['day'] - 273.15) * 9/5) + 32))
                
        else:
            temp.append (round((j['temp']['day']) - 273.15))
        
        temp.append(j['weather'][0]['main'])
        weeklyInfo.append(temp)
        i = i + 1
    return weeklyInfo
        
