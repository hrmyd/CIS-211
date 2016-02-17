from tkinter import *
from random import randint
from CardLabel import *
from Card import *

flipper_app = Tk()

CardLabel.load_images()
box = Frame(flipper_app)
box.pack()

card1 = CardLabel(box)
card1.grid(row = 0, column = 1)

card2 = CardLabel(box)
card2.grid(row = 0, column = 2)

card3 = CardLabel(box)
card3.grid(row = 0, column = 3)

move = 0

def flip():
    global move
    
    side = ['front', 'front', 'front', 'blank', 'blank', 'blank', 'back', 'back', 'back']
    label = [card1, card2, card3] * 3
    
    if move < 9:
        label[move].display(side[move], randint(0,51))
        flipper_app.update()
        move += 1
    else:
        move = 0
    
flip_button = Button(flipper_app, text = 'Flip', command = flip)
flip_button.pack()
flipper_app.mainloop()