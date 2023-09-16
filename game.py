import random
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

    def play(self, rounds, cycle_seconds, step):
        # Using busy loop to query inputs instead of IRQ, since MicroPython
        # tends to crash when Using IRQ and threads (in the LED runner)
        # simultaniusly and I'm not sure why.
        while True:
            if self._buttons.start.value() == 0:
                self._start(rounds, cycle_seconds, step)
                break
        self._highscore.show_highscores(rounds, self._score)

    def _start(self, rounds, cycle_seconds, step):
        played_rounds = 0

        target = self._draw_taget()
        self._led_runner.flicker_led(target[0], target[1], 1)
        self._display_score(score=self._score, round_score=None)
        self._run_leds(cycle_seconds)
        cycle_seconds -= step

        while True:
            if self._buttons.stop.value() == 0:
                played_rounds += 1
                self._stop_round()
                round_score = self._state_score(self._led_runner.state, target)
                self._score += round_score
                print(f'Score = {self._score}, round score #{played_rounds} = {round_score}')
                self._display_score(score=self._score, round_score=round_score)
                time.sleep(1)

                if played_rounds >= rounds:
                    break

                self._display_score(score=self._score, round_score=None)
                target = self._draw_taget()
                self._led_runner.flicker_led(target[0], target[1], 1)
                self._run_leds(cycle_seconds)
                cycle_seconds -= step
        self._led_runner.stop()

    def _draw_taget(self):
        target_col = random.randint(0, len(self._led_runner.cols) - 1)
        target_row = random.randint(0, len(self._led_runner.rows) - 1)
        return (target_col, target_row)

    def _stop_round(self):
        self._led_runner.stop()
        print(f'Stopping LEDs ({self._led_runner.state})')

    def _state_score(self, state, target):
        leds_count = len(self._led_runner.cols) * len(self._led_runner.rows)
        selected_led_idx = len(self._led_runner.cols) * state.row + state.col
        target_led_idx = len(self._led_runner.cols) * target[0] + target[1]
        distance = abs(selected_led_idx - target_led_idx)
        score = leds_count / 2 - (leds_count - distance if distance > 18 else distance)
        return int(score * 10)

    def _display_score(self, score, round_score):
        self._oled.fill(0)
        self._oled.text('Score:', 0, 0)
        self._oled.text(str(score), 4, 16)
        if round_score is not None:
            self._oled.text(f'+{round_score}', 4, 24)

        self._oled.show()

    def _run_leds(self, cycle_seconds):
        print('Starting LEDs')
        _thread.start_new_thread(self._led_runner.run_leds, (cycle_seconds,))
