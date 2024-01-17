#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    data = {"key": "value"}
    return jsonify(data)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if bakery:
        return jsonify(bakery.serialize())
    else:
        return jsonify({'message': 'Bakery not found'}), 404


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    all_baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify(BakedGood.serialize_list(all_baked_goods))

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive_good:
        return jsonify(most_expensive_good.serialize())
    else:
        return jsonify({'message': 'No baked goods found'}), 404
