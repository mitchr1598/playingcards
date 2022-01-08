# playingcards&#46;py


An Advanced and Customisable Python Playing Card Module that makes creating playing card games and running simulations general, simple and easy!

## Features
* Easy to use python interface
* Easy to Understand, general, Class Objects
* Card Comparisons

## Installation
>*Requires Python 3.9 and above*


You can install the module from [PyPI](https://pypi.org/project/playingcards1598/) or by using pip.

```sh
# Linux/MacOS
pip3 install playingcards1598

# Windows
pip install playingcards1598

```

## How To Use

### Quick Start
To quickly get started you can initiate a deck
```py
from playingcards import Deck

deck = Deck()
```

Shuffle the deck using `shuffle()`

```py
deck.shuffle()
```

Draw cards from this deck by using `draw_top_n()`

```py
drawn_cards = deck.draw_top_n(5)  # Draws 5 cards

print(len(deck))  # Prints 47
print(len(drawn_cards))  # Prints 5
```

Return the deck to original form using `reset()`

```py
deck.reset()
print(len(deck))  # Prints 52
```

### Customization
#### Custom Cards
This module presents three class objects for creating custom cards: `Rank` and `Suit` for the building blocks, and `Card` for the construction.

You can construct custom classes as follows

```python
rank = Rank('J', num_value=11)  # Creates a Jack rank
suit = Suit('s', pretty='♠')  # Creates a spade suit

card = Card(rank, suit)  # Creates the Jack of Hearts
```

A full deck of custom cards can be created by passing it during the `Deck` initiation.

```python
custom_deck = Deck([card])  # A custom deck consisting of only the card the specified above
```

Alternatively, a custom deck can be instantiated using the `from_ranks_suits()` class method

```python
big_red_deck = Deck.from_ranks_suits(
  [Rank(value, num) for rank, num in [('A', 14), ('K', 13), ('Q', 12), ('J', 11), ('T', 10)]],
  [Suit(suit, pretty) for suit, pretty in [('h', '♥'), ('d', '♦')]]
)
```

#### Card Collections
`Deck` is a subclass of `CardCollection`

Other `CardCollection`'s are possible. For example, to create a Texas Holdem Poker hand (two cards), you could do the following

```python
class TexasHand(CardCollection):
    def __init__(self, cards: list[Card]):
        super().__init__(cards, maximum = 2)
```



### Class Arguments

* **Rank** Arguments
  * value `str` - A string representation of the value of the rank
  * num_value `int` (optional) - A numerical value of the card, used in games that consist of ordering

* **Suit** Arguments
  * value `str` -  The desired value of the suit - s, h, c, d for a standard deck
  * pretty `str` (optional) - A prettier representation of the suit - ♠, ♥, ♣, ♦ for a standard deck

* **Card** Arguments
  * rank `Rank` -  The rank of the card
  * suit `Suit` - The suit of the card

* **Deck** and **CardCollection** Arguments
  * cards `list` -  A list of the cards in the collection
  * maximum `int` (optional) -  The maximum number of cards in the collection
```