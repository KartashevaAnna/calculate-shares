import xlsxwriter
from typing import Dict, List


def write_to_excel(resulting_shares: List[Dict[str, int]]):
    workbook = xlsxwriter.Workbook("to_ignore_by_git/RESULT.xlsx")
    worksheet = workbook.add_worksheet()

    row = 0
    column = 0
    col_names = [
        "№",
        "Название",
        "Всего акций",
        "Акций каждому",
        "Акций Ане",
        "Разделить после получения",
    ]
    for name in col_names:
        worksheet.write(row, column, name)
        column += 1
    for item in resulting_shares:
        column = 0
        row += 1
        for key in item:
            worksheet.write(row, column, item[key])
            column += 1
    worksheet.autofit()
    workbook.close()
