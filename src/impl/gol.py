from __future__ import annotations

from typing import Union, List, Iterable

from src.components.simulation import Simulation
from src.components.unit import Unit, SurvivalCheckStrategy, Action
from src.display.stdout import StdOutDisplayStrategy


def _get_neighbors(unit: Union[Position, Unit], sim: Simulation) -> List[Unit]:
	p = unit.pos if isinstance(unit, Unit) else unit
	# TODO refactor with warlus operator (3.9+)
	positions = [(row, col) for col in range(p[1] -1, p[1] + 2) \
		for row in range(p[0] - 1, p[0] + 2) if (row, col) != p]
	return [sim.units[pos] for pos in positions \
			if pos in sim.units.keys()]


def check_for_new_cells(sim: Simulation) -> Iterable[Unit]:
	all_cells = {(row, col) for col in range(sim.width) \
		for row in range(sim.height)}
	dead_cells = all_cells.difference(set(sim.units.keys()))
	is_future_cell = lambda cell: len(_get_neighbors(cell, sim)) == 3 

	return filter(is_future_cell, dead_cells)


class GOLSurvivalCheckStrategy(SurvivalCheckStrategy):
	def check(self, unit: Unit, sim: Simulation) -> bool:
		return 1 < len(_get_neighbors(unit, sim)) < 4


class CheckForNewCells(Action):
	def execute(self, sim: Simulation):
		new_cells = check_for_new_cells(sim)
		return {pos: Unit(pos, 1, 0, GOLSurvivalCheckStrategy()) for pos in new_cells}
		

def main():
	blinker_game = Simulation(6, 6, 5, StdOutDisplayStrategy, [
			Unit((1, 1), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 1), 1, 0, GOLSurvivalCheckStrategy()),
			Unit((0, 1), 1, 0, GOLSurvivalCheckStrategy())], 
		CheckForNewCells(), None)
	block_game = Simulation(6, 6, 5, StdOutDisplayStrategy(), [
			Unit((1, 1), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((1, 2), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 1), 1, 0, GOLSurvivalCheckStrategy()),
			Unit((2, 2), 1, 0, GOLSurvivalCheckStrategy())], 
		CheckForNewCells(), None)
	toad_game = Simulation(6, 6, 5, StdOutDisplayStrategy(), [
			Unit((1, 0), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((1, 1), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((1, 2), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 1), 1, 0, GOLSurvivalCheckStrategy()),
			Unit((2, 3), 1, 0, GOLSurvivalCheckStrategy()), 
			Unit((2, 2), 1, 0, GOLSurvivalCheckStrategy())], 
		CheckForNewCells(), None)

	sim = toad_game
	printer = StdOutDisplayStrategy()

	printer.display(sim)
	sim.units = sim.generate_next_epoch_game()
	printer.display(sim)
	sim.units = sim.generate_next_epoch_game()
	printer.display(sim)
	sim.units = sim.generate_next_epoch_game()
	printer.display(sim)