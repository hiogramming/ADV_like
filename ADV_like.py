import pygame
import sys
import csv
import unicodedata

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LOG = (127, 127, 127, 2)

FONT_SIZE = 30
TEXT_TURN = 910

class Message:
    def __init__(self):
        self.message = []
        self.message_r = []
        self.message_g = []
        self.message_b = []
        self.text_note = 0
        self.message_num = 1
        self.message_index = 0
        self.text = []
        self.unicode_length = 0
        self.text_row = 1
        self.log = [""]*10
        self.log_num = 0
            
    #文章読み込み
    def set_message(self,index,screen,start,end):
        
        with open(index,encoding="UTF-8") as f:
            reader = csv.reader(f)
            reader_T = [list(x) for x in zip(*reader)]
            self.message = reader_T[1]
            self.message_r = reader_T[2]
            self.message_g = reader_T[3]
            self.message_b = reader_T[4]

        self.text_note = 0
        self.message_num = start
        self.message_index = end
        self.text = ""
        self.text_length = len(self.message[self.message_num])
        self.unicode_length = 0
        self.text_row = 1
        screen_init(screen)

    #文章送り
    def next_text(self,screen):
        if self.text_length == self.text_note and self.message_num != self.message_index:

            self.log[self.log_num] = str(self.message[self.message_num])
            self.log_num = self.log_num + 1

            self.message_num = self.message_num + 1
            self.text_note = 0
            self.text_length = len(self.message[self.message_num])
            self.text = ""
            self.unicode_length = 0
            self.text_row = 1
            screen_init(screen)



    #文字送り
    def appear_text(self,screen,font):

        color = pygame.Color(int(self.message_r[self.message_num]),int(self.message_g[self.message_num]),int(self.message_b[self.message_num]))

        if self.text_note != self.text_length:

            if self.message[self.message_num][self.text_note] == "\\":
                self.text_row = self.text_row + 1
                self.unicode_length = 0
                self.text_note = self.text_note + 1

            self.text = str(self.message[self.message_num][self.text_note])
            
            if TEXT_TURN < self.unicode_length:
                self.text_row = self.text_row + 1
                self.unicode_length = 0

            sur = font.render(self.text, True, color)
            screen.blit(sur, [15 + self.unicode_length, (570-FONT_SIZE) + self.text_row * (FONT_SIZE + 1)])

            self.unicode_length = self.unicode_length + unicode_width(self.text) * (FONT_SIZE / 2) 
            self.text_note = self.text_note + 1

    def appear_log(self,screen,font):
        sur = font.render(str(self.log), True, WHITE)
        screen.blit(sur, [0, 0])

def unicode_width(s: str) -> int:
    return sum([unicodedata.east_asian_width(c) in 'WF' and 2 or 1 for c in s])

def draw_text_simple(bg, txt, x, y, fnt, r, g , b):
    color = pygame.Color(int(r),int(g),int(b))

    sur1 = fnt.render(txt, True, color)
    bg.blit(sur1, [x,y])

def screen_init(scr):
    pygame.draw.rect(scr, BLACK,[0,0,960,560])
    pygame.draw.rect(scr, WHITE,[0,560,960,160])
    pygame.draw.rect(scr, BLACK,[10,570,940,140])

def main():
    timer = 0
    wait_timer = 0
    index = 0

    pygame.init()
    pygame.display.set_caption("スクリプトテスト")
    screen = pygame.display.set_mode((960,720))
    clock = pygame.time.Clock()
    font = pygame.font.Font("data/genshingothic-20150607/GenShinGothic-Monospace-Normal.ttf", FONT_SIZE)
    debug_font = pygame.font.Font("data/genshingothic-20150607/GenShinGothic-Monospace-Light.ttf", 20)

    message_box = Message()

    while True:
        timer = timer + 1
        key = pygame.key.get_pressed()

        if index == 0:
            message_box.set_message("data/text/start.csv", screen, 1, 2)
            index = 1

        if index == 1:
            if message_box.message_num == message_box.message_index:
                if key[pygame.K_5] == 1:
                    message_box.set_message("data/text/test.csv", screen, 1, 6)
                    index = 99
                if key[pygame.K_6] == 1:
                    message_box.set_message("data/text/scenario.csv", screen, 1, 5)
                    index = 2
        
        if index == 2:
            if message_box.message_num == message_box.message_index:
                if key[pygame.K_1] == 1:
                    message_box.set_message("data/text/scenario.csv", screen, 6, 7)
                    index = 3
                if key[pygame.K_2] == 1:
                    message_box.set_message("data/text/scenario.csv", screen, 12, 17)
                    index = 99

        if index == 3:
            if message_box.message_num == message_box.message_index:
                if key[pygame.K_1] == 1:
                    message_box.set_message("data/text/scenario.csv", screen, 8, 9)
                    index = 99
                if key[pygame.K_2] == 1:
                    message_box.set_message("data/text/scenario.csv", screen, 10, 11)

        if index == 99:
            if message_box.message_num == message_box.message_index:
                if key[pygame.K_ESCAPE] == 1:
                    index = 0

        #終了、文字送りキー取得
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    message_box.next_text(screen)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    wait_timer = 0

        #文字送り長押し処理
        if key[pygame.K_SPACE] == 1 and message_box.text_length == message_box.text_note:
            if wait_timer == 50:
                message_box.next_text(screen)
                wait_timer = 0
            else:
                wait_timer = wait_timer + 1

        #文字送りのスピード
        speed = 3
        if key[pygame.K_LSHIFT] == 1 or key[pygame.K_RSHIFT] == 1:
            message_box.next_text(screen)
            speed = 1

        #強制的にスタートに戻る
        if key[pygame.K_RETURN] == 1:
            index = 0

        #文字表示
        if timer%speed == 0:
            message_box.appear_text(screen, font)

        #debug
        pygame.draw.rect(screen, BLACK,[0,0,960,560])
        if key[pygame.K_F1] == 1:
            draw_text_simple(screen, "timer            : "+ str(timer), 0, 0, debug_font,255,255,255)
            draw_text_simple(screen, "index            : "+ str(index), 0, 20, debug_font,255,255,255)
            draw_text_simple(screen, "message_index    : "+ str(message_box.message_index), 0, 40, debug_font,255,255,255)
            draw_text_simple(screen, "message_num      : "+ str(message_box.message_num), 0, 60, debug_font,255,255,255)
            draw_text_simple(screen, "text_length      : "+ str(message_box.text_length), 0, 80, debug_font,255,255,255)
            draw_text_simple(screen, "text_note        : "+ str(message_box.text_note), 0, 100, debug_font,255,255,255)
            draw_text_simple(screen, "space_key        : "+ str(key[pygame.K_SPACE]), 0, 120, debug_font,255,255,255)
            draw_text_simple(screen, "wait_timer       : "+ str(wait_timer), 0, 140, debug_font,255,255,255)
            draw_text_simple(screen, "unicode_length   : "+ str(message_box.unicode_length), 0, 160, debug_font,255,255,255)

        if key[pygame.K_F2] == 1:
            message_box.appear_log(screen, font)

        pygame.display.update()
        clock.tick(100)

if __name__ == "__main__":
    main()
