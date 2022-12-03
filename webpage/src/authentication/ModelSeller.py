from flask_login import UserMixin

class Admin(UserMixin):
    def __init__(self, nombre, rut):
        self.nombre =  nombre
        self.rut=rut
        self.id=rut
    
    def __repr__(self):
        return f'<Vendedor: {self.rut}>'
    def get_admin(self):
        return self.rut

class Seller(UserMixin):
    def __init__(self, nombre, rut):
        self.nombre =  nombre
        self.rut=rut
        self.id=rut
    
    def __repr__(self):
        return f'<Vendedor: {self.rut}>'
    def get_seller(self):
        return self.rut