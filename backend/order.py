import hashlib
import sqlalchemy
import json
import random
import string
import logging
import time

from sqlalchemy.pool import NullPool
from flask_restful import Resource, request
from settings import DATABASE, DATABASE_Settings, log_level
from settings import mail as MAIL_SETTINGS
from wtforms import Form, StringField, PasswordField, validators, FloatField, IntegerField, BooleanField
from wtforms import IntegerField
from pytz import timezone
from datetime import datetime
from utils.mysql import Sql_run
from utils.mail import notify_mail

from product import GetFlavours

from utils.mongo import MongoDb
from bson.objectid import ObjectId

logging.basicConfig(level=log_level)

##################################################
#               Start
#           Estimate User nb of Cal
##################################################

class EstimateUserForm(Form):
    sex = IntegerField('1 women, 2 men', [validators.DataRequired()])
    age = IntegerField('Age of user', [validators.DataRequired()])
    weight = FloatField('Weight of user', [validators.DataRequired()])
    height = FloatField('Height of user', [validators.DataRequired()])


class GetCalEstimate(Resource):
    def calc_energetic_needs(self, data):
        """
        :param data:
        :return: The amount of calories a user needs.

        Men: 10 x weight (kg) + 6.25 x height (cm) - 5 x age (y) + 5
        Women: 10 x weight (kg) + 6.25 x height (cm) - 5 x age (y) - 161.
        Next we multiply base rate by between 1.2 and 1.6 depending on exercise level.

        """
        #This is not kim's but it the precise one.
        cal_need = 0
        cal_need += data.weight.data * 10
        cal_need += data.height.data * 6.25
        cal_need -= data.age.data * 5
        if data.sex.data == 1:
            cal_need -= 161
        else:
            cal_need += 5

        active_cal_need = 1.3 * cal_need
        normal_cal_need = 1.15 * cal_need
        _tmp = {0: {'cal': cal_need},
                1: {'cal': normal_cal_need},
                2: {'cal': active_cal_need}}
        return _tmp

    def post(self):
        form = EstimateUserForm(request.form)
        if not form.validate():
            return 'ko', 400
        calories_needed = self.calc_energetic_needs(form)
        for key, value in calories_needed.items():
            cals = value['cal']
            if form.sex.data == 1:
                price = cals * 0.01
            else:
                price = cals * 0.012
            calories_needed[key]['price'] = round(price * 4)
        return calories_needed, 200


##################################################
#               Start
#           New User Order
##################################################

class NewOrderForm(Form):
    name = StringField('User name', [validators.DataRequired()])
    sex = IntegerField('1 women, 2 men', [validators.DataRequired()])
    age = IntegerField('Age of user', [validators.DataRequired()])
    weight = FloatField('Weight of user', [validators.DataRequired()])
    height = FloatField('Height of user', [validators.DataRequired()])
    sport = IntegerField('Sport level of the user, 0 to 2', [validators.DataRequired()])
    flavour = StringField('Flavour of the shake', [validators.DataRequired()])
    address = StringField('Address where we are going to deliver', [validators.DataRequired()])
    phone = StringField('User phone number', [validators.DataRequired()])
    amount = IntegerField('Amount of shakes user wants', [validators.DataRequired()])

