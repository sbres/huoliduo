import json
import sqlalchemy
from datetime import datetime

from utils.forms import Check_form
from utils.mysql import Update_val, Sql_run, Sql_execute

from flask_restful import Resource, request

from sqlalchemy.pool import NullPool
from wtforms import Form, StringField, PasswordField, validators, FloatField, BooleanField
from wtforms import IntegerField
from settings import DATABASE, check_secret, log_level, DATABASE_Settings
from utils.mongo import MongoDb
from bson.objectid import ObjectId

import logging

logging.basicConfig(level=log_level)
##################################################
#               Start
#           Get Stores
##################################################

class AdminCheckForm(Form):
    secret = StringField('The secret token of the admin', [validators.DataRequired(), check_secret])


class GetStores(Resource):
    def get_stores(self):
        engine = MongoDb.init(DATABASE_Settings, "stores")
        res = engine.get_data({})
        if res == False:
            logging.error("Find data error ! //{0}//".format(self.__class__.__name__ ))
        ret = []
        for row in res:
            tmp = {'id': str(row.get('_id')),
                   'name': row.get('name'),
                   'city': row.get('city'),
                   'open': row.get('open')}
            ret.append(tmp)
        return ret

    @Check_form(AdminCheckForm)
    def post(self):
        form = AdminCheckForm(request.form)
        try:
            flavours = self.get_stores()
        except Exception, e:
            logging.error(" {0} // {1}".format(self.__class__.__name__ , e.message))
            return 'ko', 500
        return flavours, 200


##################################################
#               Start
#            Open close shop
##################################################

class StoreOCForm(Form):
    secret = StringField('The secret token of the admin',
                         [validators.DataRequired(message='Secret is needed'), check_secret])
    id = StringField('store id', [validators.DataRequired()])
    action = BooleanField('The action true to open flase to close', [validators.AnyOf([True, False])])


class OCStore(Resource):
    @Check_form(StoreOCForm)
    def post(self):
        form = StoreOCForm(request.form)
        id = form.id.data
        if form.action.data == True:
            status = 1
        else:
            status = 0
        self.OCStoreDB(id, status)
        return 'ok'

    def OCStoreDB(self, id, status):
        engine = MongoDb.init(DATABASE_Settings, "stores")
        try:
            tmp = engine.edit_data({"_id": ObjectId(id)},
                                {"$set":
                                    {"open": status}
                                })
            logging.debug("matched_count {0}".format(tmp.matched_count))
        except Exception, e:
            logging.error("{0} // {1}".format(self.__class__.__name__ , e.message))



##################################################
#               Start
#            Get store openings
##################################################


class StoreForm(Form):
    secret = StringField('The secret token of the admin',
                         [validators.DataRequired(message='Secret is needed'), check_secret])
    id = StringField('store id', [validators.DataRequired()])


class Get_open_hours_Store(Resource):
    @Check_form(StoreForm)
    def post(self):
        res = []
        form = StoreForm(request.form)
        id = form.id.data
        engine = MongoDb.init(DATABASE_Settings, "opening_time")
        try:
            ret = engine.get_data( { "store_id": ObjectId(id) } )
        except Exception, e:
            logging.error("Find data error ! //{0}//".format(self.__class__.__name__ ))
        for row in ret:
            # logging.debug('{0}'.format(row))
            open_time = str(row.get('open_time'))[0:2] + ":" + str(row.get('open_time'))[2:4] + ":00"
            close_time = str(row.get('close_time'))[0:2] + ":" + str(row.get('close_time'))[2:4] + ":00"
            tmp = {'id': str(row.get('_id')),
                   'start': open_time,
                   'end': close_time,
                   'dow': row.get('week_day'),
                   'allDay': False,
                   # 'title' add she shop name
                   }
            res.append(tmp)
        return res


##################################################
#               Start
#            Create open Time
##################################################

class StoreTimeCreationForm(Form):
    secret = StringField('The secret token of the admin',
                         [validators.DataRequired(message='Secret is needed'), check_secret])
    id = StringField('store id', [validators.DataRequired()])
    open_h = StringField('store opening hour', [validators.DataRequired()])
    open_min = StringField('store opening min', [validators.DataRequired()])
    close_h = StringField('store closing hour', [validators.DataRequired()])
    close_min = StringField('store closing min', [validators.DataRequired()])
    day = StringField('store closing time', [validators.DataRequired()])


