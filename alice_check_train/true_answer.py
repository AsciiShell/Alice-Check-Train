import random


class InvalidNumberException(Exception):
    pass


_NUMBERS_TO_STR = {0: '', 1: 'одну', 2: 'две', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь',
                   9: 'девять', 10: 'десять', 11: 'одиннадцать', 12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать',
                   15: 'пятнадцать', 16: 'шестнадцать', 17: 'семнадцать', 18: 'восемнадцать', 19: 'девятнадцать'}


def number_to_string(number):
    if number < 20:
        return _NUMBERS_TO_STR[number]
    digit = _NUMBERS_TO_STR[number % 10]
    if 19 < number < 30:
        return 'двадцать ' + digit
    if 29 < number < 40:
        return 'тридцать ' + digit
    if 39 < number < 50:
        return 'сорок ' + digit
    if 49 < number < 60:
        return 'пятьдесят ' + digit
    raise InvalidNumberException('the number must be lower than 60, your number is: {}'.format(number))


def build_message_minutes(minutes: int, use_hours: bool):
    digit = minutes % 10
    if minutes == 0:
        if use_hours:
            return ''  # 180 -> Через 3 часа
        return 'прямо сейчас'
    if 10 < minutes < 20 or digit == 0 or digit > 4:
        minutes_word = 'минут'
    elif digit == 1:
        minutes_word = 'минуту'
    else:  # 1 < digit < 5:
        minutes_word = 'минуты'
    return '{} {} {}'.format('' if use_hours else 'через', number_to_string(minutes), minutes_word)


def build_message_hours(minutes):
    hours = minutes // 60
    hours_digit = hours % 10
    if hours == 0:
        return build_message_minutes(minutes, False)
    if 10 < hours < 20 or hours_digit == 0 or hours_digit > 4:
        hours_word = 'часов'
    elif hours_digit == 1:
        hours_word = 'час'
    else:  # 1 < hours_digit < 5:
        hours_word = 'часа'
    return 'через {} {} {}'.format(str(hours), hours_word, build_message_minutes(minutes % 60, True))


def rasp_to_text(data, max_rows=3) -> str:
    pretext = ['Затем', 'Далее', 'Вскоре после него', 'Следом', 'Потом', 'Еще один']
    random.shuffle(pretext)
    if len(data) == 0:
        return 'Нет отправлений в ближайший час.'
    result = 'Ближайший поезд отправляется {}.\n'.format(build_message_hours(data[0]['diff_minutes']))
    for text, row in zip(pretext, data[1:max_rows]):
        result += '{} {}.\n'.format(text, build_message_hours(row['diff_minutes']))
    return result
