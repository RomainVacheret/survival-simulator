from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NoReturn


class DisplayStrategy(ABC):
	@abstractmethod
	def display(self, sim: Simulation) -> NoReturn:
		pass