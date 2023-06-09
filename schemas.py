from marshmallow import Schema, fields


class PartialGripperRequestSchema(Schema):
    amount = fields.Integer(required=True, validate=lambda x: 0 <= x <= 255)


class MoveRequestSchema(Schema):
    coordinates = fields.List(fields.Float(), required=True, validate=lambda x: len(x) == 3)
    angles = fields.List(fields.Float(), required=True, validate=lambda x: len(x) == 3)
    acceleration = fields.Float(required=False)
    velocity = fields.Float(required=False)


class SetConfigRequestSchema(Schema):
    velocity = fields.Float(required=False)
    acceleration = fields.Float(required=False)
    wait_timeout_limit = fields.Float(required=False)
    program_running_timeout_limit = fields.Float(required=False)
