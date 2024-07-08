import gspread
from gspread_formatting import *

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def cell_name(row, col):
    return f'{alphabet[col-1]}{row}'

def cell_range(start_row, start_col, end_row, end_col):
    return f'{alphabet[start_col-1]}{start_row}:{alphabet[end_col-1]}{end_row}'

def create_week(name, sheet):
    #week_worksheet = sheet.add_worksheet(title=name, rows=100, cols=100)
    week_ws = sheet.worksheet(name)
    week_ws.clear()
    week_ws.format('B1:Z99', {"horizontalAlignment":"CENTER"})
    week_ws.format('B1:Z1', {'textFormat': {'bold': True}})
    set_column_width(week_ws, 'A', 200)
    
    users_worksheet = sheet.worksheet('users')
    i = 1
    while 0 == 0:
        user = users_worksheet.cell(i, 3).value
        if user is None:
            break
        week_ws.update_cell(i+3, 1, user)
        i = i + 1

    schedule_ws = sheet.worksheet('schedule')
    current_day = schedule_ws.cell(1, 1).value
    start_column = 2
    i = 1
    while 0 == 0:
        subject = schedule_ws.cell(i, 3).value
        day = schedule_ws.cell(i, 1).value
        if day != current_day:
            range = cell_range(1, start_column, 1, i)
            week_ws.merge_cells(range)
            week_ws.update_cell(1, start_column, current_day)
            range = cell_range(2, start_column, 2, i)
            week_ws.merge_cells(range)
            current_day = day
            start_column = i + 1

        if subject is None:
            break
        week_ws.update_cell(3, i + 1, subject)
        i = i + 1

    #week_ws.merge_cells('B2:C2')
