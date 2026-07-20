import pygame

from constants import SCORE_INCREASE_AMOUNT


class Score:
    def __new__(self):
        if not hasattr(self, 'inst'):
            self.inst = super().__new__(self)
            self._value = 0
        return self.inst
    
    def increase(self):
        self._value += SCORE_INCREASE_AMOUNT
    
    def get_value(self):
        return self._value
    
    def reset(self):
        self._value = 0
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, color):
        score_text = font.render(f"Score: {self._value}", True, color)
        
        text_rect = score_text.get_rect()
        text_rect.centerx = screen.get_width() // 2
        text_rect.top = 20
        
        screen.blit(score_text, text_rect)

    def draw_leaderboard(self, screen: pygame.Surface, font: pygame.font.Font, color, top_distance: int):
        from database import ScoreDatabase
        db = ScoreDatabase()
        top_scores = db.get_top_scores(9)
        
        # Title
        title_text = font.render("LEADERBOARD", True, color)
        title_rect = title_text.get_rect()
        title_rect.centerx = screen.get_width() // 2
        title_rect.top = 80 + top_distance
        screen.blit(title_text, title_rect)
        
        # Scores
        y_offset = 60 + title_rect.top
        for rank, (player_name, score, timestamp) in enumerate(top_scores, 1):
            score_text = font.render(f"{rank}. {player_name}: {score}", True, color)
            score_rect = score_text.get_rect()
            score_rect.centerx = screen.get_width() // 2
            score_rect.top = y_offset
            screen.blit(score_text, score_rect)
            y_offset += 40
