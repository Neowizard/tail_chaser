from machine import Pin
from collections import namedtuple
import time

state = namedtuple('State', ['row', 'col'])

class LedMultiplex:
    def __init__(self, rows, cols, cycle_time, led_duty_cycle):
        self.cols = cols
        self.rows = rows
        self._cycle_time = cycle_time
        self._led_duty_cycle = led_duty_cycle
        
        self._reset_state()           

    def _reset_state(self):
        self.state = state(0, 0)
        for row in self.rows:
            row.off()
            
        for col in self.cols:
            col.on()
            

    def run_leds(self):
        self._stopped = False
        self._reset_state()
        self._run = True
        
        
        led_count = len(self.rows) * len(self.cols)
        led_time = self._cycle_time/led_count
        on_time = led_time*self._led_duty_cycle/100
        off_time = led_time - on_time
        
        while self._run:
            for row, row_led in enumerate(self.rows):                
                for col, col_led in enumerate(self.cols):
                    self.state = state(row, col)
                    self._led_on(row_led, col_led)
                    
                    
                    time.sleep(on_time)
                    
                    if not self._run:
                        print(self.state)
                        break
                    
                    self._led_off(row_led, col_led)
                    time.sleep(off_time)
                if not self._run:
                    break
        
        self._stopped = True
        
    def _led_on(self, row, col):
        row.on()
        col.off()
    
    def _led_off(self, row, col):
        row.off()
        col.on()
                
    def stop(self):
        print(f'Stopping LED run')
        self._run = False
        while not self._stopped:
            pass
        print(f'Stopped')
        time.sleep(0.01) # Let the system clear any resource used by `run_leds`
