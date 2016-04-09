import json
import sqlalchemy

from flask_restful import Resource, request

from bson.objectid import ObjectId
from wtforms import Form, StringField, PasswordField, validators, FloatField
from wtforms import IntegerField
from settings import DATABASE_Settings, check_secret, log_level
from utils.mongo import MongoDb
from utils.forms import Check_form

import logging

logging.basicConfig(level=log_level)

##################################################
#               Start
#           Get flavours
##################################################

class GetFlavours(Resource):
    def get_flavours(self):
        engine = MongoDb.init(DATABASE_Settings, "flavours")
        res = engine.get_data({"status": True})
        if res == False:
            logging.error("Find data error ! //{0}//".format(self.__class__.__name__ ))
        ret = []
        for row in res:
            logging.debug(row)
            check = ['name', 'CN_name', 'price', '_id']
            error = 0
            for x in check:
                if x not in row:
                    error = 1
                    break
            if error == 0:
                tmp = {'flavour': row['name'],
                       'CN_name': row['CN_name'],
                       'price': row['price'],
                       'id' : str(row['_id'])}
                ret.append(tmp)
        return ret

    def post(self):
        try:
            flavours = self.get_flavours()
        except Exception, e:
            return 'ko {0}'.format(e.message), 500
        return flavours, 200

##################################################
#               Start
#           Get flavours admin
##################################################

class AdminCheckForm(Form):
    secret = StringField('The id of the order', [validators.DataRequired(), check_secret])

class GetFlavoursAdmin(Resource):
    def get_flavours(self):
        engine = MongoDb.init(DATABASE_Settings, "flavours")
        res = engine.get_data({})
        if res == False:
            logging.error("Find data error ! //{0}//".format(self.__class__.__name__ ))
        ret = []
        for row in res:
            logging.debug(row)
            check = ['name', 'status', 'CN_name', 'price', '_id']
            error = 0
            for x in check:
                if x not in row:
                    error = 1
                    break
            if error == 0:
                tmp = {'flavour': row['name'],
                       'status': row['status'],
                       'CN_name': row['CN_name'],
                       'price': row['price'],
                       'id' : str(row['_id'])}
                ret.append(tmp)
        return ret

    def post(self):
        form = AdminCheckForm(request.form)
        if not form.validate():
            return 'ko', 400
        flavours = self.get_flavours()
        return flavours, 200

##################################################
#               Start
#           New flavour
##################################################

class NewFlavourForm(Form):
    secret = StringField('The id of the order', [validators.DataRequired(), check_secret])
    name = StringField('Name of the new flavour', [validators.DataRequired()])
    CNname = StringField('Name of the new flavour', [validators.DataRequired()])
    price = FloatField('Price of the order', [validators.InputRequired()])

class NewFlavour(Resource):
    def save_flavour(self, flavour, cn_name, price):
        engine = MongoDb.init(DATABASE_Settings, "flavours")
        tmp = engine.save_data({'name': flavour,
                                "CN_name": cn_name,
                                "price": price,
                                "status": False})
        return tmp

    def post(self):
        form = NewFlavourForm(request.form)
        if not form.validate():
            logging.error("Invalid form ! //{0}// {1}".format(self.__class__.__name__ , request.form))
            return 'Invalid form', 400
        name = form.name.data
        cn_name = form.CNname.data
        price = form.price.data
        try:
            flavours = self.save_flavour(name, cn_name, price)
        except Exception, e:
            logging.debug('ERROR ! //NewFlavour// {0}'.format(e.message))
            print e.message
            return 'ko1', 400
        if flavours == False:
            return 'ko2', 400
        return 'ok', 200

##################################################
#               Start
#           Change flavour status
##################################################

class ChangeFlavourStatusForm(Form):
    secret = StringField('The id of the order', [validators.DataRequired(), check_secret])
    id = StringField('Name of the new flavour', [validators.DataRequired()])
    status = IntegerField('Status we are going to set the Flavour 1 to enable and 2 to disable', [validators.DataRequired()])


class ChangeFlavourStatus(Resource):
    def save_flavour(self, id, status):
        engine = MongoDb.init(DATABASE_Settings, "flavours")
        try:
            tmp = engine.edit_data({"_id": ObjectId(id)},
                                {"$set":
                                    {"status": status}
                                })
            logging.debug("matched_count {0}".format(tmp.matched_count))
        except Exception, e:
            logging.error("{0} // {1}".format(self.__class__.__name__ , e.message))


    @Check_form(ChangeFlavourStatusForm)
    def post(self):
        form = ChangeFlavourStatusForm(request.form)
        id = form.id.data
        if form.status.data == 1:
            new_status = True
        else:
            new_status = False
        print 'new status {0}'.format(new_status)
        try:
            flavours = self.save_flavour(id, new_status)
        except Exception, e:
            logging.error("{0} // {0}".format(self.__class__.__name__ , e.message))
            return 'ko', 400
        return 'ok', 200

##################################################
#               Start
#           Edit a flavour un the db
##################################################

class EditFlavourForm(Form):
    secret = StringField('The id of the order', [validators.DataRequired(), check_secret])
    type = StringField('The field we are changing', [validators.DataRequired()])
    id = StringField('Id of the field we are changing', [validators.DataRequired()])
    value = StringField('value of the field we are changing', [validators.DataRequired()])

class EditFlavour(Resource):
    def edit_value(self, id, field, value):
        try:
            engine = MongoDb.init(DATABASE_Settings, "flavours")
            tmp = engine.edit_data({"_id": ObjectId(id)},
                                {"$set":
                                    {field: value}
                                })
        except Exception, e:
            logging.error("{0} // {1}".format(self.__class__.__name__ , e.message))

    @Check_form(EditFlavourForm)
    def post(self):
        form = EditFlavourForm(request.form)
        types = ['price', 'CN_name', 'name']
        if form.type.data not in types:
            return 'ko', 400
        id = form.id.data
        field = form.type.data
        value = form.value.data
        try:
            self.edit_value(id, field, value)
        except Exception, e:
            return 'ko', 500
        return 'ok', 200

