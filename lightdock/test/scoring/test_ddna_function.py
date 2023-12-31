"""Tests for DDNA scoring function module"""

import pytest
from pathlib import Path
from lightdock.scoring.ddna.driver import DDNA, DDNAAdapter
from lightdock.pdbutil.PDBIO import parse_complex_from_file
from lightdock.structure.complex import Complex


class TestDDNA:
    def setup_class(self):
        self.path = Path(__file__).absolute().parent
        self.golden_data_path = self.path / "golden_data"
        self.dna = DDNA()

    def test_calculate_DNA_1AZP(self):
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1azp_prot.pdb"
        )
        receptor = Complex(
            chains, atoms, structure_file_name=(self.golden_data_path / "1azp_prot.pdb")
        )
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1azp_dna.pdb"
        )
        ligand = Complex(
            chains, atoms, structure_file_name=(self.golden_data_path / "1azp_dna.pdb")
        )
        adapter = DDNAAdapter(receptor, ligand)
        assert 6.915295143021656 == pytest.approx(
            self.dna(
                adapter.receptor_model,
                adapter.receptor_model.coordinates[0],
                adapter.ligand_model,
                adapter.ligand_model.coordinates[0],
            )
        )
