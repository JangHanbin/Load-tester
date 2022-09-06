import requests

s = requests.Session()

with s.request(method='get', url='http://127.0.0.1:4755', stream=True) as res:
    for content in res.iter_content():
        if content:
            print(len(content))
