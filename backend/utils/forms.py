from functools import wraps
from flask import request

def Check_form(form_class):
    def check_expired(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            form = form_class(request.form)
            if not form.validate():
                res = {'status' : "ERROR",
                       'failure': []}
                for field, errors in form.errors.items():
                    tmp = {'field': field,
                           'info': getattr(form, field).label.text,
                           'errors': errors}
                    res['failure'].append(tmp)
                return res, 400
            return func(*args, **kwargs)

        return decorated_function
    return check_expired
