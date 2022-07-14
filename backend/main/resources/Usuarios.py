from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel


class Usuario(Resource):

    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    #------------------------------------------------------------------------
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    #------------------------------------------------------------------------
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

#======================================================================================

class Usuarios(Resource): #(sin paginación)

    def get(self):
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios]
        })
    #------------------------------------------------------------------------
