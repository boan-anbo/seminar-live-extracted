import json
import re
from typing import cast

import requests
from bs4 import BeautifulSoup

from djangoProject.sources.const import EventbriteDetail, Module

test_url = 'https://www.eventbrite.co.uk/e/luvos-5-tage-online-detox-kur-registrierung-138728317131?aff=ebdssbcitybrowse&keep_tld=1'

def get_eventbrite_html_by_event_url(event_url: str) -> str:
    req = requests.get(event_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        html_raw = soup.find("script", text=re.compile('model:\s?{.*},')).__str__()
        html_part = re.findall(r'model:(\s?{.*}),', html_raw)[0]
        model = cast(EventbriteDetail, json.loads(html_part))
        # html_final_part = html_part.partition("collection:")[0]

        # json_str_part = json_str_part.partition("</script>")[0]

        # print(json.dumps(model, indent=4))

        paragraph_modules = model['structured_content']['modules']
        html_content = ''
        for module in paragraph_modules:
            module = cast(Module, module)
            if module['type'] == 'text':
                html_content += module['data']['body']['text']
        return html_content
    except:
        raise

if __name__ == '__main__':
    html_str = get_eventbrite_html_by_event_url(test_url)
    print(html_str)