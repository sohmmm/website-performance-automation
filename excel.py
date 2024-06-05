import openpyxl

class Excel:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name

        self.workbook = openpyxl.load_workbook(file_path, data_only=False)
        self.worksheet = self.workbook[sheet_name]

    def write_row(self, row_data, row_num):
        for col_num, value in enumerate(row_data, start=1):
            cell = self.worksheet.cell(row=row_num, column=col_num)
            cell.value = value

    def save_file(self, file_path):
        self.workbook.save(file_path)
        print(f'Saved to {file_path}')

