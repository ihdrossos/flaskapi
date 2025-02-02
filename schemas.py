from marshmallow import Schema, fields

"""
    Validation with marshmallow
"""

class PlainItemSchema(Schema):
    """
    name, price and store_id μόνο για validation
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    """
    name μόνο για validation
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    """
    Δέν βάζουμε required=True γιατί δεν ξέρουμε ποιο απο τα 2 θα αλλάξουν
    """
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

