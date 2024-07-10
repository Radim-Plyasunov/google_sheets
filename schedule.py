import gspread
from datetime import *
from gspread_formatting import *
from create_week import alphabet, cell_range

class Schedule:
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # в конструкторе создаем объект, который кодлючается к нашему файлу в облаке
    def __init__(self, service_account_file, spreadsheet_id):
        gc = gspread.service_account(service_account_file)
        self.sheet = gc.open_by_key(spreadsheet_id)
        self.user_ws = self.sheet.worksheet('users')
        self.subject_ws = self.sheet.worksheet('schedule')
    
    def cell_range(self, start_row, start_col, end_row, end_col):
        return f'{self.alphabet[start_col-1]}{start_row}:{self.alphabet[end_col-1]}{end_row}'

    # поиск пользователя по его идентификатору или имени
    # если идентификатор не был сохранен, то сохраняем его
    def find_user(self, user_id, user_name):
        ids = self.user_ws.col_values(2)
        names = self.user_ws.col_values(1)
        if user_id in ids:
            i = ids.index(user_id)
            return self.user_ws.cell(i + 1, 3).value
        if user_name in names:
            i = names.index(user_name)
            if user_id != 0:
                self.user_ws.update_cell(i + 1, 2, user_id)
            return self.user_ws.cell(i + 1, 3).value
        return None
    
    # получение списка пользователей
    def get_users(self):
        users = self.user_ws.col_values(3)
        users.sort()
        return users
    
    #полчуение расписания
    def get_schedule(self):
        return self.subject_ws.get("A1:C99")            # наедемся, что не больше 99 уроков в неделю )))

    # получение списка предметов по заданному дню недели
    def get_subjects(self, day_number):
        result = []
        day_name = self.weekdays[day_number]
        cells = self.get_schedule()
        for row in cells:
            if row[0] == day_name:
                result.append(row[2])
        return result
    
    # поиск листа с заданным именем
    def find_worksheet(self, title):
        for ws in self.sheet.worksheets():
            if ws.title == title:
                return ws
        return None

    # установка отметки, если все получилось и нашли, то возвращаем True
    def set_mark(self, user, subject, mark):
        #ищем нужный лист по текущей дате
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        ws_name = monday.strftime("%d.%m.%Y")      # dd.mm.yyyy
        # ищем лист
        week_ws = self.find_worksheet(ws_name)
        # если не находим, то создаем лист и заполняем
        if week_ws is None:
            week_ws = self.create_week(monday)
        
        i = 4
        # ищем строку с пользователем
        while i <= week_ws.row_count:
            current_user = week_ws.cell(i, 1).value
            if current_user == user:
                # ищем столбец
                j = 2
                while j <= week_ws.col_count:
                    current_date = week_ws.cell(2, j).value
                    current_subject = week_ws.cell(3, j).value
                    if today.strftime("%d.%m.%Y") == current_date and subject == current_subject:
                        week_ws.update_cell(i, j, f"'{mark}")
                        return True
                    j = j + 1
                return False
            i = i + 1
        return False

    def create_week(self, date):
        ws_name = date.strftime("%d.%m.%Y")
        users = self.get_users()
        schedule = self.get_schedule()
        rows = len(users) + 3 # 3 на заголовок
        cols = len(schedule) + 1
        week_ws = self.sheet.add_worksheet(title=ws_name, rows=rows, cols=cols)
        #week_ws.clear()

        # настройка страницы
        week_ws.format(cell_range(1, 2, rows, cols), {"horizontalAlignment":"CENTER"})
        week_ws.format(cell_range(1, 1, 1, cols), {'textFormat': {'bold': True}})
        set_column_width(week_ws, 'A', 200)
        
        # формирование списка пользователей
        i = 4
        for user in users:
            week_ws.update_cell(i, 1, user)
            i = i + 1

        i = 2
        current_day = schedule[0][0] # получаем первый день недели
        start_column = i
        schedule.append(["", "", ""])
        for row in schedule:
            day = row[0]
            subject = row[2]
            if day != current_day:
                range = self.cell_range(1, start_column, 1, i - 1)
                week_ws.merge_cells(range)
                week_ws.update_cell(1, start_column, current_day)
                date = date + timedelta(days=1)
                current_day = day
                start_column = i

            if day == "":
                break

            week_ws.update_cell(2, i, date.strftime("%d.%m.%Y"))
            week_ws.update_cell(3, i, subject)
            i = i + 1
        return week_ws
