import datetime
import logging
import os
import traceback

from alice_check_train.rasp_api import get_rasp, filter_rasp, RaspException
from alice_check_train.true_answer import rasp_to_text

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_config():
    key = os.getenv('RASP_KEY')
    station_from = os.getenv('STATION_FROM')
    station_to = os.getenv('STATION_TO')
    date = datetime.date.today().strftime('%Y-%m-%d')
    return key, station_from, station_to, date


def main_handler(event, context):
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'end_session': 'true'
        },
    }
    try:
        response = handler(event, context)
    except RaspException:
        response['response']['text'] = 'Ошибка подключения к Яндекс.Расписанию. Попробуйте позже'
        logger.warning('Ya rasp:\r%s\rRequest:\r%s\rResponse:\r%s\r', repr(traceback.format_exc()), repr(event),
                       repr(response))
    except Exception:  # pylint: disable=broad-except
        response['response']['text'] = 'Неизвестная ошибка'
        logger.error('Handler error:\r%s\rRequest:\r%s\rResponse:\r%s\r', repr(traceback.format_exc()), repr(event),
                     repr(response))
    else:
        logger.info('Good:\r\rRequest:\r%s\rResponse:\r%s\r', repr(event), repr(response))
    return response


def check_intent(req, key):
    return req.get('request', {}).get('nlu', {}).get('intents', {}).get(key)


# pylint: disable=W0613
def handler(event: dict, context: dict):
    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'end_session': 'false'
        },
    }
    if check_intent(event, 'YANDEX.HELP') or check_intent(event, 'YANDEX.WHAT_CAN_YOU_DO'):
        response['response']['text'] = 'Привет! Я могу проверить расписание электричек'
        return response

    key, station_from, station_to, date = get_config()
    js = get_rasp(key, station_from, station_to, date)
    filtered = filter_rasp(js['segments'], 60)
    response['response']['text'] = rasp_to_text(filtered)
    return response
