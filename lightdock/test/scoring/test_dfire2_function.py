"""Tests for DFIRE2 scoring function module"""

import pytest
from pathlib import Path
from lightdock.scoring.dfire2.driver import DFIRE2, DFIRE2Adapter
from lightdock.pdbutil.PDBIO import parse_complex_from_file
from lightdock.structure.complex import Complex


class TestDFIRE2:
    def setup_class(self):
        self.path = Path(__file__).absolute().parent
        self.golden_data_path = self.path / "golden_data"
        # FIXME: Segmentation fault when adapter is loaded here

    def test_calculate_DFIRE2_1PPE(self):
        dfire2 = DFIRE2()
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1PPErec.pdb"
        )
        receptor = Complex(chains, atoms)
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1PPElig.pdb"
        )
        ligand = Complex(chains, atoms)
        adapter = DFIRE2Adapter(receptor, ligand)
        assert -398.7303561600074 == pytest.approx(
            dfire2(
                adapter.receptor_model,
                adapter.receptor_model.coordinates[0],
                adapter.ligand_model,
                adapter.ligand_model.coordinates[0],
            )
        )

    def test_calculate_DFIRE2_1EAW(self):
        dfire2 = DFIRE2()
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1EAWrec.pdb"
        )
        receptor = Complex(chains, atoms)
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1EAWlig.pdb"
        )
        ligand = Complex(chains, atoms)
        adapter = DFIRE2Adapter(receptor, ligand)
        assert -488.34640492000244 == pytest.approx(
            dfire2(
                adapter.receptor_model,
                adapter.receptor_model.coordinates[0],
                adapter.ligand_model,
                adapter.ligand_model.coordinates[0],
            )
        )

    def test_calculate_DFIRE2_1AY7(self):
        dfire2 = DFIRE2()
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1AY7rec.pdb"
        )
        receptor = Complex(chains, atoms)
        atoms, _, chains = parse_complex_from_file(
            self.golden_data_path / "1AY7lig.pdb"
        )
        ligand = Complex(chains, atoms)
        adapter = DFIRE2Adapter(receptor, ligand)
        assert -283.19129030999665 == pytest.approx(
            dfire2(
                adapter.receptor_model,
                adapter.receptor_model.coordinates[0],
                adapter.ligand_model,
                adapter.ligand_model.coordinates[0],
            )
        )
