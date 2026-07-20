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
        self._value
    
    def reset(self):
        self._value = 0
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font, color):
        score_text = font.render(f"Score: {self._value}", True, color)
        
        text_rect = score_text.get_rect()
        text_rect.centerx = screen.get_width() // 2
        text_rect.top = 20
        
        screen.blit(score_text, text_rect)



s1 = Score()