
import requests

while True:
    try:
        f = open("slug.txt", "r")
        data = f.read()
        f.close()
        data = data.split('\n')
        for url in data:
            x = requests.get('http://127.0.0.1:8000' + url)
            print('\n\n\n running')
    except Exception as e:
        print(e)
        pass
