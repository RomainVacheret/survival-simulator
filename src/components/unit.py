from __future__ import annotations 

from abc import ABC, abstractmethod
from typing import Dict, NewType, Tuple


Position = NewType('Position', Tuple[int, int])


class Unit:
	def __init__(self, pos: Position,
		hp: int,
		mvt: int,
		survival_check:SurvivalCheckStrategy):

		self.pos = pos
		self.hp = hp
		self.mvt = mvt
		self.survival_check = survival_check


class SurvivalCheckStrategy(ABC):
	@abstractmethod
	def check(self, unit: Unit, sim: Simulation) -> bool:
		pass


class Action():
	def execute(self, sim: Simulation) -> Dict[Position, Unit]:
		# Must be overriten by sub classes
		return  dict()