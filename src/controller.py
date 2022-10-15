from http.client import CONFLICT, NOT_FOUND, OK, BAD_REQUEST,INTERNAL_SERVER_ERROR
from flask import render_template, jsonify, Response, request

from src.dao import Dao
from src.exceptions.IdException import IdException
from src.exceptions.NameException import NameException
from src.exceptions.ProductException import ProductException
from src.exceptions.QuantityException import QuantityException
from src.exceptions.conflictException import ConflictException
from src.model.product import Product
from src.constants import *


def configure_routes(app, test=False): # pragma: no mutate
    dao = Dao(test=test)

    @app.route('/product', methods=['GET'])
    def get_all():
        try:
            products = dao.get_all_product()
            serialize = [p.serialize() for p in products]
            return jsonify(serialize)
        except Exception:
            return Response(status=INTERNAL_SERVER_ERROR, response=INTERNAL_ERROR)

    @app.route('/product/<id>', methods=['PUT'])
    def modify_product(id):
        try:
            dao.update_product(int(id), request.json['name'], request.json['quantity'])
            return Response(status=OK)
        except KeyError:
            return Response(status=BAD_REQUEST, response=MISSING_ARGUMENTS)
        except ValueError:
            return Response(status=BAD_REQUEST, response=ID_NOT_INT)
        except (IdException, QuantityException, NameException) as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except ProductException as e:
            return Response(status=NOT_FOUND, response=str(e))
        except ConflictException as e:
            return Response(status=CONFLICT, response=str(e))

    @app.route('/product', methods=['POST'])
    def add_product():
        try:
            product = Product(None, request.json['quantity'], request.json['name'])
            dao.add_product(product)
            return Response(status=OK)
        except KeyError:
            return Response(status=BAD_REQUEST, response=MISSING_ARGUMENTS)
        except (IdException, QuantityException, NameException) as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except ProductException as e:
            return Response(status=NOT_FOUND, response=str(e))
        except ConflictException as e:
            return Response(status=CONFLICT, response=str(e))

    @app.route('/product/<id>', methods=['DELETE'])
    def delete_product(id):
        try:
            dao.delete_product_by_id(int(id))
            return Response(status=OK)
        except ValueError:
            return Response(status=BAD_REQUEST, response=ID_NOT_INT)
        except IdException as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except ProductException as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/')
    def index():
        return render_template('index.html')
