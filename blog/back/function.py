from functools import wraps

from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def workon(*args, **kwargs):
        # try:
        ses_user = session['username']
        if ses_user:
            return func(*args, **kwargs)
        # except:
        return redirect(url_for('back_blue.login', error='请先登录'))
    return workon



