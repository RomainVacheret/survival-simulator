from typing import NoReturn

from src.components.simulation import Simulation
from src.display.strategy import DisplayStrategy


class StdOutDisplayStrategy(DisplayStrategy):
	def display(self, sim: Simulation) -> NoReturn:
		generator = StringGenerator()
		print(generator.generate(sim))


class StringGenerator:
	# TODO Generalize character using the unit's type

	def _generate_delimiter(self, length) -> str:
		return f"+{'--' * length}+\n"

	def generate(self, sim: Simulation) -> str:
		cells_as_str = [['x' if (row, col) in sim.units.keys() else ' ' \
			 for col in range(sim.width)] for row in range(sim.height)]

		return "{}|{} |\n{}".format(
			self._generate_delimiter(sim.width),
			' |\n|'.join(map(lambda x: ' '.join(x), cells_as_str)),
			self._generate_delimiter(sim.width))