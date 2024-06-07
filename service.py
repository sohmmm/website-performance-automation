import requests
import subprocess

import time
import utils


class PageSpeedInsights:
    def __init__(self, api_key):
        self.base_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
        self.api_key = api_key

    def get_report(self, test_url, device='desktop', category=['performance', 'accessibility', 'best-practices', 'seo']):
        params = {
            'key': self.api_key,
            'url': test_url,
           'strategy': device,
            'category': category,
        }

        filtered_data = None
        try:
            res = requests.get(self.base_url, params=params, verify=False, cert=False)
            data =  res.json()

            region = 'Asia'
            filtered_data = [
                test_url,
                region,
                time.strftime("%d/%m/%Y"),
                data['lighthouseResult']['categories']['performance']['score'] * 100,
                data['lighthouseResult']['categories']['accessibility']['score'] * 100,
                data['lighthouseResult']['categories']['best-practices']['score'] * 100,
                data['lighthouseResult']['categories']['seo']['score'] * 100,
                round(utils.to_sec(data['lighthouseResult']['audits']['first-contentful-paint']['numericValue']), 3),
                round(utils.to_sec(data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']), 3),
                round(utils.to_sec(data['lighthouseResult']['audits']['total-blocking-time']['numericValue']), 3),
                data['lighthouseResult']['audits']['cumulative-layout-shift']['numericValue'],
                round(utils.to_sec(data['lighthouseResult']['audits']['speed-index']['numericValue']), 3)
            ]
        except requests.exceptions.RequestException as err:
            print(err)
            return None

        return filtered_data
    

def run_lighthouse(test_url, device='desktop', headless=False, timeout=360):
    cmd = [
        'lighthouse', test_url,
        '--output', 'json',
        f'--output-path', f'json/report-{device}.json',
        f'--chrome-flags=--start-maximized {'--headless' if headless else ''}',
        '--only-categories=performance,accessibility,best-practices,seo',
    ]

    if device == 'desktop':
        cmd.append('--preset')
        cmd.append('desktop')

    result = subprocess.run(
        cmd,
        timeout=timeout * 1000,
        shell=True,
        capture_output=True,
        text=True
    )

    return result.returncode
    