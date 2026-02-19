from django.urls import resolve

paths = [
    '/',
    '/dashboard/',
    '/reports/',
    '/reports/investments/',
    '/reports/startups/',
    '/account/profile/',
    '/account/profile/edit/',
    '/add-startup/',
    '/startups/',
    '/watchlist/',
]

for p in paths:
    try:
        r = resolve(p)
        print(p, '->', r.view_name or str(r.func))
    except Exception as e:
        print(p, '-> ERROR:', type(e).__name__, e)
