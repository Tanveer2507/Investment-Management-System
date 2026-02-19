import urllib.request

url = 'http://127.0.0.1:8000/documents/'
try:
    resp = urllib.request.urlopen(url, timeout=5)
    print('STATUS', resp.getcode())
    data = resp.read(500)
    print('LEN', len(data))
    print(data.decode('utf-8', errors='ignore')[:200])
except Exception as e:
    print('ERROR', e)
