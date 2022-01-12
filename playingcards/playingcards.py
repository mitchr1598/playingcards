from dataclasses import dataclass, field
import random
from playingcards.utils import concat_by_line

STANDARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
STANDARD_SUITS = ['s', 'h', 'c', 'd']
STANDARD_SUITS_PRETTY = ['♠', '♥', '♣', '♦']
_FRENCH_SUIT_MAPPER = dict(zip(STANDARD_SUITS, STANDARD_SUITS_PRETTY))


@dataclass(frozen=True, order=True)
class Rank:
    value: str
    num_value: int = None

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Suit:
    """
    A class for custom suits
    :param : value. The desired value of the suit - s, h, c, d for a standard deck
    :param : pretty. Optional. A prettier representation of the suit - ♠, ♥, ♣, ♦ for a standard deck
    """
    value: str
    pretty: str = None

    def __str__(self):
        return self.pretty if self.pretty is not None else self.value


@dataclass(frozen=True, order=True)
class Card:
    rank: Rank
    suit: Suit

    def __str__(self):
        return str(self.rank) + str(self.suit)

    @classmethod
    def from_string(cls, string, french_deck=True):
        """
        Produces a card object from a string.
        :param string: The string of a card, eg 'As'
        :param french_deck: bool, if true it'll automatically choose pretty suits
        :return: A card object
        """
        rank = string[0]
        suit = string[1]
        return Card(Rank(rank), Suit(suit, _FRENCH_SUIT_MAPPER[suit] if french_deck else None))

    def ascii(self) -> str:
        """
        Creates an ASCII image of the playing card object.
        """
        return f"*- - -*\n|{self.suit}    |\n|  {self.rank}  |\n|   {self.suit} |\n*- - -*"

    def __eq__(self, other):
        return self.rank.value == other.rank.value and self.suit.value == other.suit.value


@dataclass
class CardCollection:
    """
    A class for a collection of cards. Can be used for things like decks, hands, boards, etc
    """
    cards: list[Card]
    maximum: int = None
    ordered: bool = False
    reverse_order: bool = False

    def __post_init__(self):
        self._check_max_cards()
        self.order_cards()

    def order_cards(self):
        if self.ordered:
            self.cards.sort(reverse=self.reverse_order)

    def add_cards(self, cards: list[Card], position=0, randomly=False):
        if not randomly:
            for card in cards:
                self.cards.insert(position, card)
                position += 1
        else:
            for card in cards:
                self.cards.insert(random.randint(0, len(self.cards)), card)
        self.order_cards()

    def remove_cards(self, cards):  # Should add a by position option
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    def _check_max_cards(self):
        if self.maximum is not None and len(self.cards) > self.maximum:
            raise ValueError("To many cards in collection")

    def ascii(self):
        return concat_by_line([c.ascii() for c in self.cards], sep='  ')

    def __str__(self):
        return ' | '.join([str(card) for card in self.cards])

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __add__(self, other) -> list[Card]:
        if other is None:
            return self.cards
        elif isinstance(other, Card):
            return self.cards + [other]
        elif isinstance(other, CardCollection):
            return self.cards + other.cards
        else:
            raise TypeError(f"Cannot add {type(self)} to {type(other)}. CardCollections can only add to a Card or another CardCollection")

    @classmethod
    def from_string(cls, string, french_deck=True):
        """
        Produces a CardCollection object from a string.
        :param string: The string of a card collection, eg 'AsKd', or 'As Kd'
        :param french_deck: bool, if true it'll automatically choose pretty suits
        :return: A CardCollection object
        """
        string = string.replace(' ', '')
        card_strings = [string[i:i+2] for i in range(0, len(string), 2)]
        return cls([Card.from_string(c, french_deck=french_deck) for c in card_strings])


class Deck(CardCollection):
    def __init__(self, cards=None, maximum=None):
        if cards is None:  # Generate a standard French deck if cards aren't specified
            cards = [
                Card(Rank(r, num_rank), Suit(s, pretty_suit))
                for s, pretty_suit in zip(STANDARD_SUITS, STANDARD_SUITS_PRETTY)
                for num_rank, r in enumerate(STANDARD_RANKS, start=1)
            ]
        super().__init__(cards, maximum=maximum)
        self._oringinal_deck = tuple(self.cards)  # tuple to avoid being changed (Card, Rank, and Suit are all frozen)

    def shuffle(self) -> None:
        """Shuffles the deck"""
        random.shuffle(self.cards)

    def reset(self, shuffle=False) -> None:
        """Add's all original cards back into the deck and optionally shuffles it"""
        self.cards = list(self._oringinal_deck)
        if shuffle:
            self.shuffle()

    def draw_top_n(self, n, collection_type: type = CardCollection) -> CardCollection:
        """
        Draws n cards from the top of the deck and returns the drawn cards. The Deck object will now have
        :param n: The number of cards to draw.
        :param collection_type: The class that the drawn cards form. For example you could put a 'Hand' class in here
        :return: The drawn cards, either of type CardCollection, or of inputted type
        """
        if len(self.cards) <= n-1:
            raise MaxCardsDrawn(f"Asked to draw {n} cards but there is only {len(self.cards)} left in deck")
        drawn_cards = self.cards[:n]
        self.cards = self.cards[n:]
        return collection_type(drawn_cards)

    @classmethod
    def from_ranks_suits(cls, ranks: list[Rank], suits: list[Suit]):
        return Deck([Card(r, s) for s in suits for r in ranks])


class MaxCardsDrawn(Exception):
    pass


class TooManyCards(Exception):
    pass


def main():
    cc = CardCollection.from_string('AsKd')
    print(cc.ascii())
    d = Deck()
    d.remove_cards(cc)
    print(d)

    r = Rank('K', 13)
    s = Suit('h', '♥')
    c = Card(r, s)
    print(c.ascii())
    d = Deck()
    print(str(r))
    print(str(s))
    print(str(c))
    print(str(d))
    d.shuffle()
    print(str(d))
    drawn = d.draw_top_n(13)
    print(str(d))
    print(str(drawn))
    d.reset()
    print(str(d))


if __name__ == '__main__':
    main()
