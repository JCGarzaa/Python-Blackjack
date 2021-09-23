### BLACKJACK ###
## One player vs CPU dealer ##
## Player can hit or stand ##
## Player can choose bet amount ##
## Keep track of total player money (do not allow bets over total money) ##
## Alert player of win, loss, bust ##

# Create deck of 52 cards with suits and colors #
# Shuffle deck #
# Deal 2 cards, face up to player and 2 cards,1 hidden to CPU #
# when player stands, dealer plays: cannot hit past 17, and plays until bust or beats player
# Ace can be 1 or 11, assume 11, but if adding 11 exceeds 21, subtract 10 from it
# Optional: include double down or split

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  #
        self.value = 0  # start w/ 0 value
        self.aces = 0  # keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces != 0:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))

        except ValueError:
            print('Please input an integer! ')
        else:
            if chips.bet > chips.total:
                print(f'Insufficient funds. Your bet cannot exceed {chips.total}')
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input("Would you like to HIT or STAND? Enter 'h' or 's' ").lower()

        if x == 'h':
            hit(deck, hand)
        elif x == 's':
            print('Player stands. Dealer is playing.')
            playing = False
        else:
            print("Invalid input. Please try again")
            continue
        break

def double_down(chips):
    question = input("Would you like to double down? Enter 'y' or 'n': ").lower()

    if question == 'y':
        if chips.total > chips.bet * 2:
            chips.bet = chips.bet * 2
            print(f"You have doubled down. Your new bet is {chips.bet}.")
        else:
            print('Sorry, not enough chips to double down.')
    else:
        print('You have chosen not to double down.')

    playing = True

def split(deck, hand):
    if input("You have a pair. Would you like to split your hand? Enter 'y' or 'n': ") == 'y':
        new_hand = []
        new_hand.append(hand.cards.pop())
        new_hand.append(deck.deal())

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("\nPlayer's Hand =", player.value)

# end game scenarios

def player_busts(player,dealer,chips):
    chips.lose_bet()
    print('Sorry, you have busted.')

def player_wins(player,dealer,chips):
    chips.win_bet()
    print("You have won! You beat the dealer ")

def dealer_busts(player,dealer,chips):
    chips.win_bet()
    print('The dealer has busted. You win!')

def dealer_wins(player,dealer,chips):
    chips.lose_bet()
    print('The dealer wins. You lose.')

def push(player,dealer):
    print('Dealer and Player tie. It is a push')


## GAMEPLAY ##

## ADD SPLIT, DOUBLE DOWN,BLACKJACK OFF DEAL

while True:
    # opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until they reach 17 then stops. Aces count as 1 or 11.')

    # Create and shuffle deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up player chips
    player_chips = Chips()  # Default is 100

    # Prompt player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    # Ask to double down
    double_down(player_chips)

    while playing:  # recall this variable from hit_or_stand function
        # if player_hand.value / 2 == player_hand.value[0]:

        # Prompt player to hit or stand
        hit_or_stand(deck, player_hand)

        # show cards (but keep 1 dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, busts and break
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        # If hasn't busted, play dealer's hand until dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

            # Show all cards
        show_all(player_hand, dealer_hand)
        # Run win scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

        # Inform player chip total
    print(f"\nPlayer's winnings stand at {player_chips.total}")
    # Ask to play again
    new_game = input("Would you like to play again? Enter 'y' or 'n': ")

    if new_game[0].lower() == 'y':
        playing = True
    else:
        print('Thanks for playing!')
        break

