from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Configure naming conventions for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    # Specify which relationships to serialize
    serialize_rules = ('-baked_goods.bakery',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # One-to-many relationship
    baked_goods = db.relationship('BakedGood', backref='bakery', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Bakery {self.name}>'

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    # Specify which relationships to serialize
    serialize_rules = ('-bakery.baked_goods',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def __repr__(self):
        return f'<Baked Good {self.name}, ${self.price}>'