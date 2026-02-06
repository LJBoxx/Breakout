import curses
import time
import random
import keyboard

width_pad = 9
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
        time.sleep(1/15)
        if keyboard.is_pressed("b"):
            break
        elif keyboard.is_pressed("q") or keyboard.is_pressed("a"):
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
        if keyboard.is_pressed("space") and not start:
            ball_x = pad_x + int(width_pad /2)
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
                if ball_x < (pad_x + width_pad/2) and ball_dx == 1:
                    ball_dx = -1
                if ball_x > (pad_x + width_pad/2) and ball_dx == -1:
                    ball_dx = 1

            if ball_y > sh - 1:
                start = False
                ball_y, ball_x = pad_y - 1, pad_x + width_pad // 2
                ball_dy, ball_dx = -1, random.choice([-1, 1])
            for brick in bricks:
                by, bx = brick
                if ball_y == by and bx-1<=ball_x<=bx+2:
                    bricks.remove((by,bx))
                if ball_y + ball_dy == by and bx -1 <= ball_x + ball_dx <= bx + 2:
                    bricks.remove((by,bx))
                    if bx <= ball_x <= bx + 2:
                        ball_dy *= -1
                    else:
                        ball_dx *= -1  # playable but need to fix something with ball going inside neighbor block when coliding in the corner ;-;

            stdscr.addch(ball_y, ball_x, "o")
            stdscr.addstr(0,0, str(ball_dx))
            stdscr.addstr(0,6, str(ball_x))
            stdscr.addstr(0,12, str(pad_x+width_pad))


        stdscr.refresh()

curses.wrapper(main)