import FileManager

workbook, filepath = FileManager.GetFile("T4Dir", "Data_Store.xlsx", True)

worksheet1 = workbook["Employers"]

for row in range(1, 200):
    for column in range(1, 10):
        worksheet1.cell(row, column).value = None

worksheet2 = workbook["Employees"]

for row in range(1, 200):
    for column in range(1, 10):
        worksheet2.cell(row, column).value = None


workbook.save(filepath)