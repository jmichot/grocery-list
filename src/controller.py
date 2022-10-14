import json

from src.connexion import get_db_connection
from http.client import CONFLICT, NOT_FOUND, OK, BAD_REQUEST
from flask import render_template, jsonify, Response, request

from src.dao import Dao
from src.model.product import Product


def configure_routes(app, test=False):
    dao = Dao(test=test)

    @app.route('/product', methods=['GET'])
    def get_all():
        print('get all elements')
        try:
            products = dao.get_all_product()
            serialize = [p.serialize() for p in products]
            return jsonify(serialize)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/product/<id>', methods=['GET'])
    def get_one_product(id):
        print('get one element : ' + id)
        try:
            product_id = int(id)
            products = dao.get_product_by_id(product_id)
            return jsonify(products.serialize())
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/product/<id>', methods=['PUT'])
    def modify_product(id):
        print('modify element : ' + id + ', ' + request.form.get('name') + ', ' + request.form.get('quantity'))
        try:
            product_id = int(id)
            product_name = request.form.get('name')
            product_quantity = int(request.form.get('quantity'))
            dao.update_product(product_id, product_name, product_quantity)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/product', methods=['POST'])
    def add_product():
        print('add one element : ' + request.form.get('name') + ', ' + request.form.get('quantity'))
        try:
            product_quantity = int(request.form.get('quantity'))
            product_name = request.form.get('name')
            product = Product(None, product_quantity, product_name)
            dao.add_product(product)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=CONFLICT, response=str(e))

    @app.route('/product/<id>', methods=['DELETE'])
    def delete_product(id):
        print('delete one element : ' + id)
        try:
            product_id = int(id)
            dao.delete_product_by_id(product_id)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/')
    def index():
        return render_template('index.html')
