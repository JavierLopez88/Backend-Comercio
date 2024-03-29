from .. import db
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellidos = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True, index=True)
    role = db.Column(db.String(45), nullable=False, default="cliente")
    telefono = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=dt.datetime.now(), nullable=False)
    compras = db.relationship('Compra', back_populates="usuario", cascade="all, delete-orphan")

    #======================================================================
    #Getter de la contraseña, la contraseña plana no puedo leerla, es decir no puedo acceder a ella, 
    # es una propiedad de la clase pero no va a estar en la base de datos, yo en esta clase voy a 
    # tener un atributo plain_password, pero nunca se va a guardar en mi db, solo lo voy a usar para generar el hash
    @property
    def plain_password(self):
        raise AttributeError('Password can\'t be read')

    #setter de la contraseña, toma un valor en texto plano
    #genera el hash y lo guarda en el atributo password
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    #metodo que compara una contraseña en texto plano generando su hash y comparandolo con el hash guardado en mi base de datos
    def validate_pass(self, password):
        return check_password_hash(self.password, password)
    #======================================================================

    def __repr__(self):
        return f'{self.nombre}'

    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'email': self.email,
            'telefono': self.telefono,
            'role': self.role,
            'fecha': str(self.fecha_registro)
        }
        return usuario_json

    @staticmethod  #convierte json en objeto python
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        apellidos = usuario_json.get('apellidos')
        email = usuario_json.get('email')
        telefono = usuario_json.get('telefono')
        password = usuario_json.get('password')
        role = usuario_json.get('role')
        fecha_registro = usuario_json.get('fecha_registro')
        return Usuario(
            id = id,
            nombre = nombre,
            apellidos = apellidos,
            email = email,
            telefono = telefono,
            plain_password = password,
            role = role,
            fecha_registro = fecha_registro
        )
#-----------------------------------------------------------------------------    
