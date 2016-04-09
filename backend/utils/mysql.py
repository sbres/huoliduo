import sqlalchemy
from sqlalchemy.pool import NullPool

def Update_val(DB, table, where_field, where_val, field, val):
    engine = sqlalchemy.create_engine(DB,
                                          encoding='latin1',
                                          strategy='threadlocal',
                                          poolclass=NullPool,
                                          echo=True)
    engine.pool._use_threadlocal = True
    localconn = engine.connect()
    SQL = """
            UPDATE `{0}` SET `{1}`={2} WHERE `{3}`="{4}"
          """
    FULL_SQL = SQL.format(table, field, val, where_field, where_val)
    tmp = localconn.execute(FULL_SQL)
    tmp.close()
    engine.close()

def Sql_run(DB, SQL):
    """
    Makes a sql query and returns the results.
    :param DB: The Database params from settings.py
    :param SQL: The Query to run
    :return: The Query result.
    """
    engine = sqlalchemy.create_engine(DB,
                                      encoding='latin1',
                                      strategy='threadlocal',
                                      poolclass=NullPool,
                                      echo=True)
    engine.pool._use_threadlocal = True
    localconn = engine.connect()
    tmp = localconn.execute(SQL)
    res = tmp.fetchall()
    tmp.close()
    engine.close()
    return res

def Sql_execute(DB, SQL):
    """
    Makes a sql query and DON'T send the results.
    :param DB: The Database params from settings.py
    :param SQL: The Query to run
    :return: Nothing
    """
    engine = sqlalchemy.create_engine(DB,
                                      encoding='latin1',
                                      strategy='threadlocal',
                                      poolclass=NullPool,
                                      echo=True)
    engine.pool._use_threadlocal = True
    localconn = engine.connect()
    tmp = localconn.execute(SQL)
    tmp.close()
    engine.close()
    return None

