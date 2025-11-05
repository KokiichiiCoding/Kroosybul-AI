"""
Session Manager for Kroosybul AI
Handles persistent storage of project sessions, allowing users to save and resume work.
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class SessionManager:
    """Manages persistent storage of project sessions"""

    def __init__(self, db_path: str = "sessions.db"):
        """Initialize the session manager with a SQLite database

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                project_name TEXT NOT NULL,
                description TEXT,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                project_path TEXT,
                status TEXT DEFAULT 'active',
                metadata TEXT
            )
        """)

        # Create messages table for chat history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        """)

        # Create iterations table for tracking project changes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iterations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                iteration_number INTEGER NOT NULL,
                description TEXT,
                changes TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        """)

        conn.commit()
        conn.close()

    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save or update a session

        Args:
            session_id: Unique identifier for the session
            session_data: Dictionary containing session information

        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Extract relevant data
            project = session_data.get('current_project', {})
            metadata = {
                'messages': session_data.get('messages', []),
                'files': project.get('files', []),
                'dependencies': project.get('dependencies', []),
                'frameworks': project.get('frameworks', []),
                'test_results': project.get('test_results', {})
            }

            # Check if session exists
            cursor.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
            exists = cursor.fetchone() is not None

            if exists:
                # Update existing session
                cursor.execute("""
                    UPDATE sessions
                    SET project_name = ?,
                        description = ?,
                        language = ?,
                        updated_at = CURRENT_TIMESTAMP,
                        project_path = ?,
                        metadata = ?
                    WHERE session_id = ?
                """, (
                    project.get('name', 'Untitled Project'),
                    project.get('description', ''),
                    project.get('language', ''),
                    project.get('path', ''),
                    json.dumps(metadata),
                    session_id
                ))
            else:
                # Insert new session
                cursor.execute("""
                    INSERT INTO sessions (session_id, project_name, description, language, project_path, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    project.get('name', 'Untitled Project'),
                    project.get('description', ''),
                    project.get('language', ''),
                    project.get('path', ''),
                    json.dumps(metadata)
                ))

            # Save messages
            for msg in session_data.get('messages', []):
                cursor.execute("""
                    INSERT INTO messages (session_id, role, content)
                    VALUES (?, ?, ?)
                """, (session_id, msg.get('role', 'user'), msg.get('content', '')))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session by ID

        Args:
            session_id: Unique identifier for the session

        Returns:
            Session data dictionary or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get session data
            cursor.execute("""
                SELECT * FROM sessions WHERE session_id = ?
            """, (session_id,))

            row = cursor.fetchone()
            if not row:
                conn.close()
                return None

            # Parse metadata
            metadata = json.loads(row['metadata']) if row['metadata'] else {}

            # Get messages
            cursor.execute("""
                SELECT role, content, timestamp
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp ASC
            """, (session_id,))

            messages = [dict(msg) for msg in cursor.fetchall()]

            # Get iterations
            cursor.execute("""
                SELECT * FROM iterations
                WHERE session_id = ?
                ORDER BY iteration_number ASC
            """, (session_id,))

            iterations = [dict(it) for it in cursor.fetchall()]

            conn.close()

            # Reconstruct session data
            session_data = {
                'session_id': row['session_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'current_project': {
                    'name': row['project_name'],
                    'description': row['description'],
                    'language': row['language'],
                    'path': row['project_path'],
                    'files': metadata.get('files', []),
                    'dependencies': metadata.get('dependencies', []),
                    'frameworks': metadata.get('frameworks', []),
                    'test_results': metadata.get('test_results', {})
                },
                'messages': messages,
                'iterations': iterations,
                'status': row['status']
            }

            return session_data
        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def list_sessions(self, limit: int = 50, status: str = 'active') -> List[Dict[str, Any]]:
        """List all saved sessions

        Args:
            limit: Maximum number of sessions to return
            status: Filter by status (active, archived, completed)

        Returns:
            List of session summaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if status:
                cursor.execute("""
                    SELECT session_id, project_name, description, language,
                           created_at, updated_at, status
                    FROM sessions
                    WHERE status = ?
                    ORDER BY updated_at DESC
                    LIMIT ?
                """, (status, limit))
            else:
                cursor.execute("""
                    SELECT session_id, project_name, description, language,
                           created_at, updated_at, status
                    FROM sessions
                    ORDER BY updated_at DESC
                    LIMIT ?
                """, (limit,))

            sessions = [dict(row) for row in cursor.fetchall()]
            conn.close()

            return sessions
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []

    def delete_session(self, session_id: str) -> bool:
        """Delete a session and all associated data

        Args:
            session_id: Unique identifier for the session

        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Delete messages
            cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))

            # Delete iterations
            cursor.execute("DELETE FROM iterations WHERE session_id = ?", (session_id,))

            # Delete session
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    def save_iteration(self, session_id: str, iteration_number: int,
                      description: str, changes: List[Dict[str, Any]]) -> bool:
        """Save an iteration/refinement of the project

        Args:
            session_id: Unique identifier for the session
            iteration_number: The iteration number
            description: Description of changes made
            changes: List of file changes

        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO iterations (session_id, iteration_number, description, changes)
                VALUES (?, ?, ?, ?)
            """, (session_id, iteration_number, description, json.dumps(changes)))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving iteration: {e}")
            return False

    def update_session_status(self, session_id: str, status: str) -> bool:
        """Update the status of a session

        Args:
            session_id: Unique identifier for the session
            status: New status (active, archived, completed)

        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE sessions
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """, (status, session_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating session status: {e}")
            return False
