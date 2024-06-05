from service import run_lighthouse
import constants
import utils
import excel



if __name__ == '__main__':
    device = 'desktop'

    file_path = f'json/report-{device}.json'

    reports = []
    for i in range(constants.ITERATION):
        code = run_lighthouse(constants.local_url, device=constants.device, headless=True)

        if code != 0:
            print(f'Error: {code}')
            exit(code)

        data = utils.read_json_file(file_path)
        filtered_data = utils.format_data(data)
        print(filtered_data)
        reports.append(filtered_data)

    excel_file = excel.Excel(file_path='template/initial.xlsx', sheet_name='GoTo_HomePage')
    for row, report in enumerate(reports):
        if report:
            excel_file.write_row(report, row + constants.ENV)
        
    excel_file.save_file(constants.local_new_excel)
