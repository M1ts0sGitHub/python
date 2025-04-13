import keyboard, time, os
import pygame

class pomotimer():
    def __init__(self,ftime,btime,autoplay,sound) -> None:
        self.ftime_max, self.btime_max = ftime*60, btime*60
        self.ftime, self.btime = self.ftime_max, self.btime_max
        self.mode = "focus"
        self.running = 1
        self.autoplay = autoplay
        self.sound = sound
    def play_pause(self):
        self.running = (self.running + 1) % 2
    def skip(self):
        self.ftime, self.btime = self.ftime_max, self.btime_max
        if self.autoplay == 1:
            if self.mode == "focus":
                self.mode = "break"
            else:
                self.mode = "focus"
        else:
            self.running = 0
            if self.mode == "focus":
                self.mode = "break"
            else:
                self.mode = "focus"
    def reset(self):
        self.ftime, self.btime = self.ftime_max, self.btime_max
        self.mode = "focus"
        self.running = 0
        self.autoplay = 0
        self.sound = 1
    def update(self):
        if self.running:
            if self.mode == "focus" and self.ftime > 0:
                self.ftime -= 1
            elif self.mode == "break" and self.btime > 0:
                self.btime -= 1
            elif self.ftime <= 0 or self.btime <= 0:
                if self.sound == 1 and self.mode == "focus":
                    pygame.mixer.music.load(r"focus.wav")
                    pygame.mixer.music.play()
                elif self.sound == 1 and self.mode == "break":
                    pygame.mixer.music.load(r"break.wav")
                    pygame.mixer.music.play()
                self.skip()
    def autoplay_change(self):
        self.autoplay = (self.autoplay + 1) % 2
    def print(self):
        os.system('cls')
        # print('Pomotime - Cli edition')
        # print('')
        # print('(a) Autoplay,  (p) Play - Resume, (s) Skip, (r) Reset')
        # print('')
        if self.mode == "focus":
            print(f'Focus Time: {self.ftime//60}:{self.ftime%60:02d}')
        else:
            print(f'Brake Time: {self.btime//60}:{self.btime%60:02d}')


pygame.mixer.init()
os.system('title Pomotime - Cli Edition')
running = True
p = pomotimer(25,5,1,1)
t1 = time.time()
ticks = 0
while running:
    if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
        running = False
    elif keyboard.is_pressed('right'):
        p.skip()
    elif keyboard.is_pressed('space'):
        p.play_pause()
    elif keyboard.is_pressed('left'):
        p.reset()
    elif keyboard.is_pressed('a'):
        p.autoplay_change()
    elif keyboard.is_pressed('s'):
        p.sound = (p.sound + 1) % 2

    ticks += 1
    if ticks >= 100:
        ticks = 0
        p.update()
        p.print()
    time.sleep(1/100.0)