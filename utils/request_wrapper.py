from fake_useragent import UserAgent
import requests
from utils.configs import get_config

def make_request(celular: str, token: str):
    BASE_URL = get_config("SALDOS", "CONSULT_URL")
    url = "{}?linea={}".format(BASE_URL, celular)
    ua = UserAgent(browsers=["edge", "chrome", "firefox", "opera"])

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization': 'Bearer {}'.format(token),
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'https://paymentservice.mitelcel.com/v2/billing/data/fact-balancer?channelCode=2&channelDetail=11&channelSource=WEB',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': ua.random,
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, headers=headers)
    print(response.text)
    try:
        json_resp = response.json()
        return json_resp
        #return response.status_code, response.json()
    except Exception as ex:
        print("Ha ocurrido una excepcion al tratar de obtener los datos: {}".format(str(ex)))
        return 500, response.text