class NewOrder(Resource):
    def create_recipe(self, data, user_cal):
        recipe = {}
        cal_used = 0
        if data.sex.data == 1:
            recipe['Base_W'] = (1, 'base')
            cal_used += 1600
        else:
            recipe['Base_M'] = (1, 'base')
            cal_used += 2000

        extra_cals = user_cal - cal_used

        #The value is the number of calories by gr of product
        products = {'Maltodexine': 3.8,
                    'Coconut oil': 8.85,
                    'Rice protein': 3.631}
        per_product = extra_cals / len(products)
        for key, value in products.items():
            tmp = per_product / value
            recipe[key] = (int(tmp), 'gr')
        return recipe

    def calc_energetic_needs(self, data):
        """
        :param data:
        :return: The amount of calories a user needs.

        Men: 10 x weight (kg) + 6.25 x height (cm) - 5 x age (y) + 5
        Women: 10 x weight (kg) + 6.25 x height (cm) - 5 x age (y) - 161.
        Next we multiply base rate by between 1.2 and 1.6 depending on exercise level.

        """
        #This is not kim's but it the precise one.
        cal_need = 0
        cal_need += data.weight.data * 10
        cal_need += data.height.data * 6.25
        cal_need -= data.age.data * 5
        if data.sex.data == 1:
            cal_need -= 161
        else:
            cal_need += 5
        if data.sport.data == 3:
            cal_need *= 1.3
        elif data.sport.data == 2:
            cal_need *= 1.15
        return cal_need

    def save_order(self, data, ingredients, price, ran_string):
        data = {"user": {"name": data.name.data,
                          "age": data.age.data,
                          "height": data.height.data,
                          "weight": data.weight.data,
                          "sport_level": data.sport.data
                          },
                "amount": data.amount.data,
                "address": data.address.data,
                "recipe": ingredients,
                "price": price,
                "flavour": data.flavour.data,
                "secret": ran_string,
                "phone": data.phone.data,
                "status": "new",
                "history": {str(int(time.time())) : "created",},
                "created": str(int(time.time()))
        }
        engine = MongoDb.init(DATABASE_Settings, "orders")
        id = engine.save_data(data, get_id=True)
        return id

    def is_store_open(self):
        SZtimezone = timezone('Asia/Shanghai')
        SZtime = datetime.now(SZtimezone)
        SQL = """SELECT COUNT(1) FROM `opening_time`
                  INNER JOIN `stores`
                  ON opening_time.store_id = stores.id
                  AND stores.open = 1
                  WHERE `week_day`={0} AND `open_time` < "{1}"
                  AND `close_time` > "{2}"
        """.format(SZtime.strftime("%w"),
                   SZtime.strftime("%H:%M:00"),
                   SZtime.strftime("%H:%M:00"))
        #ret = Sql_run(DATABASE, SQL)
        query_1 = {
            "open": 1
        }
        query_2 = {
            "week_day": SZtime.strftime("%w"),
            "open_time": {"$lt": SZtime.strftime("%H%M00")},
            "close_time": {"$gt": SZtime.strftime("%H%M00")},
            "store_id": 42
        }
        try:
            engine_1 = MongoDb.init(DATABASE_Settings, "stores")
            engine_2 = MongoDb.init(DATABASE_Settings, "opening_time")
            res = engine_1.get_data(query_1)
            logging.debug("found {0}".format(res))
            for store in res:
                logging.debug("found {0}".format(store))
                query_2['store_id'] = store.get('_id')
                tmp = engine_2.exists(query_2)
                logging.debug("query2 : {0}".format(query_2))
                if tmp is True:
                    return True
            logging.debug("Nothing wrong ")
        except Exception, e:
            logging.error("{0} // {1}".format(self.__class__.__name__ , e.message))
        return False

    def get_flavours(self):
        ret = GetFlavours()
        tmp = ret.get_flavours()
        return tmp

    def check_flavour(self, flavour_avail, flavour_to_check):
        """
        :param flavour_avail:
        :param flavour_to_check:
        :return: Return False if the flavour doesn't exit
        """
        for element in flavour_avail:
            if element['flavour'] == flavour_to_check:
                return True
        return False

    def get_flavour_price(self, flavours_db, flavour):
        """
        :param flavour_avail:
        :param flavour_to_check:
        :return: Return False if the flavour doesn't exit
        """
        for element in flavours_db:
            if element['flavour'] == flavour:
                return float(element['price'])
        return 0

    def post(self):
        if self.is_store_open() == False:
            #TODO add more info.
            return 'Store is closed', 400

        price = 0
        sport_avail = [1, 2, 3]
        form = NewOrderForm(request.form)
        if not form.validate():
            return 'ko', 400
        amount = form.amount.data
        _flavours = self.get_flavours()
        if amount > 4:
            amount = 4
            #Or don't take the order
        if not form.sport.data in sport_avail:
            return 'wrong sport level'
        try:
            flavours = json.loads(form.flavour.data)
        except Exception, e:
            print 'ERROR'
            print e.message
            print form.flavour.data

            return 'Check the flavours should be a dico. You send {0} /// {1}'.format(form.flavour.data, e.message), 400
            return 'ko', 400
        check_t = 0
        for element in flavours:
            if not self.check_flavour(_flavours, element):
                print element
                return 'Flavour doesnt exist', 502
            check_t += int(flavours[element])
            price += int(flavours[element]) * self.get_flavour_price(_flavours, element)
        print 'Check_t {0}'.format(check_t)
        if check_t != amount:
            return 'Check the tot amount and the flavours', 400
            return 'ko', 502
        ran_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))
        calories_needed = self.calc_energetic_needs(form)
        #The recipie is for one shake
        ingredients = self.create_recipe(form, calories_needed)
        if form.sex.data == 2:
            price += calories_needed * 0.01
        else:
            price += calories_needed * 0.012
        total = price * amount
        total = round(total)
        oid = self.save_order(form, ingredients, total, ran_string)
        notify_mail(MAIL_SETTINGS, "New Order", "A new order just arrive please check.")
        _return = {'calories': calories_needed,
                   'qty': amount,
                   'price': total,
                   'oid': str(oid),
                   'oscret': ran_string}
        return _return, 200
        #return json.dumps(_return), 200

