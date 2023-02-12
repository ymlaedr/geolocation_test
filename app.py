#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declared_attr



basedir = os.path.abspath(os.path.dirname(__file__))
sqlite3_filename = 'geolocation_test.sqlite3'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, sqlite3_filename)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    user_agent = db.Column(db.String, nullable=False)
    cookie_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<GeolocationRecorder id:{} [{}] [{}] >'.format(self.id, self.user_agent, self.cookie_id)



class GeolocationCoordinates(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    geolocation_recorder_id = db.Column(
        'geolocation_recorder_id',
        db.Integer,
        db.ForeignKey('geolocation_recorder.id', onupdate='CASCADE', ondelete='CASCADE'))
    latitude = db.Column(db.Double)
    longitude = db.Column(db.Double,)
    altitude = db.Column(db.Double,)
    accuracy = db.Column(db.Double,)
    altitudeAccuracy = db.Column(db.Double,)
    heading = db.Column(db.Double,)
    meter_per_second = db.Column(db.Double,)

    def __repr__(self):
        return '<GeolocationCoordinates recorder:{} id:>'.format(self.geolocation_recorder_id, self.id)



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/pipe')
def pipe():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            time.sleep(1)
            message = ws.receive()
            if message is None:
                break
            datetime_now = datetime.datetime.now()
            data = {
                'time': str(datetime_now),
                'message': message
            }
            ws.send(json.dumps(data))
            print(message)
            print(data)
    return



if __name__ == '__main__':
    app.debug = True

    host = '0.0.0.0'
    port = 8080
    host_port = (host, port)

    server = WSGIServer(
        host_port,
        app,
        handler_class=WebSocketHandler
    )
    server.serve_forever()