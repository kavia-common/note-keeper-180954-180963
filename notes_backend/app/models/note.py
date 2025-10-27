from dataclasses import dataclass, field
from datetime import datetime
from marshmallow import Schema, fields, validate, EXCLUDE


@dataclass
class Note:
    """Domain entity representing a note."""
    id: str
    title: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class NoteCreateSchema(Schema):
    """Schema for validating note creation payloads."""
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True, validate=validate.Length(min=1, max=200), metadata={"description": "Title of the note"})
    content = fields.String(required=True, validate=validate.Length(min=1), metadata={"description": "Content of the note"})


class NoteUpdateSchema(Schema):
    """Schema for validating note update payloads."""
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=False, validate=validate.Length(min=1, max=200), metadata={"description": "Title of the note"})
    content = fields.String(required=False, validate=validate.Length(min=1), metadata={"description": "Content of the note"})


class NoteSchema(Schema):
    """Schema for serializing a Note."""
    id = fields.String(required=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
