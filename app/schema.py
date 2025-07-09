from marshmallow import Schema, fields, validate


class ReviewSchema(Schema):
    """Serializer for reviews API =)"""

    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)
    sentiment = fields.Str(
        dump_only=True, validate=validate.OneOf(["negative", "positive", "neutral"])
    )
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        title = "Review"
