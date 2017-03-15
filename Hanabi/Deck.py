#!/usr/bin/python

from Card import Card
from constants import _COLORS, _NUMBERS
from random import shuffle


class Deck(object):
  def __init__(self,
               difficulty,
               frequencies=[3, 2, 2, 2, 1],
               excluded_colors=["Unknown"]
               ):
    self.cards = []
    self.difficulty = difficulty
    self.frequencies = frequencies
    self.excluded_colors = excluded_colors

    self.set_difficulty()
    self._build()


  def set_difficulty(self, difficulty=None):
    if not difficulty:
      difficulty = self.difficulty
    if difficulty == "Difficult":
      self.frequencies = [1, 1, 1, 1, 1]
    else:
      if "Rainbow" not in self.excluded_colors:
        self.excluded_colors.append("Rainbow")

  def _build(self):
    for color in _COLORS.keys():
        if color not in self.excluded_colors:
            for number in _NUMBERS:
                for x in range(self.frequencies[int(number) - 1]):
                    self.cards.append(Card(color, number))
    shuffle(self.cards)
    self.cards_remaining = len(self.cards)

  def get_card(self):
    self.cards_remaining -= 1
    return self.cards.pop()

if __name__ == "__main__":

  test = Deck("Normal")

  for card in test.cards:
      print(card)
  print(test.cards_remaining)

  print('')
  print(test.cards[-1])
  card = test.get_card()
  print(card)
  print(test.cards_remaining)
