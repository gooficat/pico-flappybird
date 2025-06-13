from machine import Pin, I2C
import ssd1306
import time
import random

i2c = I2C(sda=Pin(0), scl=Pin(1))
btn = Pin(2, Pin.IN)

display = ssd1306.SSD1306_I2C(128, 64, i2c)


class Bird:
    x = 64.0
    y = 32.0
    vel = 0.0
    def update(self):
        self.y += self.vel
        self.vel += 0.1
    def draw(self):
        display.pixel(int(self.x), int(self.y), 1)
    def hop(self):
        self.vel = -1.2

class PipeColumn:
    def __init__(self, x):
        self.x = x
        self.top_y = random.randint(0, 16)
        self.low_y = self.top_y + 48
    def draw(self):
        display.rect(self.x, 16, 8, self.top_y, 1)
        display.rect(self.x, self.low_y, 8, 64-self.low_y, 1)
        
        
bird = Bird()

btnpressed = False

pipes = {}

score = 0
playing = True


for i in range(4):
    pipes[i] = (PipeColumn(128 + i * 32))
    pipes[i].draw()

display.fill(0)
display.text('READY', 32, 32, 1)
display.show()
time.sleep(1)
display.fill(0)
display.text('SET', 32, 32, 1)
display.show()
time.sleep(1)
display.fill(0)
display.text('GO!', 32, 32, 1)
display.show()
time.sleep(1)
    

try:
    while playing:
        if btn.value():
            btnpressed = True
        elif btnpressed == True:
            bird.hop()
            btnpressed = False
        
        bird.update()
        
        if bird.y > 72 or bird.y < 16:
            playing = False
        
        display.fill(0)
        
        for i in pipes:
            if pipes[i].x <= -8:
                pipes[i] = PipeColumn(128)
                score += 1
            pipes[i].draw()
            pipes[i].x -= 1 + int(score/10)
            if (bird.y > pipes[i].low_y) or (bird.y < pipes[i].top_y+16):
                if pipes[i].x < bird.x and pipes[i].x+8 > bird.x:
                    playing = False
        bird.draw()
        
        display.text('score:' + str(score), 0, 0, 1)
        
        display.show()
        
    
except KeyboardInterrupt:
    display.poweroff()

try:
    display.text('GAMEOVER', 32, 32, 1)
    display.show()
    time.sleep(5)
    display.poweroff()
except KeyboardInterrupt:
    display.poweroff()
