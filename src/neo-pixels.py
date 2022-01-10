# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# This code is based on the article: Arduino – Controlling a WS2812 LED strand with NeoPixel or FastLED
# (https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/#LEDStripEffectColorWipe)
# ------------------------------------------------------------------------------------------

from microbit import sleep, display, button_b, pin1
from neopixel import NeoPixel
from random import randint
from math import sin, sqrt
from utime import ticks_ms, ticks_diff

class NeoPixels:
    def __init__(self, pin, num_pixels = 30):
        self._num_pixels = num_pixels
        self._strip = NeoPixel(pin, num_pixels)
        self.clear()
        
    def _wheel(self, wheel_pos):
        c = bytearray(3)
        
        if wheel_pos < 85:
            c[0] = wheel_pos * 3
            c[1] = 255 - wheel_pos * 3
            c[2] = 0
        elif wheel_pos < 170:
            wheel_pos -= 85
            c[0] = 255 - wheel_pos * 3
            c[1] = 0
            c[2] = wheel_pos * 3
        else:
            wheel_pos -= 170
            c[0] = 0
            c[1] = wheel_pos * 3
            c[2] = 255 - wheel_pos * 3
            
        return c
    
    def _set_pixel_heat_color(self, pixel, temperature):
        t192 = round((temperature / 255.0) * 191)
        
        heatramp = t192 & 0x3F
        heatramp <<= 2
        
        if t192 > 0x80:
            self.set_pixel(pixel, 255, 255, heatramp)
        elif t192 > 0x40:
            self.set_pixel(pixel, 255, heatramp, 0)
        else:
            self.set_pixel(pixel, heatramp, 0, 0)
            
    def _fade_to_black(self, pixel, fade_value): 
        old_color = self._strip[pixel]
        
        red = old_color[0]
        if red <= 10:
            red = 0
        else:
            red = int(round(red - (red * fade_value / 256)))
 
        green = old_color[1]
        if green <= 10:
            green = 0
        else:
            green = int(round(green - (green * fade_value / 256)))
             
        blue = old_color[2]
        if blue <= 10:
            blue = 0
        else:
            blue = int(round(blue - (blue * fade_value / 256)))
            
        self.set_pixel(pixel, red, green, blue)
 
    def get_number_pixels(self):
        return self._num_pixels
     
    def clear(self):
        self._strip.clear()
    
    def fill(self, red, green, blue):
        self._strip.fill((int(round(red)), int(round(green)), int(round(blue))))
    
    def set_pixel(self, index, red, green, blue):
        self._strip[index] = (int(round(red)), int(round(green)), int(round(blue)))
    
    def get_pixel(self, index):
        return self._strip[index]
     
    def show(self):
        self._strip.show()
    
    def fade(self):
        self.fade_in_out(0xFF, 0x00, 0x00)
        self.fade_in_out(0x00, 0xFF, 0x00)
        self.fade_in_out(0x00, 0x00, 0xFF)
        
    def fade_in_out(self, red, green, blue):
        for k in range(255):
            r = (k / 256.0) * red
            g = (k / 256.0) * green
            b = (k / 256.0) * blue
            
            self.fill(r, g, b)
            self.show()
            
        for k in range(255, 0, -1):
            r = (k / 256.0) * red
            g = (k / 256.0) * green
            b = (k / 256.0) * blue
            
            self.fill(int(r), int(g), int(b))
            self.show()
        
    def strobe(self, red, green, blue, strobe_count, flash_delay, end_pause):
        for j in range(strobe_count):
            self.fill(red, green, blue)
            self.show()
            sleep(flash_delay)
            self.fill(0x00, 0x00, 0x00)
            self.show()
            sleep(flash_delay)
            
        sleep(end_pause)
        
    def halloween_eyes(self, red, green, blue, eye_width, eye_space, fade, steps, fade_delay, end_pause):
        start_point = randint(0, self._num_pixels - (2 * eye_width) - eye_space)
        start_2nd_eye = start_point + eye_width + eye_space
    
        for i in range(eye_width):
            self.set_pixel(start_point + i, red, green, blue)
            self.set_pixel(start_2nd_eye + i, red, green, blue)
            
        self.show()
        
        if fade:
            for j in range(steps):
                r = j * (red / steps)
                g = j * (green / steps)
                b = j * (blue / steps)
                
                for i in range(eye_width):
                    self.set_pixel(start_point + i, r, g, b)
                    self.set_pixel(start_2nd_eye + i, r, g, b)
                    
                self.show()
                sleep(fade_delay)
                
        self.fill(0, 0, 0)
        self.show()
        
        sleep(end_pause)
        
    def cylon(self, red, green, blue, eye_size, speed_delay, return_delay):
        pixel_range = self._num_pixels - eye_size - 2
        
        for i in range(pixel_range):
            self.fill(0x0, 0x0, 0x0)
            self.set_pixel(i, red / 10, green / 10, blue / 10)
            
            for j in range(1, eye_size):
                self.set_pixel(i + j, red, green, blue)
            
            self.set_pixel(i + eye_size + 1, red / 10, green / 10, blue / 10);
            self.show()
            sleep(speed_delay)
            
        sleep(return_delay)
        
        for i in range(pixel_range, 0, -1):
            self.fill(0x0, 0x0, 0x0)
            self.set_pixel(i, red / 10, green / 10, blue / 10)

            for j in range(1, eye_size):
                self.set_pixel(i + j, red, green, blue)

            self.set_pixel(i + eye_size + 1, red / 10, green / 10, blue / 10);
            self.show()
            sleep(speed_delay)
            
        sleep(return_delay)
                
    def center_to_outside(self, red, green, blue, eye_size, speed_delay, return_delay):
        pixel_range = int(round((self._num_pixels - eye_size) / 2))
        
        for i in range(pixel_range, 0, -1):
            self.fill(0x0, 0x0, 0x0)
            self.set_pixel(i, red / 10, green / 10, blue / 10)
            
            for j in range(1, eye_size):
                self.set_pixel(i + j, red, green, blue)
    
            self.set_pixel(i + eye_size + 1, red / 10, green / 10, blue / 10)
            
            self.set_pixel(self._num_pixels - i, red / 10, green / 10, blue / 10)
   
            for j in range(1, eye_size):
                self.set_pixel(self._num_pixels - i - j, red, green, blue)
 
            self.set_pixel(self._num_pixels - i - eye_size - 1, red / 10, green / 10, blue / 10)
   
            self.show()
            sleep(speed_delay)
            
        sleep(return_delay)
 
    def outside_to_center(self, red, green, blue, eye_size, speed_delay, return_delay):
        pixel_range = int(round((self._num_pixels - eye_size) / 2))
        
        for i in range(pixel_range):
            self.fill(0x0, 0x0, 0x0)
            self.set_pixel(i, red / 10, green / 10, blue / 10)
            
            for j in range(1, eye_size):
                self.set_pixel(i + j, red, green, blue)

            self.set_pixel(i + eye_size + 1, red / 10, green / 10, blue / 10)
             
            self.set_pixel(self._num_pixels - 1, red / 10, green / 10, blue / 10)
             
            for j in range(1, eye_size):
                self.set_pixel(self._num_pixels - i - j, red, green, blue)
 
            self.set_pixel(self._num_pixels - i - eye_size - 1, red / 10, green / 10, blue / 10)
            
            self.show()
            sleep(speed_delay)
            
        sleep(return_delay)
 
    def right_to_left(self, red, green, blue, eye_size, speed_delay, return_delay):
        pixel_range = self._num_pixels - eye_size - 2
        
        for i in range(pixel_range, 0, -1):
            self.fill(0x0, 0x0, 0x0)
            self.set_pixel(i, red / 10, green / 10, blue / 10)
            
            for j in range(1, eye_size):
                self.set_pixel(i + j, red, green, blue)
   
            self.set_pixel(i + eye_size + 1, red / 10, green / 10, blue / 10);
            self.show()
            sleep(speed_delay)
                    
        sleep(return_delay)
        
    def left_to_right(self, red, green, blue, eye_size, speed_delay, return_delay):
        pixel_range = self._num_pixels - eye_size - 2
        
        for i in range(pixel_range):
            self.fill(0x0, 0x0, 0x0)
            self.set_pixel(i, red / 10, green / 10, blue / 10)
            
            for j in range(1, eye_size):
                self.set_pixel(i + j, red, green, blue)
   
            self.set_pixel(i + eye_size + 1, red / 10, green / 10, blue / 10);
            self.show()
            sleep(speed_delay)
            
        sleep(return_delay)
        
    def kitt(self, red, green, blue, eye_size, speed_delay, return_delay):
        self.right_to_left(red, green, blue, eye_size, speed_delay, return_delay)
        self.left_to_right(red, green, blue, eye_size, speed_delay, return_delay)
        self.outside_to_center(red, green, blue, eye_size, speed_delay, return_delay)
        self.center_to_outside(red, green, blue, eye_size, speed_delay, return_delay)
        self.left_to_right(red, green, blue, eye_size, speed_delay, return_delay)
        self.right_to_left(red, green, blue, eye_size, speed_delay, return_delay)
        self.outside_to_center(red, green, blue, eye_size, speed_delay, return_delay)
        self.center_to_outside(red, green, blue, eye_size, speed_delay, return_delay)
 
    def twinkle(self, red, green, blue, count, speed_delay, only_one):
        self.fill(0x0, 0x0, 0x0)
        
        for i in range(count):
            self.set_pixel(randint(0, self._num_pixels - 1), red / 10, green / 10, blue / 10)
            self.show()
            
            sleep(speed_delay)
            
            if only_one:
                self.fill(0x0, 0x0, 0x0)
        
        sleep(speed_delay)
            
    def twinkle_random(self, count, speed_delay, only_one):
        self.fill(0x0, 0x0, 0x0)
        
        for i in range(count):
            self.set_pixel(randint(0, self._num_pixels - 1), randint(0, 255), randint(0, 255), randint(0, 255))
            self.show()
            
            sleep(speed_delay)
            
            if only_one:
                self.fill(0x0, 0x0, 0x0)
                
        sleep(speed_delay)
     
    def sparkle(self, red, green, blue, speed_delay):
        pixel = randint(0, self._num_pixels - 1)
        
        self.set_pixel(pixel, red, green, blue)
        self.show()
        sleep(speed_delay)
        self.set_pixel(pixel, 0x0, 0x0, 0x0)
        
    def snow_sparkle(self, red, green, blue, sparkle_delay, speed_delay):
        self.fill(red, green, blue)
        
        pixel = randint(0, self._num_pixels - 1)
        self.set_pixel(pixel, 0xFF, 0xFF, 0xFF)
        self.show()
        
        sleep(speed_delay)
        
        self.set_pixel(pixel, red, green, blue)
        self.show()
        
        sleep(speed_delay)
        
    def running_lights(self, red, green, blue, wave_delay):
        position = 0
        pixel_range = self._num_pixels * 2
        
        for j in range(pixel_range):
            position += 1
            
            for i in range(self._num_pixels):
                r = int(round(((sin(i + position) * 127 + 128) / 255) * red))
                g = int(round(((sin(i + position) * 127 + 128) / 255) * green))
                b = int(round(((sin(i + position) * 127 + 128) / 255) * blue))
                
                self.set_pixel(i, r, g, b)
                
            self.show()
            sleep(wave_delay)
        
    def color_wipe(self, red, green, blue, speed_delay):
        for i in range(self._num_pixels):
            self.set_pixel(i, red, green, blue)
            self.show()
            sleep(speed_delay)
    
    def rainbow_cycle(self, speed_delay):
        for j in range(256 * 5):
            for i in range(self._num_pixels):
                wheel_pos = int(((i * 256 / self._num_pixels) + j)) & 255
                c = self._wheel(wheel_pos)
                
                self.set_pixel(i, c[0], c[1], c[2])
            self.show()
            sleep(speed_delay)
    
    def theater_chase(self, red, green, blue, speed_delay):
        for j in range(10):
            for q in range(3):
                for i in range(0, self._num_pixels, 3):
                    self.set_pixel(i + q, red, green, blue)
                self.show()
                sleep(speed_delay)
                
                for i in range(0, self._num_pixels, 3):
                    self.set_pixel(i + q, 0x00, 0x00, 0x00)
              
    def theater_chase_rainbow(self, speed_delay):
        for j in range(256):
            for q in range(3):
                for i in range(0, self._num_pixels, 3):
                    wheel_pos = (i + j) % 255
                    c = self._wheel(wheel_pos)
                    self.set_pixel(i + q, c[0], c[1], c[2])
                self.show()
                
                sleep(speed_delay)
                
                for i in range(0, self._num_pixels, 3):
                    self.set_pixel(i + q, 0x00, 0x00, 0x00)
    
    def bouncing_balls(self, red, green, blue, ball_count):
        gravity = -9.81
        start_height = 1
        height = [0.0] * ball_count
        impact_velocity_start = sqrt(-2 * gravity * start_height)
        impact_velocity = [0.0] * ball_count
        time_since_last_bounce = [0.0] * ball_count
        position = [0] * ball_count
        clock_time_since_last_bounce = [0] * ball_count
        dampening = [0.0] * ball_count
        
        for i in range(ball_count):
            clock_time_since_last_bounce[i] = ticks_ms()
            height[i] = start_height
            position[i] = 0
            impact_velocity[i] = impact_velocity_start
            time_since_last_bounce[i] = 0
            dampening[i] = 0.90 - float(i) / pow(ball_count, 2)
        
        while True:
            for i in range(ball_count):
                time_since_last_bounce[i] = ticks_diff(ticks_ms(), clock_time_since_last_bounce[i])
                height[i] = 0.5 * gravity * pow(time_since_last_bounce[i] / 1000 , 2.0 ) + impact_velocity[i] * time_since_last_bounce[i] / 1000
                
                if height[i] < 0:
                    height[i] = 0
                    impact_velocity[i] = dampening[i] * impact_velocity[i]
                    clock_time_since_last_bounce[i] = ticks_ms()
                    
                    if impact_velocity[i] < 0.01:
                        impact_velocity[i] = impact_velocity_start
                        
                position[i] = round(height[i] * (self._num_pixels - 1) / start_height)
                
            for i in range(ball_count):
                self.set_pixel(position[i], red, green, blue)
                
            self.show()
            self.fill(0x00, 0x00, 0x00)
        
    def bouncing_colored_balls(self, ball_count, colors):
        gravity = -9.81
        start_height = 1
        height = [0.0] * ball_count
        impact_velocity_start = sqrt(-2 * gravity * start_height)
        impact_velocity = [0.0] * ball_count
        time_since_last_bounce = [0.0] * ball_count
        position = [0] * ball_count
        clock_time_since_last_bounce = [0] * ball_count
        dampening = [0.0] * ball_count
        
        for i in range(ball_count):
            clock_time_since_last_bounce[i] = ticks_ms()
            height[i] = start_height
            position[i] = 0
            impact_velocity[i] = impact_velocity_start
            time_since_last_bounce[i] = 0
            dampening[i] = 0.90 - float(i) / pow(ball_count, 2)
            
        while True:
            for i in range(ball_count):
                time_since_last_bounce[i] = ticks_diff(ticks_ms(), clock_time_since_last_bounce[i])
                height[i] = 0.5 * gravity * pow(time_since_last_bounce[i] / 1000 , 2.0 ) + impact_velocity[i] * time_since_last_bounce[i] / 1000
                
                if height[i] < 0:
                    height[i] = 0
                    impact_velocity[i] = dampening[i] * impact_velocity[i]
                    clock_time_since_last_bounce[i] = ticks_ms()
                    
                    if impact_velocity[i] < 0.01:
                        impact_velocity[i] = impact_velocity_start
                        
                position[i] = round(height[i] * (self._num_pixels - 1) / start_height)
                
            for i in range(ball_count):
                self.set_pixel(position[i], colors[i][0], colors[i][1], colors[i][2])
                
            self.show()
            self.fill(0x00, 0x00, 0x00)
    
    def meteor_rain(self, red, green, blue, meteor_size, meteor_trail_decay, meteor_random_decay, speed_delay):
        self.fill(0x00, 0x00, 0x00)
        
        for i in range(self._num_pixels * 2):
            for j in range(self._num_pixels):
                if not meteor_random_decay or randint(0, 10) > 5:
                    self._fade_to_black(j, meteor_trail_decay)
                
            for j in range(meteor_size):
                if i - j < self._num_pixels and i - j >= 0:
                    self.set_pixel(i - j, red, green, blue)
                    
            self.show()
            sleep(speed_delay)
            
    def fire(self, cooling, sparking, speed_delay):
        heat = bytearray(self._num_pixels)
        
        for i in range(self._num_pixels):
            cooldown = randint(0, int(round(((cooling * 10) / self._num_pixels) + 2)))
            
            if cooldown > heat[i]:
                heat[i] = 0
            else:
                heat[i] = heat[i] - cooldown
                
        
        for k in range(self._num_pixels - 1, 2, -1):
            heat[k] = int(round((heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3))
            
        if randint(0, 255) < sparking:
            y = randint(0, 7)
            heat[y] = heat[y] + randint(160, 255)
        
        for j in range(self._num_pixels):
            self._set_pixel_heat_color(j, heat[j])
            
        self.show() 
        sleep(speed_delay) 
          
def main():
    display.clear()
    display.show('>')
    
    strip = NeoPixels(pin1)
    
    while True:
        if button_b.was_pressed():
            break
            
        print('Fire')
        strip.fire(55, 120, 15)
        sleep(1000)
        strip.clear() 
  
    strip.clear()
    display.clear()
     
if __name__ == '__main__':
    main()
    