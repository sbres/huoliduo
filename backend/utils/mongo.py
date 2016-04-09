from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.DEBUG)


class MongoDb():
    def __init__(self, user, pw, host="127.0.0.1", port=27017, db=None, col=None):
        self.connected = False
        self.db = None
        self.col = None
        url = 'mongodb://{user}:{pw}@{host}:{port}/admin'
        #url = 'mongodb://{user}:{pw}@{host}:{port}/admin?authMechanism=SCRAM-SHA-1'
        self.url = url.format(user=user,
                   pw=pw,
                   host=host,
                   port=port,
                   )
        try:
            self.con = MongoClient(self.url)
            self.connected = True
        except Exception, e:
            logging.error('Failed to connect to db')
        if db is not None:
            self.set_db(db)
            if col is not None:
                self.set_col(col)

    @classmethod
    def init(cls, DATABASE, col):
        return cls(DATABASE.get('user'),
                   DATABASE.get('password'),
                   DATABASE.get('host'),
                   DATABASE.get('port'),
                   DATABASE.get('database'),
                   col
                   )

    def set_db(self, db):
        if not self.connected:
            logging.debug('db not connected')
            return False
        try:
            self.db = self.con.get_database(db)
        except Exception, e:
            self.connected = False
            logging.error("Failed to set db // {0}".format(e.message))
            return False
        return True

    def set_col(self, col):
        if not self.connected:
            print 'db not connected'
            return False
        if self.db is None:
            return False
        try:
            self.col = self.db.get_collection(col)
        except Exception, e:
            logging.error("Failed to ser col // {0}".format(e.message))
            self.connected = False
            return False
        return True

    def save_data(self, data, db=None, col=None, get_id=False):
        if not self.connected:
            logging.error("Engine is not initialised.")
            return False
        if self.col is None and col is None:
            logging.error("Engine is not initialised.")
            return False
        if self.db is None and db is None:
            logging.error("Engine is not initialised.")
            return False
        if col is not None:
            if db is not None:
                try:
                    _db = self.con.get_database(db)
                    _col = _db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return False
            else:
                try:
                    _col = self.db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return False
        else:
            _col = self.col

        try:
            id = _col.insert(data)
        except Exception, e:
            logging.error("Failed inserting data // {0}".format(e.message))
            return False
        if get_id:
            return id
        return True

    def get_data(self, query, db=None, col=None):
        if not self.connected:
            logging.error("Engine is not initialised.")
            return None
        if self.col is None and col is None:
            logging.error("Engine is not initialised.")
            return None
        if self.db is None and db is None:
            logging.error("Engine is not initialised.")
            return None
        if col is not None:
            if db is not None:
                try:
                    _db = self.con.get_database(db)
                    _col = _db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return None
            else:
                try:
                    _col = self.db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return None
        else:
            _col = self.col

        try:
            return self.col.find(query)
        except Exception, e:
            logging.error("Failed finding data // {0}".format(e.message))
            return None

    def exists(self, query, db=None, col=None):
        if not self.connected:
            logging.error("Engine is not initialised.")
            return False
        if self.col is None and col is None:
            logging.error("Engine is not initialised.")
            return False
        if self.db is None and db is None:
            logging.error("Engine is not initialised.")
            return False
        if col is not None:
            if db is not None:
                try:
                    _db = self.con.get_database(db)
                    _col = _db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return False
            else:
                try:
                    _col = self.db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return False
        else:
            _col = self.col

        try:
            tmp = self.col.find(query).limit(1)
        except Exception, e:
            logging.error("Failed finding data // {0}".format(e.message))
        if tmp.count() == 0:
            return False
        return True

    def edit_data(self, query, to_save, db=None, col=None):
        if not self.connected:
            logging.error("Engine is not initialised.")
            return None
        if self.col is None and col is None:
            logging.error("Engine is not initialised.")
            return None
        if self.db is None and db is None:
            logging.error("Engine is not initialised.")
            return None
        if col is not None:
            if db is not None:
                try:
                    _db = self.con.get_database(db)
                    _col = _db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return None
            else:
                try:
                    _col = self.db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return None
        else:
            _col = self.col

        try:
            return self.col.update_one(query, to_save)
        except Exception, e:
            logging.error("Failed finding data // {0}".format(e.message))
            return None

    def delete_data(self, query, db=None, col=None):
        if not self.connected:
            logging.error("Engine is not initialised.")
            return None
        if self.col is None and col is None:
            logging.error("Engine is not initialised.")
            return None
        if self.db is None and db is None:
            logging.error("Engine is not initialised.")
            return None
        if col is not None:
            if db is not None:
                try:
                    _db = self.con.get_database(db)
                    _col = _db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return None
            else:
                try:
                    _col = self.db.get_collection(col)
                except Exception, e:
                    logging.error("Failed initing mongo // {0}".format(e.message))
                    return None
        else:
            _col = self.col

        try:
            return self.col.remove(query)
        except Exception, e:
            logging.error("Failed finding data // {0}".format(e.message))
            return None