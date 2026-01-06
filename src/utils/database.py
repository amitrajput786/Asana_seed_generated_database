"""Database utility for SQLite operations"""

import sqlite3
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for Asana simulation"""
    
    def __init__(self, db_path: str = "output/asana_simulation.sqlite"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        
    def connect(self) -> sqlite3.Connection:
        """Create database connection"""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        logger.info(f"Connected to database: {self.db_path}")
        return self.conn
    
    def initialize_schema(self, schema_path: str = "schema.sql"):
        """Initialize database with schema"""
        if not self.conn:
            self.connect()
            
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            
        self.conn.executescript(schema_sql)
        self.conn.commit()
        logger.info("Database schema initialized")
        
    def insert_one(self, table: str, data: dict) -> None:
        """Insert a single row into a table"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        self.conn.execute(sql, list(data.values()))
        
    def insert_many(self, table: str, data_list: list[dict]) -> None:
        """Insert multiple rows into a table"""
        if not data_list:
            return
            
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?' for _ in data_list[0]])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        values = [list(d.values()) for d in data_list]
        self.conn.executemany(sql, values)
        self.conn.commit()
        logger.info(f"Inserted {len(data_list)} rows into {table}")
        
    def fetch_all(self, table: str) -> list[dict]:
        """Fetch all rows from a table"""
        cursor = self.conn.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def fetch_ids(self, table: str, id_column: str) -> list[str]:
        """Fetch all IDs from a table"""
        cursor = self.conn.execute(f"SELECT {id_column} FROM {table}")
        return [row[0] for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
