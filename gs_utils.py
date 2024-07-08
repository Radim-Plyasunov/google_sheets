import gspread

def find_user(user_ws, user_id, user_name):
    ids = user_ws.col_values(2)
    names = user_ws.col_values(1)
    if user_id in ids:
        i = ids.index(user_id)
        return user_ws.cell(i + 1, 3).value
    if user_name in names:
        i = names.index(user_name)
        if user_id != 0:
            user_ws.update_cell(i + 1, 2, user_id)
        return user_ws.cell(i + 1, 3).value
    return None

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

def get_subjects(subject_ws, day_number):
    result = []
    day_name = weekdays[day_number]
    cells = subject_ws.get("A1:B99")
    for row in cells:
        if row[0] == day_name:
            result.append(row[1])
    return result