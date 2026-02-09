"""
Database connection module for Neon PostgreSQL
"""

import os
from typing import Generator
from contextlib import contextmanager
import logging

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import SimpleConnectionPool
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False
    logging.warning("psycopg2 not installed. Database features will not work.")

logger = logging.getLogger(__name__)

# Database connection pool
_pool = None


def get_connection_string() -> str:
    """Get database connection string from environment."""
    conn_string = os.getenv('DATABASE_URL')
    
    if not conn_string:
        raise ValueError(
            "DATABASE_URL environment variable not set. "
            "Please set it to your Neon PostgreSQL connection string."
        )
    
    return conn_string


def init_db_pool():
    """Initialize database connection pool."""
    global _pool
    
    if not HAS_PSYCOPG2:
        raise ImportError("psycopg2-binary is required. Install with: pip install psycopg2-binary")
    
    if _pool is None:
        try:
            conn_string = get_connection_string()
            # Create connection pool (min 1, max 5 connections)
            _pool = SimpleConnectionPool(1, 5, conn_string)
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise


@contextmanager
def get_db() -> Generator:
    """
    Get database connection from pool.
    Usage:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users")
    """
    global _pool
    
    if _pool is None:
        init_db_pool()
    
    conn = None
    try:
        conn = _pool.getconn()
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            _pool.putconn(conn)


def init_db():
    """
    Initialize database - create tables if they don't exist.
    Reads schema.sql and executes it.
    """
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(schema_sql)
                conn.commit()
        
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database schema: {e}")
        raise


def test_connection() -> bool:
    """Test database connection."""
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                return result is not None
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
