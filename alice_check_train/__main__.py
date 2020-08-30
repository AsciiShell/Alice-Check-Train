import datetime
import os

from alice_check_train.main import rasp_to_text
from alice_check_train.rasp_api import get_rasp, filter_rasp


def main():
    key = os.getenv('RASP_KEY')
    station_from = os.getenv('STATION_FROM')
    station_to = os.getenv('STATION_TO')
    date = datetime.date.today().strftime('%Y-%m-%d')

    js = get_rasp(key, station_from, station_to, date)
    filtered = filter_rasp(js['segments'], 60)
    message = rasp_to_text(filtered)
    print(message)


if __name__ == '__main__':
    main()
