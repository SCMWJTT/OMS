-- ONE comments and suggested edits. Safe to run again: it only creates what is missing.
CREATE TABLE IF NOT EXISTS notes (
  id TEXT PRIMARY KEY,
  doc TEXT NOT NULL,
  rev TEXT,
  bm TEXT NOT NULL,
  pidx INTEGER NOT NULL,
  quote TEXT,
  kind TEXT NOT NULL,
  body TEXT,
  new_text TEXT,
  author TEXT,
  created TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  status_by TEXT,
  status_at TEXT
);
CREATE INDEX IF NOT EXISTS notes_doc ON notes(doc);
CREATE TABLE IF NOT EXISTS replies (
  id TEXT PRIMARY KEY,
  note_id TEXT NOT NULL,
  author TEXT,
  body TEXT NOT NULL,
  created TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS replies_note ON replies(note_id);
