import socket
from wtforms import ValidationError
import logging

hostname = socket.gethostname()
mail = {'send': False,
        'Email_to_send': "",
        'Email_to_send_pass': "",
        'Email_to_receive': []}

if hostname == 'Stephanes-MacBook-Pro.local' or hostname == 'Stephanes-MBP':
    DATABASE_Settings = {
        'user': 'dev',
        'password': 'dev',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'purefood'
        }
elif hostname == 'docker_python':
    DATABASE_Settings = {
        'user': 'admin',
        'password': 'dev',
        'host': 'mongodb',
        'port': '27017',
        'database': 'huoliduo'
        }


else:
    DATABASE_Settings = {
        'user': 'flask',
        'password': 'Pfoodn1',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'purefood'
        }

DATABASE = "mysql+mysqlconnector://%s:%s@%s:%s/%s" % (str(DATABASE_Settings.get('user')),
                                                     str(DATABASE_Settings.get('password')),
                                                     str(DATABASE_Settings.get('host')),
                                                     str(DATABASE_Settings.get('port')),
                                                     str(DATABASE_Settings.get('database')))

secret = 'cfdgvshbfjnkvemrgjw4hipfeuovyackfdsjhvafds'

log_level = logging.DEBUG

def check_secret(form, to_check):
    if form.secret.data != secret:
        raise ValidationError("Invalid secret")
