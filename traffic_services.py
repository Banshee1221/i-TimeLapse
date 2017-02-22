import requests
import json
import xmltodict

class fetcher:

    GP = {}
    WC = {}
    KZN = {}
    provinces = {"GP": GP, "WC": WC, "KZN": KZN}

    def __init__(self):

        fetcher.GP['ID'] = 'GP'
        fetcher.WC['ID'] = 'WC'
        fetcher.KZN['ID'] = 'KZN'

        data = {
            "token": "",
            "minLat": 0,
            "minLng": 0,
            "latSpan": 0,
            "lngSpan": 0,
            "fetchedIDs": ""
        }

        req = requests.post('https://www.i-traffic.co.za/MapService.asmx/GetCameras', data=data)
        jsonConv = json.loads(json.dumps(xmltodict.parse(str(req._content))))
        payload = jsonConv["ServiceResponseOfOverlayPayload"]["Payload"]["AddOverlays"]["Overlay"]

        counterGP, counterWC, counterKZN = 0, 0, 0
        for camera in payload:
            if "gp$" in camera['ID']:
                fetcher.GP[counterGP] = dict({'Name': camera['Title'], 'URL': camera['TooltipUrl'].split('&')[2].split('=')[1]})
                counterGP += 1
            if "wc$" in camera['ID']:
                fetcher.WC[counterWC] = dict({'Name': camera['Title'], 'URL': camera['TooltipUrl'].split('&')[2].split('=')[1]})
                counterWC += 1
            if "kzn$" in camera['ID']:
                fetcher.KZN[counterKZN] = dict({'Name': camera['Title'], 'URL': camera['TooltipUrl'].split('&')[2].split('=')[1]})
                counterKZN += 1

    def getList(self):
        for key, val in fetcher.provinces.items():
            print "======== "+val['ID']+" ========\n" + json.dumps(val, indent=2)
            print "================================="


    def callImage(self, region, num):
        if region is not ("WC" or "GP" or "KZN"):
            return -1

        print "ID: ",fetcher.provinces[region]['ID']
        print "Name: ",fetcher.provinces[region][num]['Name']
        print "URL: ",fetcher.provinces[region][num]['URL']

        url_static = "https://www.i-traffic.co.za/CctvImageHandler.ashx?"
        url_dynamic = "networkId=" + fetcher.provinces[region]['ID'] + "&deviceId=" + fetcher.provinces[region][num]['URL']
        URL = url_static+url_dynamic
        return URL

    def __writer(self, outFile, dictionary):
        id = dictionary['ID']
        for numbers in dictionary:
            if numbers is "ID":
                continue
            name = dictionary[numbers]['Name']
            url = dictionary[numbers]['URL']
            toWrite = id + "," + name + "," + url + "\n"
            outFile.write(toWrite)

"""
        dataFile = open('camData.csv', "wb")
        dataFile.write("REGION,TITLE,URL\n")
        self.__writer(dataFile, fetcher.GP)
        self.__writer(dataFile, fetcher.KZN)
        self.__writer(dataFile, fetcher.WC)
"""




