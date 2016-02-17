from tkinter import *
from tkinter.messagebox import *
from CardLabel import *
from Card import *
from Deck import *

class BlackjackFrame(Frame):
    """
    Subclass of Frame, creates a blackjack game.
    """
    
    _player_hand = []
    _dealer_hand = []
    
    _player_move = 0
    _dealer_move = 0
    
    _player_wins = 0
    _dealer_wins = 0
    
    def __init__(self, parent):
        """
        Buttons and card labels initialized.
        """
        
        Frame.__init__(self, parent)
        self.configure(background = 'white')
        
        self._cards = Deck(BlackjackCard)
        self._cards.shuffle()
        self.pack()
        
        CardLabel.load_images()
        
        self._dc1 = CardLabel(self)
        self._dc1.grid(row = 0, column = 0)
        self._dc2 = CardLabel(self)
        self._dc2.grid(row = 0, column = 1)
        self._dc3 = CardLabel(self)
        self._dc3.grid(row = 0, column = 2)
        self._dc4 = CardLabel(self)
        self._dc4.grid(row = 0, column = 3)
        self._dc5 = CardLabel(self)
        self._dc5.grid(row = 0, column = 4)
        self._dc6 = CardLabel(self)
        self._dc6.grid(row = 0, column = 5)
        
        self._pc1 = CardLabel(self)
        self._pc1.grid(row = 1, column = 0)
        self._pc2 = CardLabel(self)
        self._pc2.grid(row = 1, column = 1)
        self._pc3 = CardLabel(self)
        self._pc3.grid(row = 1, column = 2)
        self._pc4 = CardLabel(self)
        self._pc4.grid(row = 1, column = 3)
        self._pc5 = CardLabel(self)
        self._pc5.grid(row = 1, column = 4)
        self._pc6 = CardLabel(self)
        self._pc6.grid(row = 1, column = 5)
        
        self._deal = Button(self, text = 'Deal', command = self.dealcb)
        self._deal.grid(row = 2, column = 0, padx = 10, pady = 10)
        self._hit = Button(self, text = 'Hit', command = self.hitcb)
        self._hit.grid(row = 2, column = 2, padx = 10, pady = 10)
        self._stand = Button(self, text = 'Stand', command = self.standcb)
        self._stand.grid(row = 2, column = 4, padx = 10, pady = 10)

        self.dealcb()
        
    def dealcb(self):
        """
        Resets player and dealer hands with 2 cards each from top of deck and sets up starting layout for each hand.
        """
        self._hit.configure(state = ACTIVE)
        self._stand.configure(state = ACTIVE)
        old = self._dealer_hand + self._player_hand
        self._cards.restore(old)

        self._player_hand = self._cards.deal(2)
        self._dealer_hand = self._cards.deal(2)
        self._player_move = 0
        self._dealer_move = 0
        
        self._dc1.display('back')
        self._dc2.display('front', self._dealer_hand[1]._id)
        self._dc3.display('blank')
        self._dc4.display('blank')
        self._dc5.display('blank')
        self._dc6.display('blank')
        
        self._pc1.display('front', self._player_hand[0]._id)
        self._pc2.display('front', self._player_hand[1]._id)
        self._pc3.display('blank')
        self._pc4.display('blank')
        self._pc5.display('blank')
        self._pc6.display('blank')
        
        Label(self, text = 'Dealer Wins: ').grid(row = 3, column = 2, padx = 10, pady = 10)
        self.dcount = Label(self, text = self._dealer_wins)
        self.dcount.update_idletasks()
        self.dcount.grid(row = 3, column = 3, padx = 10, pady = 10)
        Label(self, text = 'Player Wins: ').grid(row = 4, column = 2, padx = 10, pady = 10)
        self.pcounts = Label(self, text = self._player_wins)
        self.pcounts.grid(row = 4, column = 3, padx = 10, pady = 10)
        self.pcounts.update_idletasks()
    
    def hitcb(self):
        """
        Appends card from top of deck to players hand, changes display of cards in players hand from blank to the new card. 
        """
    
        label = [self._pc3, self._pc4, self._pc5, self._pc6]
    
        if self._player_move < 4 and self.total(self._player_hand) <= 21:
            card = self._cards.deal(1)
            self._player_hand.extend(card)
            label[self._player_move].display('front', self._player_hand[self._player_move + 2]._id)
            self._player_move += 1
            
            if self.total(self._player_hand) > 21:
                self._hit.configure(state = DISABLED)
                showinfo(title = 'Game Over', message = 'You Lose, Total Over 21')
                self._player_move = 0
                self._dealer_wins += 1
    
    def standcb(self):
        """
        'flips' over dealers first card to front, compares total points of player and dealer to determine winner.
        """
        
        label = [self._dc3, self._dc4, self._dc5, self._dc6]
        
        while self.total(self._dealer_hand) < 17:
            card = self._cards.deal(1)
            self._dealer_hand.extend(card)
            label[self._dealer_move].display('front', self._dealer_hand[self._dealer_move + 2]._id)
            self._dealer_move += 1
            
        self._hit.configure(state = DISABLED)
        self._stand.configure(state = DISABLED)
        self._dc1.display('front', self._dealer_hand[0]._id)
        
        dealer_total, player_total = self.total(self._dealer_hand), self.total(self._player_hand)
        
        if dealer_total <= 21 and player_total <= 21:
            if dealer_total > player_total:
                showinfo(title = 'Game Over', message = 'You Lose, Dealer Wins')
                self._dealer_wins += 1
            elif player_total > dealer_total:
                showinfo(title = 'Game Over', message = 'You Win!')
                self._player_wins += 1
            elif dealer_total > 21:
                showinfo(title = 'Game Over', message = 'You Win!')
                self._player_wins += 1
            else:
                showinfo(title = 'Game Over', message = "It's a tie")
        else:
            showinfo(title = 'Game Over', message = "It's a tie")
        
        
    def total(self, hand):
        """
        Calculates the total for a given hand.
        """
        points = 0
        n_aces = 0
        
        for card in hand:
            points += card.points()
            if card.rank() == 12:
                n_aces += 1
        
        while points > 21 and n_aces > 0:
            points -= 10
            n_aces -= 1
            
        return points