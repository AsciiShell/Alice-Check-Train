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
    if noun > 60:
        return word_return(noun % 60)


def build_message_minutes(noun):
    s = noun % 10
    if 10 < noun < 20:
        return word_return(noun) + ' минут'
    if s == 1:
        return word_return(noun) + ' минуту'
    if 1 < s < 5:
        return word_return(noun) + ' минуты'
    if s > 4 or s == 0:
        return word_return(noun) + ' минут'


def build_message_hours(noun):
    noun_h = noun // 60
    s = noun_h % 10
    if 10 < noun_h < 20:
        return word_return(noun_h) + ' часов' + build_message_minutes(noun % 60)
    if s == 1:
        return word_return(noun_h) + ' час' + build_message_minutes(noun % 60)
    if 1 < s < 5:
        return word_return(noun_h) + ' часа' + build_message_minutes(noun % 60)
    if s > 4 or s == 0:
        return word_return(noun_h) + ' часов' + build_message_minutes(noun % 60)


def _second_to_minutes_seconds(s):
    s = int(s)
    return s // 60, s % 60


def rasp_to_text(data) -> str:
    if len(data) == 0:
        return 'Нет ближайших поездов в ближайший час'
    else:
        result = ''
        if (int(data[0]['diff'].total_seconds()) // 60) > 60:
            result = 'Ближайший поезд отправляется через {}\n'.format(
                build_message_hours(int(data[0]['diff'].total_seconds()) // 60)
            )
        else:
            result = 'Ближайший поезд отправляется через {}\n'.format(
                build_message_minutes(int(data[0]['diff'].total_seconds()) // 60)
            )
    for row in data[1:]:
        if (int(row['diff'].total_seconds()) // 60) > 60:
            result += 'Затем через {}\n'.format(
                build_message_hours(int(row['diff'].total_seconds()) // 60))
        else:
            result += 'Затем через {}\n'.format(
                build_message_minutes(int(row['diff'].total_seconds()) // 60))
    return result
