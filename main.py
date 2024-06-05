import time

import constants
import api
import excel
from service import PageSpeedInsights

if __name__ == "__main__":
    test_url = 'https://www.goto.com/'
    psi = PageSpeedInsights(api_key=api.PAGESPEED_API_KEY)

    # get from api
    reports = []
    for i in range(constants.ITERATION):
        current_report = psi.get_report(test_url=constants.test_url)

        # time.sleep(30)
        reports.append(current_report)

    # write into excel
    excel_file = excel.Excel(file_path=constants.filepath, sheet_name='GoTo_HomePage')
    for row, report in enumerate(reports):
        if report:
            excel_file.write_row(report, row + constants.ENV)
    
    # save
    excel_file.save_file(constants.api_new_path)
