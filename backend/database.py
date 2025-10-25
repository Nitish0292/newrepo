"""Database helper for backend.

Encapsulates connection to MongoDB and provides a small API used by routes.
"""
import os
from typing import Optional

import pymongo

_client: Optional[pymongo.MongoClient] = None
_db: Optional[pymongo.database.Database] = None
_collection_name = os.getenv('MONGO_COLLECTION_NAME', 'flasktutorial')


def init_db():
    """Initialize the Mongo client and database using `MONGO_URL`.

    After calling this, `get_collection()` will return a Collection object or
    None if initialization failed.
    """
    global _client, _db
    if _client is not None:
        return True

    mongo_url = os.getenv('MONGO_URL') or os.getenv('MONGO_URL')
    if not mongo_url:
        # nothing to do — env not set
        return False

    try:
        _client = pymongo.MongoClient(mongo_url)
        # default DB name from env or fallback
        db_name = os.getenv('MONGO_DB_NAME', 'assessmentdb')
        _db = _client[db_name]
        return True
    except Exception:
        _client = None
        _db = None
        return False


def get_collection(name: Optional[str] = None):
    """Return the configured collection or None if not available.

    If `name` is provided, return that collection name; otherwise return the
    default collection configured by `_collection_name`.
    """
    if _db is None:
        return None
    collection_name = name if name else _collection_name
    return _db[collection_name]