class New_open_hours_Store(Resource):
    @Check_form(StoreTimeCreationForm)
    def post(self):
        form = StoreTimeCreationForm(request.form)
        if int(form.open_h.data) > 24 or int(form.open_h.data) < 0 or \
            int(form.close_h.data) > 24 or int(form.close_h.data) < 0:
            return 'ko | check hour !', 400

        if int(form.open_min.data) >= 60 or int(form.open_min.data) < 0 or \
            int(form.close_min.data) >= 60 or int(form.close_min.data) < 0:
            return 'ko | check min !', 400
        open = datetime(year=1970, month=01, day=01, hour=int(form.open_h.data), minute=int(form.open_min.data))
        close = datetime(year=1970, month=01, day=01, hour=int(form.close_h.data), minute=int(form.close_min.data))
        open_str = open.strftime("%H%M00")
        close_str = close.strftime("%H%M00")

        tmp = {"store_id": ObjectId(form.id.data),
               "open_time": open_str,
               "close_time": close_str,
               "week_day": form.day.data,
               }
        try:
            engine = MongoDb.init(DATABASE_Settings, "opening_time")
            engine.save_data(tmp)
        except Exception, e:
            logging.error("{0} // {0}".format(self.__class__.__name__ , e.message))
            return 'ko', 500
        return 'ok'

##################################################
#               Start
#            Delete open time
##################################################

class StoreForm_2(Form):
    secret = StringField('The secret token of the admin',
                         [validators.DataRequired(message='Secret is needed'), check_secret])
    id = StringField('store id', [validators.DataRequired()])

class delete_hours_Store(Resource):
    @Check_form(StoreForm_2)
    def post(self):
        form = StoreForm_2(request.form)
        logging.debug("Goint to delete : {0}".format(form.id.data))
        try:
            engine = MongoDb.init(DATABASE_Settings, "opening_time")
            engine.delete_data({"_id": ObjectId(form.id.data)})
        except Exception, e:
            logging.error("Find data error ! //{0}//".format(self.__class__.__name__ ))

        return 'ok'

##################################################
#               Start
#            Edit open time
##################################################

class StoreTimeEditForm(Form):
    secret = StringField('The secret token of the admin',
                         [validators.DataRequired(message='Secret is needed'), check_secret])
    id = StringField('opening id', [validators.DataRequired()])
    open_h = StringField('store opening hour', [validators.DataRequired()])
    open_min = StringField('store opening min', [validators.DataRequired()])
    close_h = StringField('store closing hour', [validators.DataRequired()])
    close_min = StringField('store closing min', [validators.DataRequired()])
    day = StringField('store closing time', [validators.DataRequired()])

class edit_hours_Store(Resource):
    def edit_time(self, _id, _open, _close, day):
        try:
            logging.debug("id : {0}, open: {1}, close: {2}, day: {3}".format(_id, _open, _close, day))
            engine = MongoDb.init(DATABASE_Settings, "opening_time")
            tmp = engine.edit_data({"_id": ObjectId(_id)},
                                {"$set": {
                                        "open_time": _open,
                                        "close_time": _close,
                                        "week_day": day
                                    }
                                })

        except Exception, e:
            logging.error("{0} // {1}".format(self.__class__.__name__ , e.message))

    @Check_form(StoreTimeEditForm)
    def post(self):
        form = StoreTimeEditForm(request.form)
        open = datetime(year=1970, month=01, day=01, hour=int(form.open_h.data), minute=int(form.open_min.data))
        close = datetime(year=1970, month=01, day=01, hour=int(form.close_h.data), minute=int(form.close_min.data))
        open_str = open.strftime("%H%M00")
        close_str = close.strftime("%H%M00")
        self.edit_time(form.id.data, open_str, close_str, form.day.data)
        return 'ok'

##################################################
#               Start
#            Are stores open
##################################################

from pytz import timezone

class OpenStoresForm(Form):
    city = StringField('The city we want to know ', [validators.DataRequired()])

class AreOpenStores(Resource):
    #TODO add check by cities one day
    #@Check_form(OpenStoresForm)
    def post(self):
        #TZ Asia/Shanghai
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


##################################################
#               Start
#            Create new store
##################################################

class NewStoreForm(Form):
    secret = StringField('The secret token of the admin',
                         [validators.DataRequired(message='Secret is needed'), check_secret])
    name = StringField('Name of the store', [validators.DataRequired()])
    city = StringField('Name of the city', [validators.DataRequired()])
    lat = StringField('latx of the store', [validators.DataRequired()])
    lng = StringField('laty of the store', [validators.DataRequired()])

class NewStore(Resource):
    @Check_form(NewStoreForm)
    def post(self):
        form = NewStoreForm(request.form)
        try:
            self.save_store(form.name.data,
                        form.city.data,
                        form.lat.data,
                        form.lng.data)
        except Exception, e:
            logging.error(" {0} // {1}".format(self.__class__.__name__ , e.message))
            return 'ko', 400
        return 'ok'

    def save_store(self, name, city, lat, lng):
        engine = MongoDb.init(DATABASE_Settings, "stores")
        tmp = engine.save_data({'name': name,
                                'city': city,
                                'lat': lat,
                                'lng': lng,
                                'open': False,
                                'timezone': "Asia/Shanghai"
                                })
        return tmp

