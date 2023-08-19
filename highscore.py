import json

class Highscore:
    def __init__(self, oled):
        self._oled = oled
        
    def _read_highscores(self, rounds):
        try:
            with open(f'highscores_{rounds}', 'rt') as highscores_file:
                highscores = json.load(highscores_file)
        except Exception as e:
            print(f'Failed to read highscores_{rounds}. Error: {e}')
            highscores = [0,0,0,0,0]
            
        print(f'debug: {highscores}')
        return list(highscores)
    
    def _write_highscores(self, rounds, highscores):
        highscores_json = json.dumps(highscores)
        with open(f'highscores_{rounds}', 'wt') as highscores_file:
            highscores_file.write(highscores_json)


    def _display_highscores(self, rounds, highscores, highlight_idx):
        self._oled.fill(0)
        self._oled.fill_rect(0, 0, 128, 16, 1)
        self._oled.text('Highscores:', 0, 0, 0)
        
        for idx, highscore in enumerate(highscores):
            self._oled.text(f'{idx+1}. {highscore}', 4, 16+(8*idx))
            
        if highlight_idx is not None:
            
            highlighted_rows = range(16+(8*highlight_idx), 16+(8*(highlight_idx+1)))
            for col in range(0, 128):
                for row in highlighted_rows:
                    flipped_pixel =  not self._oled.pixel(col, row)
                    self._oled.pixel(col, row, flipped_pixel)
                    
        self._oled.show()
        
        
    def show_highscores(self, rounds, new_score):
        print(f'Reading highscores for {rounds} rounds (new score = {new_score})')
        highscores = self._read_highscores(rounds)
        
        print(f'highscores = {highscores}')
        highlight_idx = None
        for idx, score in enumerate(highscores):
            if new_score > score:
                print(f'New score ({new_score}) > score #{idx} ({score})')
                highlight_idx = idx
                highscores.insert(idx, new_score)
                highscores = highscores[:5]
                break
        print(f'New highscores = {highscores}')
        
        print(f'Displaying highscores. Highlighting {highlight_idx}')
        self._display_highscores(rounds, highscores, highlight_idx)
        
        self._write_highscores(rounds, highscores)
        
