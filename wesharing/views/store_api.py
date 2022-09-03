from flask import Blueprint, url_for, request,  jsonify

from werkzeug.utils import redirect
import sqlite3
import pandas as pd

bp = Blueprint('store_api', __name__, url_prefix='/store_api')

@bp.route('/getStoreInfoFromId', methods=['GET'])
def getStoreInfoFromId():
    store_id = request.args['store_id']
    conn = sqlite3.connect('wesharingDB.db')
    fda_df = pd.read_sql_query(f"select * from 'tbl_store' where store_id={store_id}", conn)
    conn.close()
    print("requested detail store info",store_id)
    return jsonify(fda_df.to_dict(orient='records'))

def getGpsRange(raw, lat, lon, diff):
    raw_lat, raw_lon = raw.split(',')
    if (lat-diff <= float(raw_lat) <= lat+diff) and (lon-diff <= float(raw_lon) <= lon+diff):
        return True
    return False

@bp.route('/getStoreByGPS', methods=['GET'])
def getStoreByGPS():
    if request.method == 'GET':
        lat = float(request.args['lat'])
        lon = float(request.args['lon'])
        distance = int(request.args['dis'])
        diff = 0.00001 * distance

        print(lat,lon,distance)

        conn = sqlite3.connect('wesharingDB.db')
        store_df = pd.read_sql_query(f"select * from 'FDA'", conn)
        conn.close()

        store_filtered = store_df[store_df['GPS'].apply(
            getGpsRange, args=(lat, lon, diff))]
        return jsonify(store_filtered.to_dict(orient='records'))


@bp.route('/getStoreAll', methods=['GET'])
def getStoreAll():
    if request.method == 'GET':
        print("get All store data info")

        conn = sqlite3.connect('wesharingDB.db')
        store_df = pd.read_sql_query(f"select * from 'FDA'", conn)
        conn.close()

        return jsonify(store_df.to_dict(orient='records'))