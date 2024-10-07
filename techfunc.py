import logging  # Выводим лог на консоль и в файл
import sys  # Выход из точки входа
from datetime import datetime  # Дата и время
from QuikPy import QuikPy
import pandas as pd
import numpy as np


#connecting 
def connectquik():
    logger = logging.getLogger('QuikPy.Connect')  # Будем вести лог
    qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK по портам по умолчанию
    # qp_provider = QuikPy(host='<Адрес IP>')  # Подключение к удаленному QUIK по портам по умолчанию
    # qp_provider = QuikPy(host='<Адрес IP>', requests_port='<Порт запросов>', callbacks_port='<Порт подписок>')  # Подключение к удаленному QUIK по другим портам

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                        datefmt='%d.%m.%Y %H:%M:%S',  # Формат даты
                        level=logging.DEBUG,  # Уровень логируемых событий NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
                        handlers=[logging.FileHandler('Connect.log'), logging.StreamHandler()])  # Лог записываем в файл и выводим на консоль
    logging.Formatter.converter = lambda *args: datetime.now(tz=qp_provider.tz_msk).timetuple()  # В логе время указываем по МСК

    # Проверяем соединение с терминалом QUIK
    is_connected = qp_provider.is_connected()['data']  # Состояние подключения терминала к серверу QUIK
    logger.info(f'Терминал QUIK подключен к серверу: {is_connected == 1}')
    logger.info(f'Отклик QUIK на команду Ping: {qp_provider.ping()["data"]}')  # Проверка работы скрипта QuikSharp. Должен вернуть Pong
    msg = 'Hello from Python!'
    logger.info(f'Отправка сообщения в QUIK: {msg}{qp_provider.message_info(msg)["data"]}')  # Проверка работы QUIK. Сообщение в QUIK должно показаться как информационное
    if is_connected == 0:  # Если нет подключения терминала QUIK к серверу
        qp_provider.close_connection_and_thread()  # Перед выходом закрываем соединение для запросов и поток обработки функций обратного вызова
        sys.exit()  # Выходим, дальше не продолжаем

    return qp_provider


def collectdatequik(df: pd.DataFrame) -> pd.DataFrame:
    df = pd.json_normalize(df['data'])
    
    keyslist = []
    for col in df.columns:
        if col.split('.')[0] == 'datetime':
            keyslist.append(col)

    for col in keyslist:
        df[col] = df[col].astype(str)

    df['date'] = df['datetime.year']+'-' \
        +df['datetime.month']+'-' \
        +df['datetime.day']+' ' \
        +df['datetime.hour']+':' \
        +df['datetime.min']+':' \
        +df['datetime.sec']
    df['date'] = pd.to_datetime(df['date'])

    df = df.drop(columns=keyslist)

    return df


def getvar(df: pd.DataFrame) -> pd.DataFrame:
    df['frameyield'] = (df.loc[:, 'open'] - df.loc[:, 'close'])/df.loc[:, 'open']
    df['framevar'] = (df.loc[:, 'high'] - df.loc[:, 'low'])/df.loc[:, 'close']

    return df


def calcspread(assetval:float, rate:float, expirdate:str, dividend:float=0, futval:float=0, lotsize:float=10):
    maturity = pd.to_datetime(expirdate)-pd.to_datetime('today').normalize()
    maturity = int(maturity.days)

    assetval = assetval*lotsize
    dividend = dividend*lotsize

    F0 = assetval*(1+rate*(maturity/365)-dividend/assetval)

    if futval==None:
        return F0
    
    else:
        return (F0, futval-F0)



if __name__=="__main__":
    pass