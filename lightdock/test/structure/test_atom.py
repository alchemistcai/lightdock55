"""Tests for Atom class"""

import pytest
from lightdock.structure.atom import Atom, HetAtom
from lightdock.error.lightdock_errors import AtomError


class TestAtom:
    def test_create_empty_atom(self):
        atom = Atom()
        assert 0.0 == pytest.approx(atom.x)

    def test_assign_element_and_mass(self):
        atom = Atom(
            1,
            "CA",
            "",
            "A",
            "ALA",
            1,
            "",
            x=0.0,
            y=0.0,
            z=0.0,
            occupancy=1.0,
            b_factor=0.0,
            element=None,
            mass=None,
        )
        assert atom.element == "C"
        assert Atom.MASSES[atom.element] == pytest.approx(atom.mass)

    def test_create_atom_not_given_element(self):
        atom = Atom(
            1,
            "PB",
            "",
            "A",
            "ALA",
            1,
            "",
            x=0.0,
            y=0.0,
            z=0.0,
            occupancy=1.0,
            b_factor=0.0,
            element=None,
            mass=None,
        )
        assert atom.element == "PB"
        assert Atom.MASSES[atom.element] == pytest.approx(atom.mass)

    def test_assign_element_and_mass_of_not_recognized_element(self):
        with pytest.raises(AtomError):
            atom = Atom(
                1,
                "Ty",
                "",
                "A",
                "BSG",
                1,
                "",
                x=0.0,
                y=0.0,
                z=0.0,
                occupancy=1.0,
                b_factor=0.0,
                element=None,
                mass=None,
            )
            assert atom.name != "Ty"

    def test_not_recognized_element(self):
        """Test if Tylium is recognized"""
        with pytest.raises(AtomError):
            atom = Atom(
                1,
                "Ty",
                "",
                "A",
                "BSG",
                1,
                "",
                x=0.0,
                y=0.0,
                z=0.0,
                occupancy=1.0,
                b_factor=0.0,
                element="Ty",
                mass=None,
            )
            assert atom.name != "Ty"

    def test_is_hydrogen(self):
        atom1 = Atom(
            1,
            "CA",
            "",
            "A",
            "ALA",
            1,
            "",
            x=1.0,
            y=2.0,
            z=-3.0,
            occupancy=1.0,
            b_factor=0.0,
            element=None,
            mass=None,
        )
        atom2 = Atom()

        assert not atom1.is_hydrogen() and atom2.is_hydrogen()

    def test_is_backbone(self):
        atom1 = Atom(
            1,
            "CA",
            "",
            "A",
            "ALA",
            1,
            "",
            x=1.0,
            y=2.0,
            z=-3.0,
            occupancy=1.0,
            b_factor=0.0,
            element=None,
            mass=None,
        )
        atom2 = Atom()

        assert atom1.is_backbone() and not atom2.is_backbone()

    def test_distance(self):
        atom1 = Atom(
            1,
            "CA",
            "",
            "A",
            "ALA",
            1,
            "",
            x=1.0,
            y=2.0,
            z=2.0,
            occupancy=1.0,
            b_factor=0.0,
            element=None,
            mass=None,
        )
        atom2 = Atom()

        assert 3.0 == pytest.approx(atom1.distance(atom2))
        assert 3.0 == pytest.approx(atom2.distance(atom1))

    def test_clone(self):
        atom1 = Atom()
        atom2 = atom1.clone()

        assert atom1 == atom2
        assert not atom1 != atom2

        atom1.name = "C"

        assert atom1 != atom2

    def test_to_string(self):
        atom1 = Atom(
            1,
            "CA",
            "",
            "A",
            "ALA",
            1,
            "",
            x=1.0,
            y=2.0,
            z=2.0,
            occupancy=1.0,
            b_factor=0.0,
            element=None,
            mass=None,
        )
        assert str(atom1) == "  CA   1.000   2.000   2.000"


class TestHetAtom:
    def test_create_atom(self):
        atom = HetAtom()
        assert atom.__class__.__name__ == "HetAtom"
