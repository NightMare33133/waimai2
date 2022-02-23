from flask import g,redirect,url_for
from functools import wraps

def login_required(func):
    #写装饰器记得写@wrap()
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(g,'user'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("user.login"))
    return wrapper