from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         # do not serialize the password, its a security breach
    #     }

class Planetas(db.Model):
    __tablename__ = 'Planetas'
    id = db.Column(db.Integer, primary_key=True)
    diametro = db.Column(db.String(250))
    periodo_rotacion = db.Column(db.String(250))
    periodo_orbital = db.Column(db.String(250))
    gravedad = db.Column(db.String(250))
    poblacion = db.Column(db.String(250))
    clima = db.Column(db.String(250))
    terreno = db.Column(db.String(250))
    superficie_acuatica = db.Column(db.String(250))
    creado = db.Column(db.String(250))
    editado = db.Column(db.String(250))
    nombre = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "diametro": self.diametro,
            "periodo_rotacion": self.periodo_rotacion,
            "periodo_orbital": self.periodo_orbital,
            "gravedad": self.gravedad,
            "poblacion": self.poblacion,
            "clima": self.clima,
            "terreno": self.terreno,
            "superficie_acuatica": self.superficie_acuatica,
            "creado":self.creado,
            "editado":self.editado,
            "nombre": self.nombre
        }

class Personajes(db.Model):
    __tablename__ = 'Personajes'
    id = db.Column(db.Integer, primary_key=True)
    altura = db.Column(db.String(250))
    masa = db.Column(db.String(250))
    pelo = db.Column(db.String(250))
    piel = db.Column(db.String(250))
    ojos = db.Column(db.String(250))
    nacimiento = db.Column(db.String(250))
    genero = db.Column(db.String(250))
    creado = db.Column(db.String(250))
    editado = db.Column(db.String(250))
    nombre = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "altura": self.altura,
            "masa": self.masa,
            "pelo": self.pelo,
            "piel": self.piel,
            "ojos": self.ojos,
            "nacimiento": self.nacimiento,
            "genero": self.genero,
            "creado": self.creado,
            "editado": self.editado,
            "nombre": self.nombre,
        }

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(250), nullable=False)
    apellido_1 = db.Column(db.String(250), nullable=False)
    apellido_2 = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "apellido_1": self.apellido_1,
            "apellido_2": self.apellido_2,
            "email": self.email,
            "password": self.password
            # "mail": self.mail
        }

class Favoritos(db.Model):
    __tablename__ = 'Favoritos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    personajes_id = db.Column(db.Integer, db.ForeignKey('Personajes.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('Planetas.id'))
    Personajes = db.relationship(Personajes)
    planetas = db.relationship(Planetas)
    usuarios = db.relationship(Usuarios)

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personajes_id": self.personajes_id,
            "planetas_id": self.planetas_id
        }


