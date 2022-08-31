from flask import Blueprint, url_for, request
from werkzeug.utils import redirect
import sqlite3
import pandas as pd

bp = Blueprint('store_api', __name__, url_prefix='/store_api')

@bp.route('/getStoreInfoFromId', methods=['GET'])
def getStoreInfoFromId():
    store_id = request.args['store_id']
    conn = sqlite3.connect('wesharingDB.db')
    print(store_id, conn)
    # fda_df = pd.read_sql_query('SELECT * FROM sqlite_master WHERE type=\'table\';', conn)
    # print(fda_df)
    # conn.close()
    # return fda_df.to_json(force_ascii=False)
    return ""