import hashlib
import sqlalchemy
import json
import random
import string
import logging
import time

from sqlalchemy.pool import NullPool
from flask_restful import Resource, request
from settings import DATABASE, check_secret, DATABASE_Settings, log_level
from wtforms import Form, StringField, PasswordField, validators, FloatField, IntegerField, BooleanField
from wtforms import IntegerField

from utils.mongo import MongoDb
from bson.objectid import ObjectId

logging.basicConfig(level=log_level)

##################################################
#               Start
#           Get All New orders
##################################################

class AdminCheckForm(Form):
    secret = StringField('The secret of the admin', [validators.DataRequired(), check_secret])

class GetNewOrders(Resource):
    def post(self):
        form = AdminCheckForm(request.form)
        print request.form
        if not form.validate():
            return 'ko', 400
        ret = []
        query = {
            "status": "u_acepted"
        }
        engine = MongoDb.init(DATABASE_Settings, "orders")
        res = engine.get_data(query)
        for row in res:
            tmp = dict(row.items())
            tmp['flavour'] = json.loads(tmp['flavour'])
            logging.debug(tmp)
            tmp["id"] = str(tmp["_id"])
            del tmp["_id"]
            ret.append(tmp)
        return ret

##################################################
#               Start
#           Accept order from user
##################################################

class ConfimOrder(Form):
    oid = StringField('The id of the order', [validators.DataRequired()])
    osecret = StringField('The id of the order', [validators.DataRequired()])
    action = IntegerField('1 to confirm and 2 to cancel', [validators.DataRequired()])
    secret = StringField('The secret of the admin', [validators.DataRequired(), check_secret])

class MakerOrderAccept(Resource):
    def change_status(self, oid, isecret, status):
        engine = MongoDb.init(DATABASE_Settings, "orders")
        query = {
            "status": "u_acepted",
            "_id": ObjectId(oid),
            "secret": isecret,
        }
        status = {1: "m_acepted", 2: "m_canceled"}[status]
        key = "history.{0}".format(time.time())
        new_data = {"$set": {
                        "status": status,
                        key: "MakerOrderAccept"
                    }}
        engine.edit_data(query, new_data)

    def post(self):
        logging.debug("1")
        form = ConfimOrder(request.form)
        if not form.validate():
            logging.debug("2")
            return 'Not valid', 502
            return 'ko', 502
        logging.debug("3")
        if form.action.data != 1 and form.action.data != 2:
            return 'ko', 502
        self.change_status(form.oid.data, form.osecret.data, form.action.data)
        return 'ok', 200

##################################################
#               Start
#           Get All orders in production
##################################################

class GetProductionOrders(Resource):
    def post(self):
        form = AdminCheckForm(request.form)
        print request.form
        if not form.validate():
            return 'ko', 400
        query = {
            "status": "m_acepted"
        }
        engine = MongoDb.init(DATABASE_Settings, "orders")
        res = engine.get_data(query)
        ret = []
        for row in res:
            logging.debug("Row : {0}".format(row))
            tmp = row
            tmp["id"] = str(tmp["_id"])
            del tmp["_id"]
            ret.append(tmp)
        return ret

##################################################
#               Start
#           Validate a order is made
##################################################

class MinConfimOrder(Form):
    oid = StringField('The id of the order', [validators.DataRequired()])
    osecret = StringField('The id of the order', [validators.DataRequired()])
    secret = StringField('The secret of the admin', [validators.DataRequired(), check_secret])

class OrderDone(Resource):
    def change_status(self, oid, isecret):
        engine = MongoDb.init(DATABASE_Settings, "orders")
        query = {
            "status": "m_acepted",
            "_id": ObjectId(oid),
            "secret": isecret,
        }
        status = "m_done"
        key = "history.{0}".format(time.time())
        new_data = {"$set": {
                        "status": status,
                        key: "MakerOrderDone"
                    }}
        engine.edit_data(query, new_data)

    def post(self):
        form = MinConfimOrder(request.form)
        if not form.validate():
            return 'Not valid', 502
            return 'ko', 502
        self.change_status(form.oid.data, form.osecret.data)
        return 'ok', 200

##################################################
#               Start
#     Get all orders waiting to be send
##################################################

class GetWaitingOrders(Resource):
    def post(self):
        form = AdminCheckForm(request.form)
        if not form.validate():
            return 'ko', 400
        query = {
            "status": "m_done"
        }
        engine = MongoDb.init(DATABASE_Settings, "orders")
        res = engine.get_data(query)
        ret = []
        for row in res:
            tmp = row
            tmp["id"] = str(tmp["_id"])
            del tmp["_id"]
            tmp['flavour'] = json.loads(tmp['flavour'])
            ret.append(tmp)
        return ret


##################################################
#               Start
#      Say that the order was sent.
##################################################

class MinConfimOrder_2(Form):
    oid = StringField('The id of the order', [validators.DataRequired()])
    osecret = StringField('The id of the order', [validators.DataRequired()])
    secret = StringField('The secret of the admin', [validators.DataRequired(), check_secret])

class OrderSent(Resource):
    def change_status(self, oid, isecret):
        engine = MongoDb.init(DATABASE_Settings, "orders")
        query = {
            "status": "m_done",
            "_id": ObjectId(oid),
            "secret": isecret,
        }
        status = "shipped"
        key = "history.{0}".format(time.time())
        new_data = {"$set": {
                        "status": status,
                        key: "Sent"
                    }}
        engine.edit_data(query, new_data)

    def post(self):
        form = MinConfimOrder_2(request.form)
        if not form.validate():
            return 'Not valid', 502
            return 'ko', 502
        self.change_status(form.oid.data, form.osecret.data)
        return 'ok', 200