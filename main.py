from __future__ import annotations

import abc

from typing import Iterable, NoReturn, Optional, List, Tuple, NewType, Union


# Exceptions
class LengthMustBePositiveException(Exception):
	pass


class SurvivalCheckStrategy(abc.ABC):

	@abc.abstractmethod
	def check(self, unit: Unit, game: Game) -> bool:
		pass

class Unit:
	def __init__(self, pos: Position,
		hp: int,
		mvt: int,
		survival_check:SurvivalCheckStrategy):

		self.pos = pos
		self.hp = hp
		self.mvt = mvt
		self.survival_check = survival_check

class Action():
	def execute(self, game: Game):
		# Must be implemented by sub classes
		# return game.units
		return  dict()
# 
class DisplayStrategy(abc.ABC):
	@abc.abstractmethod
	def display(self, game: Game) -> NoReturn:
		pass

class StdOutDisplayStrategy(DisplayStrategy):
	def display(self, game: Game) -> NoReturn:
		pass


class Game:
	def __init__(self, width: int,
		height: int,
		epochs: int,
		units: Optional[List[Unit]]=None,
		display_strategy: Optional[DisplayStrategy]=None,
		pre_epoch_action: Optional[Action]=None,
		post_epoch_action: Optional[Action]=None):

		self.width = width
		self.height = height
		self.epochs = epochs
		self.units = units or dict()
		self.display_strategy = display_strategy or StdOutDisplayStrategy()
		self.pre_epoch_action = pre_epoch_action or Action()
		self.post_epoch_aciton = post_epoch_action or Action()

		if isinstance(self.units, list):
			self.units = {unit.pos: unit for unit in self.units}

		self._assert_parameters_are_valid()

	def display(self) -> NoReturn:
		self.display_strategy.display(self)

	def _assert_parameters_are_valid(self):
		if self.width < 0 or self.height < 0 :
			raise LengthMustBePositiveException('Attributs `width` and `height` \
 must be positive')

	def execute_current_epoch(self, game: Game) -> Game:
		# for unit in self.units.values():
		# 	unit.survival_check.check(self)
		func = lambda x: x.survival_check.check(x, game)
		print('game.units', game.units.keys())

		print('nouv', [unit.pos for unit in game.units.values()])
		future_units = {unit.pos: unit for unit in \
			filter(func, game.units.values())}

		# next_game_state = game
		# next_game_state.units = future_units

		# return next_game_state
		return future_units

	def generate_next_epoch_game(self) -> Game:
		next_epoch = self.pre_epoch_action.execute(self)
		
		print('COUNT1', len(next_epoch), next_epoch.keys())
		print('?', next_epoch)
		# next_epoch2 = self.execute_current_epoch(self)
		# print('COUNT2', len(next_epoch2.units))
		# next_epoch.units.update(next_epoch2.units)
		# print('COUNT', len(next_epoch.units))
		# next_epoch.update()
		next_ = self.execute_current_epoch(self)
		print('COUNT2', len(next_), next_.keys())
		v = self.post_epoch_aciton.execute(self)

		print('COUNT3', len(v), v.keys())
		# next_epoch.update(v)

		next_.update(next_epoch)
		next_.update(v)
		print('COUNT4', len(next_), next_.keys())

		return next_
		# return next_epoch

# Types 
Position = NewType('Position', Tuple[int, int])


# Utils
def get_distance(p1: Position, p2: Position) -> int:
	return abs(p1 ** 2 + p2 ** 2)

def get_distance(u1: Unit, u2: Unit) -> int:
	return get_distance(u1.pos, u2.pos)


""" --- FIRST IMPLEMENTATION --- """

class GOLSurvivalCheckStrategy(SurvivalCheckStrategy):
	def check(self, unit: Unit, game: Game) -> bool:
		length = len(get_neighbors(unit, game))
		print(length)

		return 1 < length < 4
	

def check_for_new_cells(game: Game) -> Iterable[Unit]:
	all_cells = {(row, col) for col in range(game.width) \
		for row in range(game.height)}

	print('all_cell', all_cells)
	dead_cells = all_cells.difference(set(game.units.keys()))
	# print('dead_cells', dead_cells)
	# dead_cells = [game.units[pos] for pos in dead_cells if pos in game.units.keys()]
	# print('2dead_cells', dead_cells)
	# is_future_cell = lambda cell: survival_check.check(get_neighbors(cell, game))
	is_future_cell = lambda cell: len(get_neighbors(cell, game)) == 3 

	return filter(is_future_cell, dead_cells)



def get_neighbors(unit: Union[Position, Unit], game: Game) -> List[Unit]:
	# p = unit.pos
	p = unit.pos if isinstance(unit, Unit) else unit
	# Refactor with walrus operator in 3.9
	positions = [(row, col) for col in range(p[1] -1, p[1] + 2) for row in range(p[0] - 1, p[0] + 2) if (row, col) != p]
	# positions = [(p[0] + 1, p[1]), (p[0], p[1] + 1), 
	# 	(p[0] -1, p[1]), (p[0], p[1] -1)]

	print(positions, p)
	return [game.units[pos] for pos in positions \
			if pos in game.units.keys()]

# def get_neighbors(unit: Unit, game: Game) -> List[Unit]:
# 	return get_neighbors(unit.pos, game)
def create_str(game: Game) -> str:
	# return ''.join(['x' if (row, col) in game.units.keys() else ' ' for row in game.height for col in game.width])
	cells_as_str = [['x' if (row, col) in game.units.keys() else ' ' for col in range(game.width)] for row in range(game.height)]
	delimiter = f"+{'--' * game.width}+\n"

	return "{}|{} |\n{}".format(
		delimiter,
		' |\n|'.join(map(lambda x: ' '.join(x), cells_as_str)),
		delimiter)

class CheckForNewCells(Action):
	def execute(self, game: Game):
		new_cells = check_for_new_cells(game)
		# TODO Improve
		u = list(game.units.values())

		if len(u) == 0:
			return game


		y = dict()
		for cell in new_cells:

			y[cell] = Unit(cell, 1, 0, GOLSurvivalCheckStrategy())

		print('Y1', y.keys())
		print('Y2', [u.pos for u in y.values()])

		# new_cells = list(new_cells)
		print('new cells', y)
		# game.units.update(y)
		
		return y
if __name__ == '__main__':
	


	blinker_game = Game(6, 6, 5, [
			Unit((1, 1), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 1), 1, 0, GOLSurvivalCheckStrategy()),
			Unit((0, 1), 1, 0, GOLSurvivalCheckStrategy())], 
		None, CheckForNewCells(), None)
	block_game = Game(6, 6, 5, [
			Unit((1, 1), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((1, 2), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 1), 1, 0, GOLSurvivalCheckStrategy()),
			Unit((2, 2), 1, 0, GOLSurvivalCheckStrategy())], 
		None, CheckForNewCells(), None)
	toad_game = Game(6, 6, 5, [
			Unit((1, 0), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((1, 1), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((1, 2), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 1), 1, 0, GOLSurvivalCheckStrategy()),
			Unit((2, 3), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 2), 1, 0, GOLSurvivalCheckStrategy())], 
		None, CheckForNewCells(), None)

	print('TEST', [unit.pos for unit in toad_game.units.values()])

	game = blinker_game

	print(create_str(game))
	o = game.generate_next_epoch_game()
	game.units = o
	print(create_str(game))
	o = game.generate_next_epoch_game()
	game.units = o
	print(create_str(game))
	o = game.generate_next_epoch_game()
	game.units = o
	print(create_str(game))