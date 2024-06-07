import streamlit as st
import time

from excel import Excel
from service import PageSpeedInsights, run_lighthouse
import api
import utils


excel_row_nums = {
    "Development-Before": 3,
    "Development-After": 9,
    "Review-Before": 23,
    "Review-After": 29,
    "Gamma-Before": 43,
    "Gamma-After": 49,
    "Production-Before": 63,
    "Production-After": 69,
}


def pagespeed_insights(test_url, delay, iteration, device):
    psi = PageSpeedInsights(api_key=api.PAGESPEED_API_KEY)

    reports = []
    for _ in range(iteration):
        current_report = psi.get_report(test_url=test_url, device=device)
        reports.append(current_report)

        time.sleep(delay)

    return reports

def local_lighthouse(test_url, delay, device, iteration):
    reports = []
    for _ in range(iteration):
        code = run_lighthouse(test_url, device=device, headless=False)
        if code != 0:
            st.toast(f'Some error occured. Please try again. code: {code}')
            return

        data = utils.read_json_file(f'json/report-{device}.json')
        filtered_data = utils.format_data(data)
        reports.append(filtered_data)

        time.sleep(delay)

    return reports

def generate_excel_report(uploaded_file, reports, sheet_row_num, sheet_name='GoTo_HomePage'):
    try:
        excel_file = Excel(file_path=uploaded_file, sheet_name=sheet_name)

        for row, report in enumerate(reports):
            if report:
                excel_file.write_row(report, row + sheet_row_num)

        excel_file.save_file('reports/report.xlsx')

        return "Report generated successfully"
    except:
        return "Some error occured. Please try again."
    

def main():
    st.title("PageSpeed Insights")

    uploaded_file = st.file_uploader("Upload template", type=["xlsx"])

    test_url = st.text_input("Enter the URL to test", value='https://www.goto.com/')

    col1, col2, col3 = st.columns(3)
    with col1:
        tool = st.radio(
            "Select the tool",
            ("Lighthouse", "Page Speed Insights"),
            key='tool_option'
        )
    with col2:
        device = st.radio(
            "Select the device",
            ("desktop", "mobile"),
            key='device_option'
        )
    with col3:
        environment_duration = st.radio(
            "Select the environment duration",
            ("Before", "After"),
            key='environment_duration_option'
        )

    environment = st.selectbox("Select Environment", ["Development", "Review", "Gamma", "Production"])

    col1, col2 = st.columns(2)
    with col1:
        delay = st.number_input("Delay", value=30, min_value=0, key='delay')
    with col2:
        iteration = st.number_input("Iteration", value=5, min_value=0, key='iteration')

    start_test_btn = st.button("Start Test")

    if start_test_btn:
        if environment is None:
            st.toast('Please select the environment')
        elif environment_duration is None:
            st.toast('Please select the environment duration')
        elif uploaded_file is None:
            st.toast("Please upload a file")
        else:
            sheet_row_num = excel_row_nums[f'{environment}-{environment_duration}']

            try:
                reports = None
                if tool == 'Lighthouse':
                    reports = local_lighthouse(test_url, delay, device, iteration)
                else:
                    reports = pagespeed_insights(test_url, delay, iteration, device)
                
                msg = generate_excel_report(uploaded_file, reports, sheet_row_num)
                
                st.toast(msg)
                st.balloons()
                st.session_state['report'] = True
            except:
                st.error("Error")

    if 'report' in st.session_state:
        download_button = st.download_button(
            label="Download Report",
            data=open("reports/report.xlsx", "rb").read(),
            file_name="report.xlsx",
            mime="application/vnd.ms-excel",
            key='download_button'
        )


if __name__ == "__main__":
    main()