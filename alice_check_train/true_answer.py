import random


class InvalidNumberException(Exception):
    pass


# pylint: disable=R0911,R0912
def first_req(noun):
    if noun == 0:
        return ''
    if noun == 1:
        return 'одну'
    if noun == 2:
        return 'две'
    if noun == 3:
        return 'три'
    if noun == 4:
        return 'четыре'
    if noun == 5:
        return 'пять'
    if noun == 6:
        return 'шесть'
    if noun == 7:
        return 'семь'
    if noun == 8:
        return 'восемь'
    if noun == 9:
        return 'девять'
    raise InvalidNumberException(
        'wrong number is entered: {}'.format(noun))


# pylint: disable=R0911,R0912
def word_return(noun):
    if noun < 10:
        return first_req(noun)
    if 9 < noun < 20:
        if noun == 10:
            return 'десять'
        if noun == 11:
            return 'одинадцать'
        if noun == 12:
            return 'двенадцать'
        if noun == 13:
            return 'тринадцать'
        if noun == 14:
            return 'четырнадцать'
        if noun == 15:
            return 'пятнадцать'
        if noun == 16:
            return 'шестнадцать'
        if noun == 17:
            return 'семнадцать'
        if noun == 18:
            return 'восемнадцать'
        if noun == 19:
            return 'девятнадцать'
        if noun == 20:
            return 'двадцать'
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
            return
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
