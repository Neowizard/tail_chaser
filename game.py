import time
import os
from machine import Pin
import _thread
import highscore

class Game:
    def __init__(self, led_runner, oled, buttons):
        self._oled = oled
        self._led_runner = led_runner
        self._buttons = buttons
        self._highscore = highscore.Highscore(self._oled)
        self._score = 0        
    
    
    def play(self, rounds):
        # Using busy loop to query inputs instead of IRQ, since MicroPython
        # tends to crash when Using IRQ and threads (in the LED runner)
        # simultaniusly and I'm not sure why.
        while True:
            if self._buttons.start.value() == 0:
                self._start(rounds)
                break           
        self._highscore.show_highscores(rounds, self._score)
        
    
    def _start(self, rounds):
        played_rounds = 0
        
        self._display_score(score=self._score, round_score=None)
        self._run_leds()
        while True:
            if self._buttons.stop.value() == 0:
                played_rounds += 1
                round_score = self._stop_round()
                self._score += round_score
                print(f'Score = {self._score}, round score = {round_score}')
                self._display_score(score=self._score, round_score=round_score)
                time.sleep(1)
                
                if played_rounds >= rounds:
                    break
                
                self._display_score(score=self._score, round_score=None)
                self._run_leds()
        self._led_runner.stop()
            
    
    def _stop_round(self):
        
        self._led_runner.stop()
        print(f'Stopping LEDs ({self._led_runner.state})')
        round_score = self._state_score(self._led_runner.state)
        return round_score
           
           
    def _state_score(self, state):
        leds_count = len(self._led_runner.cols) * len(self._led_runner.rows)
        selected_led_idx = len(self._led_runner.cols) * state.row + state.col
        score = (leds_count/2 - abs(selected_led_idx - leds_count/2))*10
        return int(score)
    
    
    def _display_score(self, score, round_score):
        self._oled.fill(0)
        self._oled.text('Score:', 0, 0)
        self._oled.text(str(score), 4, 16)
        if round_score is not None:
            self._oled.text(f'+{round_score}',4, 24)    

        self._oled.show()


    def _run_leds(self):
        print('Starting LEDs')
        _thread.start_new_thread(self._led_runner.run_leds, ())

        