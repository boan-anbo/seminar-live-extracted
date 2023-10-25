import json

import requests


def openocr_image(url: str, lang: str) -> str:
    data = {
        "img_url": url,
        "engine": "tesseract",
        "engine_args": { "lang": lang }

    }
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    r = requests.post("http://localhost:9292/ocr", data=json.dumps(data), headers=headers)
    return r.text