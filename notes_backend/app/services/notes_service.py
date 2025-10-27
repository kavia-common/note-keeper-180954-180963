import uuid
from datetime import datetime
from typing import Dict, List, Optional

from ..models.note import Note


class NotesServiceInterface:
    """Interface for notes data operations to support swapping storage backends."""

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """Return all notes in reverse chronological order."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a single note by its ID, or None if not found."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def create_note(self, title: str, content: str) -> Note:
        """Create a new note with the given title and content."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def update_note(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
        """Update an existing note's title and/or content; returns updated note or None if not found."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID; returns True if deleted, False if not found."""
        raise NotImplementedError


class InMemoryNotesService(NotesServiceInterface):
    """Simple in-memory implementation useful for development and testing."""

    def __init__(self, seed: bool = True):
        self._store: Dict[str, Note] = {}
        if seed:
            self._seed_data()

    def _seed_data(self):
        examples = [
            ("Welcome", "This is your first note. Feel free to edit or delete it."),
            ("Ideas", "• Build a notes app\n• Add search\n• Support tags"),
        ]
        for title, content in examples:
            self.create_note(title, content)

    def list_notes(self) -> List[Note]:
        return sorted(self._store.values(), key=lambda n: n.updated_at, reverse=True)

    def get_note(self, note_id: str) -> Optional[Note]:
        return self._store.get(note_id)

    def create_note(self, title: str, content: str) -> Note:
        note_id = str(uuid.uuid4())
        now = datetime.utcnow()
        note = Note(id=note_id, title=title, content=content, created_at=now, updated_at=now)
        self._store[note_id] = note
        return note

    def update_note(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
        note = self._store.get(note_id)
        if not note:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = datetime.utcnow()
        self._store[note_id] = note
        return note

    def delete_note(self, note_id: str) -> bool:
        return self._store.pop(note_id, None) is not None


# Factory for selecting backend (extend later to support DB using env vars)
def get_notes_service() -> NotesServiceInterface:
    """
    PUBLIC_INTERFACE
    Return the active notes service implementation.

    This is currently an in-memory implementation. In the future, this can be
    extended to read environment variables and return a database-backed service
    without changing route code.
    """
    # Placeholder for future selection logic, e.g., based on env like NOTES_BACKEND=memory|db
    return InMemoryNotesService(seed=True)
