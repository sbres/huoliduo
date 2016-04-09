import aerospike
import hashlib
import random, string
import json

from flask_restful import Resource, request
from settings import config_areospike, namespace_areospike
from wtforms import Form, StringField, PasswordField, validators
from wtforms import IntegerField

try:
    client = aerospike.client(config_areospike).connect()
except Exception, e:
    print 'ERROR Database : {0}'.format(e.message)


class UserLoginForm(Form):
    openid = StringField('Wechat openid', [validators.DataRequired()])
    password = PasswordField('Acount password', [validators.DataRequired()])

class UserAuthenticateForm(Form):
    openid = StringField('Wechat openid', [validators.DataRequired()])
    secret = PasswordField('Acount secret key', [validators.DataRequired()])

class NewUser(Resource):
    def post(self):
        data = UserLoginForm(request.form)
        print data.openid.data
        print data.password.data
        if data.validate():
            #check if user exists
            (key, meta) = client.exists((namespace_areospike, 'user', data.openid.data))
            h_password = hashlib.sha512(data.password.data).hexdigest()
            if meta is None:
                #We create a new user
                secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))
                data = {'openid': data.openid.data,
                        'password': h_password,
                        'secret': secret,
                        'balance': 0}
                client.put(key, data)
            else:
                #User wants to login, We refresh token.
                (key, meta, bins) = client.get((namespace_areospike, 'user', data.openid.data))
                if h_password == bins.get('password'):
                    secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))
                    bins['secret'] = secret
                    client.put(key, bins)
                else:
                    return 'ko', 400

            #Return the data
            ret = {'secret': secret}
            return json.dumps(ret), 200202
        else:
            return 'ko', 400

class UserInfoForm(Form):
    openid = StringField('Wechat openid', [validators.DataRequired()])
    secret = PasswordField('Account secret', [validators.DataRequired()])
    name = StringField('Name of the user')
    sex = IntegerField('1 Male , 2 Female')
    phone = IntegerField('Phone of the user')
    birth = IntegerField('Birth of the user in Unix timestamp')
    height = IntegerField('Height of the user in cm')
    weight = IntegerField('weight of the user in g')


class SaveUserData(Resource):
    def post(self):
        form = UserInfoForm(request.form)
        if form.validate():
            (key, meta, bins) = client.get((namespace_areospike, 'user', form.openid.data))
            db_secret = bins.get('secret')
            if form.secret.data != db_secret:
                return 'ko', 400
            to_save = False
            if form.name.data is not None:
                bins['name'] = form.name.data
                to_save = True
            if form.sex.data is not None:
                bins['sex'] = form.sex.data
                to_save = True
            if form.phone.data is not None:
                bins['phone'] = form.phone.data
                to_save = True
            if form.birth.data is not None:
                bins['birth'] = form.birth.data
                to_save = True
            if form.height.data is not None:
                bins['height'] = form.height.data
                to_save = True
            if form.weight.data is not None:
                bins['weight'] = form.weight.data
                to_save = True
            if to_save:
                client.put(key, bins)
            return 'ok', 200
        else:
            return 'ko', 400

class UserAddressForm(Form):
    openid = StringField('Wechat openid', [validators.DataRequired()])
    secret = PasswordField('Account secret', [validators.DataRequired()])
    name = StringField('Name of the place', [validators.DataRequired()])
    address = StringField('Direction of the place', [validators.DataRequired()])


class SaveUserAddress(Resource):
    def post(self):
        form = UserAddressForm(request.form)
        if form.validate() == False:
            return 'ko', 400
        (key, meta, bins) = client.get((namespace_areospike, 'user', form.openid.data))
        db_secret = bins.get('secret')
        if form.secret.data != db_secret:
            return 'ko', 400
        db_address = bins.get('address', [])
        db_address.append({'name': form.name,
                           'address': form.address})
        bins['address'] = db_address
        client.put(key, bins)
        return 'ok', 200

class DeleteUserAddress(Resource):
    def post(self):
        form = UserAddressForm(request.form)
        if form.validate() == False:
            return 'ko', 400
        (key, meta, bins) = client.get((namespace_areospike, 'user', form.openid.data))
        db_secret = bins.get('secret')
        if form.secret.data != db_secret:
            return 'ko', 400
        db_address = bins.get('address', [])
        i = 0
        for pair in db_address:
            if pair['name'] == form.name and pair['address'] == form.address:
                break
            i += 1
        try:
            del db_address[i]
        except Exception, e:
            pass
        bins['address'] = db_address
        client.put(key, bins)
        return 'ok', 200


class GetUserData(Resource):
    def post(self):
        form = UserAuthenticateForm(request.form)
        if form.validate() == False:
            return 'ko', 400
        (key, meta, bins) = client.get((namespace_areospike, 'user', form.openid.data))
        db_secret = bins.get('secret')
        if form.secret.data != db_secret:
            return 'ko', 400
        del bins['secret']
        del bins['password']
        del bins['openid']
        return json.dumps(bins), 200


