from flask import request

def fetch_key(r: request):
    if r.form.get('auth') and len(r.form.get('auth')) > 0:
        return r.form.get('auth')
    elif r.cookies.get('auth') and len(r.cookies.get('auth')) > 0:
        return r.cookies.get('auth')
    else:
        return None
