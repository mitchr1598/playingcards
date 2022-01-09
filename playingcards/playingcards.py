from dataclasses import dataclass, field
import random

STANDARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
STANDARD_SUITS = ['s', 'h', 'c', 'd']
STANDARD_SUITS_PRETTY = ['♠', '♥', '♣', '♦']


@dataclass(order=True)
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


@dataclass
class CardCollection:
    """
    A class for a collection of cards. Can be used for things like decks, hands, boards, etc
    """
    cards: list[Card]
    maximum: int = None

    def __post_init__(self):
        self._check_max_cards()

    def add_cards(self, cards: list[Card], position=0, randomly=False):
        if not randomly:
            for card in cards:
                self.cards.insert(position, card)
                position += 1
        else:
            for card in cards:
                self.cards.insert(random.randint(0, len(self.cards)), card)

    def _check_max_cards(self):
        if self.maximum is not None and len(self.cards) > self.maximum:
            raise ValueError

    def __str__(self):
        return ' | '.join([str(card) for card in self.cards])

    def __len__(self):
        return len(self.cards)


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
    r = Rank('K', 13)
    s = Suit('h', '♥')
    c = Card(r, s)
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
