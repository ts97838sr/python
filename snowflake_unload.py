import sys
import pandas as pd
import snowflake.connector
import configparser
import ast,json,logging,datetime
import numpy as np

curr_timestamp = datetime.datetime.now().strftime("%Y%m%d_%I%M%s")
logname = 'snowflake' +curr_timestamp +'.log'
logger = logging.getLogger("snowflake")
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/var/log/' + logname)
fh.setLevel(logging.INFO)
formatter = logging.Firmatter('%(asctime)s %(levelname)s %(message)s',datefrmt='%Y-%m-%dT%H:%M:%S%z' )
fh.setFormatter(formatter)
logger.addHandler(fh)

def dbconfig_parser(region):
    """
    Config parser Reading db credentials INI File
    """
    config=configparser.ConfigParser()
    config.read('db_config.ini')
    db_credentials = dict((k.upper(), v) for k,v in config.items(region.lower()))
    db_credentials = ast.literal_eval(json.dumps(db_credentials))
    return db_credentials

def get_snowflake_connection(region,db_credentials):
    """
    Authenticate and deliver snowflake connection object
    """
    ctx = snowflake.connector.connect(
    user=db_credentials['USER'],
    password=db_credentials['PASSWORD'],
    account=db_credentials['HOST'],
    warehouse=db_credentials['WAREHOUSE']
    )
    return ctx

def get_snowflake_cursor(regon,db_credentials):
    """
    Deliver a cursor for query execution
    """
    ctx = get_snowflake_connection(region,db_credentials)
    cs = ctx.cursor()
    return cs

def select_table(user,table,cursor):
    """
    Select and return selected User table
    """
    sql ='''SELECT * FROM SB.USER_{user}.{table}'''
    cursor.execute(sql)
    return cursor.fetchall()

def get_query_as_df(sql,cursor):
    """
    Deliver a pandas dataframe for a query
    """
    cursor.execute(sql)
    t_data = cursor.fetchall()
    t_columns = cursor._column_idx_to_name.values()
    df = pd.DataFrame(t_data,columns=t_columns)
    for col in df.columns:
        if ((df[col].dtypes != np.int64) & (df[col].dtypes != np.float64)):
            df[col] = df[col].fillna('')
    return df

def unloadmain(region,query):
    try:
        db_credentials = dbconfig_parser(region)
        logger.info('Extract Database connection details')
    except Exception as err:
        logger.error('Extract Database connection details failed : %s', err)
        exit(2)
    else:
        logger.info('Start Database session')

    try:
        unload_data=get_query_as_df(query,get_snowflake_cursor(region,db_credentials))
        logger.info('DATA UNLOAD : %s', query)
    except Exception as e:
        logger.error('Database unload failed: %s ',e)
        exit(3)
    else:
        logger.info('Database unload finished successfully for: %s',query)

    fh.flush()
    fh.close()
    return unload_data
