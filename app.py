#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from hashlib import md5

from flask import Flask, request, render_template, make_response
from flask_socketio import SocketIO, send, emit

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declared_attr



uri_prefix = os.environ.get('URI_PATH') if os.environ.get('URI_PATH') is not None else ''
basedir = os.path.abspath(os.path.dirname(__file__))
sqlite3_filename = 'geolocation_test.sqlite3'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, sqlite3_filename)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret!'


socketio = SocketIO(app, cors_allowed_origins='*') # TODO: cors_allowed_originは本来適切に設定するべき

db = SQLAlchemy(app)
migrate = Migrate(app, db)



class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)



class GeolocationRecorder(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    md5_code = db.Column(db.String, nullable=False)
    user_agent = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<GeolocationRecorder id:{} [{}] [{}] >'.format(self.id, self.user_agent, self.cookie_id)



class GeolocationCoordinates(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    geolocation_recorder_md5_code = db.Column(db.String,)
    latitude = db.Column(db.Double)
    longitude = db.Column(db.Double,)
    altitude = db.Column(db.Double,)
    accuracy = db.Column(db.Double,)
    altitudeAccuracy = db.Column(db.Double,)
    heading = db.Column(db.Double,)
    meter_per_second = db.Column(db.Double,)

    def __repr__(self):
        return '<GeolocationCoordinates recorder:{} id:>'.format(self.geolocation_recorder_id, self.id)



@app.route(f'/{uri_prefix}')
def index():
    resp = make_response(render_template('index.html', uri_prefix=uri_prefix))
    if request.cookies.get('md5_code') is None:
        resp.set_cookie('md5_code', md5(bytes(str(time.time()), 'utf-8')).hexdigest())
    return resp



## https://kivantium.hateblo.jp/entry/2021/10/18/110509

# ユーザー数
user_count = 0
# 現在のテキスト
text = ""

# ユーザーが新しく接続すると実行
@socketio.on('connect')
def connect(auth):
    global user_count, text
    user_count += 1
    # 接続者数の更新（全員向け）
    emit('count_update', {'user_count': user_count}, broadcast=True)
    # テキストエリアの更新
    emit('text_update', {'text': text})


# ユーザーの接続が切断すると実行
@socketio.on('disconnect')
def disconnect():
    global user_count
    user_count -= 1
    # 接続者数の更新（全員向け）
    emit('count_update', {'user_count': user_count}, broadcast=True)


# テキストエリアが変更されたときに実行
@socketio.on('text_update_request')
def text_update_request(json):
    global text
    text = json["text"]
    # 変更をリクエストした人以外に向けて送信する
    # 全員向けに送信すると入力の途中でテキストエリアが変更されて日本語入力がうまくできない
    emit('text_update', {'text': text}, broadcast=True, include_self=False)

# 位置情報取得時に実行
@socketio.on('geolocation_record_request')
def geolocation_record_request(coords):
    request.cookies.get('md5_code')
    print(request.cookies.get('md5_code'), coords)

    db.session.add(GeolocationCoordinates(**{
        'geolocation_recorder_md5_code': request.cookies.get('md5_code'),
        'timestamp': datetime.fromisoformat(coords['timestamp']),
        'accuracy': coords['accuracy'],
        'altitude': coords['altitude'],
        'altitudeAccuracy': coords['altitudeAccuracy'],
        'heading': coords['heading'],
        'latitude': coords['latitude'],
        'longitude': coords['longitude'],
        'meter_per_second': coords['speed']
    }))
    db.session.commit()


if __name__ == '__main__':
    # 本番環境ではeventletやgeventを使うらしいが簡単のためデフォルトの開発用サーバーを使う
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)