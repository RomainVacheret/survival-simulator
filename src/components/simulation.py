from __future__ import annotations

from typing import Optional, NoReturn, List, Dict

from src.components.exceptions import LengthMustBePositiveException
from src.components.unit import Unit, Action, Position
from src.display.strategy import DisplayStrategy


class Simulation:
	def __init__(self, width: int,
		height: int,
		epochs: int,
		display_strategy: DisplayStrategy,
		units: Optional[List[Unit]]=None,
		pre_epoch_action: Optional[Action]=None,
		post_epoch_action: Optional[Action]=None):

		self.width = width
		self.height = height
		self.epochs = epochs
		self.display_strategy = display_strategy 
		self.units = units or dict()
		self.pre_epoch_action = pre_epoch_action or Action()
		self.post_epoch_aciton = post_epoch_action or Action()

		if isinstance(self.units, list):
			self.units = {unit.pos: unit for unit in self.units}

		self._assert_parameters_are_valid()

	def display(self) -> NoReturn:
		self.display_strategy.display(self)

	def _assert_parameters_are_valid(self) -> NoReturn:
		if self.width < 0 or self.height < 0 :
			raise LengthMustBePositiveException('Attributs `width` and `height` \
 must be positive')

	def execute_current_epoch(self, sim: Simulation) -> Dict[Position, Unit]: 
		func = lambda x: x.survival_check.check(x, sim)
		future_units = {unit.pos: unit for unit in \
			filter(func, sim.units.values())}

		return future_units

	def generate_next_epoch_game(self) -> Dict[Position, Unit]:
		pre_units = self.pre_epoch_action.execute(self)
		next_units = self.execute_current_epoch(self)
		post_units = self.post_epoch_aciton.execute(self)

		next_units.update(pre_units)
		next_units.update(post_units)

		return next_units