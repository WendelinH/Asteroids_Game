import os
import sqlite3

from constants import BASE_PATH
from score import Score

class ScoreDatabase:
    def __init__(self, db_path="scores.db"):
        self.db_path = os.path.join(BASE_PATH, db_path)
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_score(self, player_name=None):
        if player_name is None:
            player_name = os.getlogin()
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO scores (player_name, score) VALUES (?, ?)",
            (player_name, Score().get_value())
        )
        
        conn.commit()
        conn.close()
    
    def get_all_scores(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT player_name, score, timestamp FROM scores ORDER BY score DESC")
        scores = cursor.fetchall()
        
        conn.close()
        return scores
    
    def get_top_scores(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT player_name, score, timestamp FROM scores ORDER BY score DESC LIMIT ?",
            (limit,)
        )
        scores = cursor.fetchall()
        
        conn.close()
        return scores
    
    def get_high_score(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT MAX(score) FROM scores")
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result[0] is not None else 0
