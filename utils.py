import json
import time

def read_json_file(file_path):
    with open(file_path, 'r', encoding="utf8") as file:
        return json.load(file)
        
def format_data(data):
    filtered_data = [
        data['requestedUrl'],
        'local',
        time.strftime("%d/%m/%Y"),
        data['categories']['performance']['score'] * 100,
        data['categories']['accessibility']['score'] * 100,
        data['categories']['best-practices']['score'] * 100,
        data['categories']['seo']['score'] * 100,
        round(to_sec(data['audits']['first-contentful-paint']['numericValue']), 3),
        round(to_sec(data['audits']['largest-contentful-paint']['numericValue']), 3),
        round(to_sec(data['audits']['total-blocking-time']['numericValue']), 3),
        data['audits']['cumulative-layout-shift']['numericValue'],
        round(to_sec(data['audits']['speed-index']['numericValue']), 3)
    ]

    return filtered_data


def to_sec(millis):
    return millis / 1000
