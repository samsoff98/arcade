from app import *



if __name__ == '__main__':
    Mainclass(width=GAME_WIDTH,height=GAME_HEIGHT,fps=60.0).run()

    """
    def changecolor(self,input):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        if input.is_key_down('spacebar'):
            current = True
        else:
            current = False
        change = current>0 and self._press == 0
        if change:
            for a in self._snake:
                a.fillcolor = introcs.RGB(r,g,b)

        self._press = current
    """
