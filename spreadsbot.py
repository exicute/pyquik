import numpy as np
import pandas as pd 
import requests

from mexc_api.spot import Spot
from mexc_api.websocket import SpotWebsocketStreamClient
from mexc_api.common.enums import Side, OrderType, StreamInterval, Action
from mexc_api.common.exceptions import MexcAPIError


class mexcspreadbot():
    '''
    1) Определить bid и ask
    2) Расчитать разрыв между ними
    3) Определить где выставить заявку на покупку и продажу:
        Определить плотности (по количеству заявок в небольшом диапозоне)
    
    *отработать момент, если цена резко уходит
    *спуфферские плотности
    *учесть какое количество покупать и продавать, чтобы все заявки прошли

    Для поиска монет:
    1) Есть объемы последние несколько минут-часов
    2) Монета малоликвдиная
    3) Есть плотности и спрэд
    '''
    
    key = 'mx0vgltzOxKejJSn38'
    secret_key = '1c6eed2aca944aae956f7720b2696073'

    def __init__(self) -> None:
        pass

    def getdata():
        pass


if __name__=="__main__":

    spot = Spot(key, secret_key)
    symbol = spot.market.default_symbols()[0]
    exinfo = spot.market.exchange_info(symbol=symbol)

    print(exinfo)