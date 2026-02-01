import curses
import time
import random
import keyboard

width_pad = 8
superspd = 2


def main(stdscr):
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.clear()
    start = False

    sh, sw = stdscr.getmaxyx()

    pad_x, pad_y = sw //2 - width_pad //2, sh - 2

    ball_y, ball_x = pad_y - 1, pad_x + width_pad //2
    ball_dy, ball_dx = -1, random.choice([-1,1])

    rows = 5
    cols = sw//4
    bricks = []
    for row in range(rows):
        for col in range(cols):
            bricks.append((row+1, col*4))
    #print(bricks)

    while True:
        time.sleep(1/20)
        if keyboard.is_pressed("b"):
            break
        elif keyboard.is_pressed("q"):
            if keyboard.is_pressed("shift"):
                pad_x -= 2*superspd
            else: 
                pad_x -=2
            pad_x = max(1, min(pad_x, sw - width_pad))
        elif keyboard.is_pressed("d"):
            if keyboard.is_pressed("shift"):
                pad_x += 2*superspd
            else: 
                pad_x +=2
            pad_x = max(1, min(pad_x, sw - width_pad))
        if keyboard._pressed_events:
            start = True

        

        stdscr.clear()
        
        for by, bx in bricks:
            stdscr.addstr(by, bx, "###")

        for i in range(width_pad):
            stdscr.addch(pad_y, pad_x + i, "_")
        
        if start:
                
            ball_x += ball_dx
            ball_y += ball_dy

            if ball_x <= 0 or ball_x >= sw-1:
                ball_dx *= -1
            if ball_y <=0:
                 ball_dy *= -1
            if ball_y == pad_y and pad_x <= ball_x <= pad_x + width_pad:
                 ball_dy *= -1
            if ball_y > sh - 1:
                start = False
                ball_y, ball_x = pad_y - 1, pad_x + width_pad // 2
                ball_dy, ball_dx = -1, random.choice([-1, 1])
            for brick in bricks:
                by, bx = brick
                if ball_y == by and bx <= ball_x < bx + 4:
                    ball_dy *= -1

            stdscr.addch(ball_y, ball_x, "o")


        stdscr.refresh()

curses.wrapper(main)