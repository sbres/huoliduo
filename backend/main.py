from flask import Flask, redirect, send_from_directory
from flask_restful import Resource, Api
from flask.ext.cors import CORS

from order import NewOrder, ConfirmOrder, GetCalEstimate, GetOrderStatus

from order_admin import GetNewOrders, MakerOrderAccept, GetProductionOrders
from order_admin import OrderDone, GetWaitingOrders, OrderSent
from product import GetFlavours, NewFlavour, ChangeFlavourStatus, GetFlavoursAdmin
from product import EditFlavour

from stores import GetStores, OCStore, Get_open_hours_Store
from stores import New_open_hours_Store, delete_hours_Store, edit_hours_Store
from stores import AreOpenStores, NewStore


import logging
from logging.handlers import RotatingFileHandler

#logging.basicConfig()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

#logging.getLogger('flask_cors').level = logging.DEBUG

######################################################
#                   All about flavours
#
######################################################
api.add_resource(GetFlavours, '/api/v0/product/flavours/get')                   #Updated
api.add_resource(GetFlavoursAdmin, '/api/v0/product/flavours/getadmin')         #Updated
api.add_resource(NewFlavour, '/api/v0/product/flavours/new')                    #Updated
api.add_resource(ChangeFlavourStatus, '/api/v0/product/flavours/setstatus')     #Updated
api.add_resource(EditFlavour, '/api/v0/product/flavours/edit_existing')         #Updated



######################################################
#                   All about stores
#
######################################################

api.add_resource(NewStore, '/api/v0/stores/admin/new')                          #Updated
api.add_resource(OCStore, '/api/v0/stores/admin/ocstore')                       #Updated
api.add_resource(GetStores, '/api/v0/stores/admin/getall')                      #Updated
api.add_resource(AreOpenStores, '/api/v0/stores/areopen')                       #Updated




######################################################
#                   All about stores
#                    Opening times
######################################################

api.add_resource(Get_open_hours_Store, '/api/v0/stores/admin/getopenhstore')    #Updated
api.add_resource(New_open_hours_Store, '/api/v0/stores/admin/newopenhstore')    #Updated
api.add_resource(delete_hours_Store, '/api/v0/stores/admin/delopenhstore')      #Updated
api.add_resource(edit_hours_Store, '/api/v0/stores/admin/editopenhstore')       #Updated




######################################################
#             User Endpoints for Order
#
######################################################
api.add_resource(GetCalEstimate, '/api/v0/product/order/estimate')              #ok
api.add_resource(NewOrder, '/api/v0/product/order/new')                         #Updated
api.add_resource(ConfirmOrder, '/api/v0/product/order/user_accept')             #Updated
api.add_resource(GetOrderStatus, '/api/v0/product/order/get_status')



api.add_resource(GetNewOrders, '/api/v0/product/orders/get_new')                #Updated
api.add_resource(MakerOrderAccept, '/api/v0/product/order/maker_accept')        #Updated
api.add_resource(GetProductionOrders, '/api/v0/product/orders/get_making')      #Updated
api.add_resource(OrderDone, '/api/v0/product/orders/done')                      #Updated
api.add_resource(GetWaitingOrders, '/api/v0/product/orders/waiting')            #Updated
api.add_resource(OrderSent, '/api/v0/product/orders/sent')                      #Updated

#@app.errorhandler(Exception)
#def all_exception_handler(error):
#    app.logger.error(str(error))
#    return 'SNAP https://media.giphy.com/media/xs6FqhzEdWMZW/giphy.gif', 500

import socket

@app.route('/')
def nigga():
    return '{0}'.format(socket.gethostname())
    return 'Supp nigga you lost ?'

@app.route('/admin')
def admin_index():
    return redirect('/admin/index.html')

@app.route('/admin/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/app/', filename)

@app.route('/sound/<path:filename>')
def get_sounds(filename):
    return send_from_directory(app.root_path + '/sound/', filename)



if __name__ == '__main__':
    handler = RotatingFileHandler('log/rest-api.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=8000)
