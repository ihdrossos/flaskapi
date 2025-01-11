from marshmallow import Schema, fields

"""
    Validation with marshmallow
"""

class ItemSchema(Schema):
    """
    name, price and store_id μόνο για validation
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id= fields.Str(required=True)

class ItemUpdateSchema(Schema):
    """
    Δεν βάζουμε required=True γιατί δεν ξέρουμε ποιο απο τα 2 θα αλλάξουν
    """
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    """
    name μόνο για validation
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

