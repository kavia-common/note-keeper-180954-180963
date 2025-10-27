from flask_smorest import Blueprint
from flask.views import MethodView

from ..models.note import NoteSchema, NoteCreateSchema, NoteUpdateSchema
from ..services.notes_service import get_notes_service

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="CRUD operations for notes"
)

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
create_schema = NoteCreateSchema()
update_schema = NoteUpdateSchema()

_service = get_notes_service()


@blp.route("")
class NotesList(MethodView):
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """
        PUBLIC_INTERFACE
        List all notes.

        Returns:
            200: Array of notes, most recently updated first.
        """
        notes = _service.list_notes()
        return notes

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema)
    def post(self, payload):
        """
        PUBLIC_INTERFACE
        Create a new note.

        Request body:
            title: string (required, 1..200)
            content: string (required)

        Returns:
            201: Created note resource.
            400: Validation error.
        """
        title = payload.get("title")
        content = payload.get("content")
        note = _service.create_note(title=title, content=content)
        return note, 201


@blp.route("/<string:note_id>")
class NoteDetail(MethodView):
    @blp.response(200, NoteSchema)
    def get(self, note_id: str):
        """
        PUBLIC_INTERFACE
        Get a note by ID.

        Params:
            note_id: string path parameter

        Returns:
            200: Note resource.
            404: If not found.
        """
        note = _service.get_note(note_id)
        if not note:
            return {"message": "Note not found"}, 404
        return note

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def put(self, payload, note_id: str):
        """
        PUBLIC_INTERFACE
        Update a note by ID.

        Request body (one or both fields required):
            title: string (1..200)
            content: string

        Returns:
            200: Updated note.
            400: Validation error.
            404: If not found.
        """
        if not payload:
            return {"message": "At least one field (title or content) must be provided"}, 400

        updated = _service.update_note(note_id, title=payload.get("title"), content=payload.get("content"))
        if not updated:
            return {"message": "Note not found"}, 404
        return updated

    def delete(self, note_id: str):
        """
        PUBLIC_INTERFACE
        Delete a note by ID.

        Returns:
            204: On success.
            404: If not found.
        """
        deleted = _service.delete_note(note_id)
        if not deleted:
            return {"message": "Note not found"}, 404
        return "", 204
