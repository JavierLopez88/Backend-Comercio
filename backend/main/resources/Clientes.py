from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel

class Cliente(Resource):
    
    def get(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        if cliente.role == 'cliente':
            return cliente.to_json()
        else:
            return '', 404
    #-----------------------------------------------------------------
    def delete(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        try:
            db.session.delete(cliente)
            db.session.commit()
            return '', 204
        except:
            return '', 404
    #-----------------------------------------------------------------
    def put(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(cliente, key, value)
        try:
            db.session.add(cliente)
            db.session.commit()
            return cliente.to_json(), 201
        except:
            return '', 404

#======================================================================================

class Clientes(Resource):
    
    def get(self):
        page = 1
        per_page = 5
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente')
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        clientes = clientes.paginate(page, per_page, True, 10)
        return jsonify({
            'clientes': [cliente.to_json() for cliente in clientes.items],
            'total': clientes.total,
            'pages': clientes.pages,
            'page': page
        })
    #-----------------------------------------------------------------
    def post(self):
        cliente = UsuarioModel.from_json(request.get_json())
        cliente.role = 'cliente'
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201

