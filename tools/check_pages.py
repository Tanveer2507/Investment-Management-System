from django.test import Client

paths = [
    '/',
    '/dashboard/',
    '/reports/',
    '/reports/investments/',
    '/reports/startups/',
    '/documents/',
    '/documents/upload/',
    '/startups/',
    '/add-startup/',
    '/startups/1/',
]

c = Client()
for p in paths:
    try:
        r = c.get(p, HTTP_HOST='localhost')
        info = f"{p} -> {r.status_code}"
        if 'Location' in r:
            info += f" (Location: {r['Location']})"
        print(info)
        if r.status_code == 200:
            try:
                print(r.content.decode('utf-8')[:400])
            except Exception:
                pass
    except Exception as e:
        print(p, 'ERROR', type(e).__name__, e)