##################################################
#               Start
#           User Confirm Order
##################################################

class ConfimOrder(Form):
    oid = StringField('The id of the order', [validators.DataRequired()])
    osecret = StringField('The id of the order', [validators.DataRequired()])
    awnser = IntegerField('1 to confirm and 2 to cancel', [validators.DataRequired()])#AnyOf([True, False])

class ConfirmOrder(Resource):
    def checkrequest(self, id, secret):
        engine = MongoDb.init(DATABASE_Settings, "orders")
        query = {
            "status": "new",
            "secret": secret,
            "_id": ObjectId(id)
        }
        return engine.exists(query)

    def ChangeOrderStat(self, oid, status):
        engine = MongoDb.init(DATABASE_Settings, "orders")
        query = {
            "status": "new",
            "_id": ObjectId(oid)
        }
        status = {1: "u_acepted", 2: "u_canceled"}[status]
        key = "history.{0}".format(int(time.time()))
        new_data = {"$set": {
                        "status": status,
                        key: "ConfimOrder"
                    }}
        return engine.edit_data(query, new_data)

    def post(self):
        form = ConfimOrder(request.form)
        print form.oid.data
        if not form.validate():
            return 'Not valid', 502
            return 'ko', 502
        if form.awnser.data != 1 and form.awnser.data != 2:
            return 'ko', 502
        if not self.checkrequest(form.oid.data, form.osecret.data):
            logging.debug("{0} // oid {1}".format(self.__class__.__name__ , form.oid.data))
            logging.debug("{0} // osecret {1}".format(self.__class__.__name__ , form.osecret.data))
            return 'Invalid data ko', 502
            return 'ko', 502
        self.ChangeOrderStat(form.oid.data, form.awnser.data)
        return 'ok', 200

##################################################
#               Start
#           User Get order Status
##################################################

class GetOrderStatusForm(Form):
    oid = StringField('The id of the order', [validators.DataRequired()])
    osecret = StringField('The id of the order', [validators.DataRequired()])

ORDER_STATUS = {'to_confirm_user': {"US": "You need to confirm your order.",
                               "CN": "TO DO"},
                'canceled_user': {"US": "You cancelled your order.",
                               "CN": "TO DO"},
                'to_confirm_houliduo': {"US": "Your order needs to be confirmed by us.",
                               "CN": "TO DO"},
                'canceled_houliduo': {"US": "Your order was cancelled by us.",
                               "CN": "TO DO"},
                'making': {"US": "Your order is being made",
                               "CN": "TO DO"},
                'made': {"US": "Your order is going to be send",
                               "CN": "TO DO"},
                'send': {"US": "Your order was sent ! it should arrive soon !",
                               "CN": "TO DO"},}

class GetOrderStatus(Resource):
    def checkrequest(self, id, secret):
        query = {
            "_id": ObjectId(id),
            "secret": secret,
        }
        engine = MongoDb.init(DATABASE_Settings, "orders")
        res = engine.get_data(query)
        if res == []:
            return 'ERROR'
        logging.debug("Order : {0}".format(res[0]))
        data = res[0]
        status = data.get("status", "ERROR")

        return status

    def post(self):
        form = GetOrderStatusForm(request.form)
        if not form.validate():
            return 'Not valid', 502
            return 'ko', 502
        ret = self.checkrequest(form.oid.data, form.osecret.data)
        if ret == 'ERROR':
            return 'ko', 400
        return ret, 200