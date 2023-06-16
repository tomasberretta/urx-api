from marshmallow import Schema, fields, validate


class PartialGripperRequestSchema(Schema):
    amount = fields.Integer(required=True, validate=lambda x: 0 <= x <= 255)

class MoveRequestSchema(Schema):
    direction = fields.Str(required=True, validate=validate.OneOf(["up", "down", "left", "right", "forward", "backward", "roll", "pitch", "yaw"]))
    distance = fields.Float(required=True, validate=lambda x: x >= 0)
    acceleration = fields.Float(required=False, missing=None, validate=lambda x: x >= 0)
    velocity = fields.Float(required=False, missing=None, validate=lambda x: x >= 0)


class MoveJRequestSchema(Schema):
    joint_positions = fields.List(fields.Float(), required=True, validate=lambda x: len(x) == 6)
    acceleration = fields.Float(required=False)
    velocity = fields.Float(required=False)
    pose_object = fields.Boolean(required=False)
    relative = fields.Boolean(required=False)


class MoveLRequestSchema(Schema):
    coordinates_and_angles = fields.List(fields.Float(), required=True, validate=lambda x: len(x) == 6)
    acceleration = fields.Float(required=False)
    velocity = fields.Float(required=False)
    pose_object = fields.Boolean(required=False)
    relative = fields.Boolean(required=False)


class MoveLSRequestSchema(Schema):
    coordinates_list = fields.List(fields.List(fields.Float(), required=True, validate=lambda x: len(x) == 6),
                                   required=True)
    acceleration = fields.Float(required=False)
    velocity = fields.Float(required=False)


class SetConfigRequestSchema(Schema):
    velocity = fields.Float(required=False)
    acceleration = fields.Float(required=False)
    wait_timeout_limit = fields.Float(required=False)
    program_running_timeout_limit = fields.Float(required=False)
