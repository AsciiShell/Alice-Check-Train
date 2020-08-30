import random


class InvalidNumberException(Exception):
    pass


nouns_to_str = {0: '', 1: 'одну', 2: 'две', 3: 'три', 4: 'четыре', 5: 'пять',
                6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять', 10: 'десять',
                11: 'одинадцать', 12: 'двенадцать', 13: 'тринадцать',
                14: 'четырнадцать', 15: 'пятнадцать', 16: 'шестнадцать',
                17: 'семнадцать', 18: 'восемнадцать', 19: 'девятнадцать'}


# pylint: disable=R0911,R0912
def first_req(noun):
    if 0 <= noun <= 9:
        return nouns_to_str[noun]
    raise InvalidNumberException(
        'wrong number is entered: {}'.format(noun))


# pylint: disable=R0911,R0912
def word_return(noun):
    if noun < 10:
        return first_req(noun)
    if 9 < noun < 20:
        return nouns_to_str[noun]
    if 19 < noun < 30:
        return 'двадцать ' + first_req(noun % 10)
    if 29 < noun < 40:
        return 'тридцать ' + first_req(noun % 10)
    if 39 < noun < 50:
        return 'сорок ' + first_req(noun % 10)
    if 49 < noun < 60:
        return 'пятьдесят ' + first_req(noun % 10)
    raise InvalidNumberException(
        'the number must be lower than 60, your number is: {}'.format(noun))


def build_message_minutes(noun, hours):
    s = noun % 10
    pretext = ''
    # если поезд отправляется < чем через час, то pretext = через,
    # для корректной речи алисы
    if noun == 0:
        if hours:
            return ''
        return 'прямо сейчас'
    if not hours:
        pretext = 'через '
    if 10 < noun < 20:
        return pretext + word_return(noun) + ' минут'
    if s == 1:
        return pretext + word_return(noun) + ' минуту'
    if 1 < s < 5:
        return pretext + word_return(noun) + ' минуты'
    if s > 4 or s == 0:
        return pretext + word_return(noun) + ' минут'


def build_message_hours(noun):
    noun_h = noun // 60
    if not noun_h:
        return build_message_minutes(noun, False)
    if 10 < noun_h < 20:
        return 'через ' + str(noun_h) + ' часов ' + \
               build_message_minutes(noun % 60, True)
    s = noun_h % 10
    if s == 1:
        return 'через ' + str(noun_h) + ' час ' + \
               build_message_minutes(noun % 60, True)
    if 1 < s < 5:
        return 'через ' + str(noun_h) + ' часа ' + \
               build_message_minutes(noun % 60, True)
    if s > 4 or s == 0:
        return 'через ' + str(noun_h) + ' часов ' + \
               build_message_minutes(noun % 60, True)


def rasp_to_text(data) -> str:
    pretext = ['Затем', 'Далее', 'Вскоре после него', 'Следом', 'Потом',
               'Еще один']
    if len(data) == 0:
        return 'Нет отправлений в ближайший час.'
    if (int(data[0]['diff'].total_seconds()) // 60) > 60:
        result = 'Ближайший поезд отправляется {}.\n'.format(
            build_message_hours(int(data[0]['diff'].total_seconds()) // 60)
        )
    else:
        result = 'Ближайший поезд отправляется {}.\n'.format(
            build_message_hours(
                int(data[0]['diff'].total_seconds()) // 60)
        )
    for row in data[1:]:
        if (int(row['diff'].total_seconds()) // 60) > 60:
            result += '{} {}.\n'.format(random.choice(pretext),
                                        build_message_hours(int(
                                            row['diff'].total_seconds()) // 60))
        else:
            result += '{} {}.\n'.format(random.choice(pretext),
                                        build_message_hours(int(
                                            row['diff'].total_seconds()) // 60))
    return result
