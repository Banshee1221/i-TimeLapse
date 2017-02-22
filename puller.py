import requests
import json
import xmltodict
import webbrowser

GP = {}
WC = {}
KZN = {}

GP['ID'] = 'GP'
WC['ID'] = 'WC'
KZN['ID'] = 'KZN'

data = {
    "token": "",
    "minLat": 0,
    "minLng": 0,
    "latSpan": 0,
    "lngSpan": 0,
    "fetchedIDs": ""
}

r = requests.post('https://www.i-traffic.co.za/MapService.asmx/GetCameras', data=data)

soup = str(r._content)
print soup
jsonConv = json.loads(json.dumps(xmltodict.parse(soup)))
payload = jsonConv["ServiceResponseOfOverlayPayload"]["Payload"]["AddOverlays"]["Overlay"]

counterGP, counterWC, counterKZN = 0, 0, 0
for camera in payload:
    if "gp$" in camera['ID']:
        GP[counterGP] = dict({'Name': camera['Title'], 'URL': camera['TooltipUrl'].split('&')[2].split('=')[1]})
        counterGP += 1
    if "wc$" in camera['ID']:
        WC[counterWC] = dict({'Name': camera['Title'], 'URL': camera['TooltipUrl'].split('&')[2].split('=')[1]})
        counterWC += 1
    if "kzn$" in camera['ID']:
        KZN[counterKZN] = dict({'Name': camera['Title'], 'URL': camera['TooltipUrl'].split('&')[2].split('=')[1]})
        counterKZN += 1

#URL = "https://www.i-traffic.co.za/CctvImageHandler.ashx?networkId="+GP['ID']+"&deviceId="+GP[50]['URL']
#webbrowser.open(URL)