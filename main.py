import datetime
import logging
import os
import traceback

from rasp_api import get_rasp, filter_rasp, RaspException

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _second_to_minutes_seconds(s):
    s = int(s)
    return s // 60, s % 60


def rasp_to_text(data) -> str:
    if len(data) == 0:
        return 'Нет ближайших поездов в ближайший час'
    result = 'Ближайший поезд отправляется через {} минут {} секунд.\n'.format(
        *_second_to_minutes_seconds(data[0]['diff'].total_seconds())
    )
    for row in data[1:]:
        result += 'Затем через {} минут.\n'.format(
            _second_to_minutes_seconds(row['diff'].total_seconds())[0]
        )
    return result


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
    except Exception as e:
        response['response']['text'] = 'Неизвестная ошибка'
        logger.error('Handler error:\r%s\rRequest:\r%s\rResponse:\r%s\r', repr(traceback.format_exc()), repr(event),
                     repr(response))
    else:
        logger.info('Good:\r\rRequest:\r%s\rResponse:\r%s\r', repr(event), repr(response))
    return response


def check_intent(req, key):
    try:
        return req['request']['nlu']['intents'][key]
    except KeyError:
        return None


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

    key = os.getenv('RASP_KEY')
    station_from = os.getenv('STATION_FROM')
    station_to = os.getenv('STATION_TO')

    date = datetime.date.today().strftime('%Y-%m-%d')
    js = get_rasp(key, station_from, station_to, date)
    filtered = filter_rasp(js['segments'], 60)
    response['response']['text'] = rasp_to_text(filtered)
    return response
