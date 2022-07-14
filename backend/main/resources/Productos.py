from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import ProductoModel


class Productos(Resource):
    def post(self):
        producto = ProductoModel.from_json(request.get_json()) #listen un json y lo hace obj python
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201 #devuelve obj python en forma de json
    #------------------------------------------------------------------------
    def get(self):
        page = 1
        per_page = 5
        productos = db.session.query(ProductoModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        productos = productos.paginate(page, per_page, True, 10)
        return jsonify({
            'productos': [producto.to_json() for producto in productos.items],
            'total': productos.total,
            'pages': productos.pages,
            'page': page
        })

#======================================================================================

class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            return producto.to_json()
        except:
            return 'Producto no existe'
    #------------------------------------------------------------------------
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items() #retorna clave:valor
        for key, value in data:
            setattr(producto, key, value) 
        try:
            db.session.add(producto) #si ya existe lo actualiza
            db.session.commit()
            return producto.to_json(), 201
        except:
            return '', 404
    #------------------------------------------------------------------------
    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except:
            return '', 404
