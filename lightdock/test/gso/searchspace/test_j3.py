"""Tests for J3 function"""

import pytest
from lightdock.gso.searchspace.benchmark_ofunctions import J3
from lightdock.gso.coordinates import Coordinates


class TestJ3:
    def setup_class(self):
        self.expected_values = [
            [
                3.80536808724531,
                4.563758239636366,
                4.489780170100593,
                4.563758239636366,
                3.80536808724531,
            ],
            [
                4.563758239636366,
                5.285985504563145,
                2.27281915378979,
                5.285985504563145,
                4.563758239636366,
            ],
            [
                4.489780170100593,
                2.27281915378979,
                0,
                2.27281915378979,
                4.489780170100593,
            ],
            [
                4.563758239636366,
                5.285985504563145,
                2.27281915378979,
                5.285985504563145,
                4.563758239636366,
            ],
            [
                3.80536808724531,
                4.563758239636366,
                4.489780170100593,
                4.563758239636366,
                3.80536808724531,
            ],
        ]

    def test_compute_J1_matrix(self):
        j3 = J3()
        for i in range(5):
            for j in range(5):
                assert self.expected_values[i][j] == pytest.approx(j3(Coordinates([-10.0 + j * 5.0, -10.0 + i * 5.0])))
