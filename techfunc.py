import logging  # Выводим лог на консоль и в файл
import sys  # Выход из точки входа
from datetime import datetime  # Дата и время
from QuikPy import QuikPy


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


#subscribe_to_candles



if __name__=="__main__":
    pass