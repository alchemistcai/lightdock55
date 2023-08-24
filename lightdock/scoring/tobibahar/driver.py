"""
TOBI potentials scoring functions as described in:

Tobi, D. and Bahar, I. (2006), Optimal design of protein docking potentials: Efficiency and limitations.
Proteins, 62: 970-981. https://doi.org/10.1002/prot.20859
"""

from pathlib import Path
import scipy.spatial

from lightdock.error.lightdock_errors import PotentialsParsingError
from lightdock.structure.model import DockingModel
from lightdock.structure.space import SpacePoints
from lightdock.scoring.functions import ModelAdapter, ScoringFunction
from lightdock.constants import DEFAULT_CONTACT_RESTRAINTS_CUTOFF


class TOBIBAHARPotential(object):
    """Loads TOBI potentials information"""

    # NH and OC are SPECIAL, the rest should be centroids
    recognized_residues = [
        "ALA",
        "ARG",
        "ASN",
        "ASP",
        "CYS",
        "GLN",
        "GLU",
        "GLY",
        "HIS",
        "ILE",
        "LEU",
        "LYS",
        "MET",
        "PHE",
        "PRO",
        "SER",
        "THR",
        "TRP",
        "TYR",
        "VAL",
        "NH",
        "OC",
    ]

    # N, CA, C, O and GLYCA are special
    atom_types = [
        ["N"],
        ["CA"],
        ["C"],
        ["O"],
        ["GLYCA"],
        [
            "ALACB",
            "ARGCB",
            "ASNCB",
            "ASPCB",
            "CYSCB",
            "GLNCB",
            "GLUCB",
            "HISCB",
            "ILECB",
            "LEUCB",
            "LYSCB",
            "METCB",
            "PHECB",
            "PROCB",
            "PROCG",
            "PROCD",
            "THRCB",
            "TRPCB",
            "TYRCB",
            "VALCB",
        ],
        ["LYSCE", "LYSNZ"],
        ["LYSCD"],
        ["ASPCG", "ASPOD1", "ASPOD2", "GLUCD", "GLUOE1", "GLUOE2"],
        ["ARGCZ", "ARGNH1", "ARGNH2"],
        ["ASNCG", "ASNOD1", "ASNND2", "GLNCD", "GLNOE1", "GLNNE2"],
        ["ARGCD", "ARGNE"],
        ["SERCB", "SEROG", "THROG1", "TYROH"],
        ["HISCG", "HISND1", "HISCD2", "HISCE1", "HISNE2", "TRPNE1"],
        ["TYRCE1", "TYRCE2", "TYRCZ"],
        [
            "ARGCG",
            "GLNCG",
            "GLUCG",
            "ILECG1",
            "LEUCG",
            "LYSCG",
            "METCG",
            "METSD",
            "PHECG",
            "PHECD1",
            "PHECD2",
            "PHECE1",
            "PHECE2",
            "PHECZ",
            "THRCG2",
            "TRPCG",
            "TRPCD1",
            "TRPCD2",
            "TRPCE2",
            "TRPCE3",
            "TRPCZ2",
            "TRPCZ3",
            "TRPCH2",
            "TYRCG",
            "TYRCD1",
            "TYRCD2",
        ],
        ["ILECG2", "ILECD1", "ILECD", "LEUCD1", "LEUCD2", "METCE", "VALCG1", "VALCG2"],
        ["CYSSG"],
    ]

    def __init__(self):
        data_path = Path(__file__).parent.resolve() / "data"
        self.tobibahar = self._read_potentials(data_path / "TOBI_BAHAR.dat")

    def _read_potentials(self, data_file_name):
        """Reads TOBI data potentials"""
        data_file = open(data_file_name)
        data = data_file.readlines()
        data_file.close()
        potentials = [[None for i in range(22)] for j in range(22)]
        try:
            for x in range(22):
                for y in range(22):
                    potentials[x][y] = float(data[x + 1].strip().split()[y + 1])

        except Exception as e:
            raise PotentialsParsingError(
                f"Error parsing {data_file_name} file. Details: {e}"
            )

        return potentials


class TOBIBAHARAdapter(ModelAdapter):
    """Adapts a given Complex to a DockingModel object suitable for this
    TOBI-BAHAR scoring function.
    """

    def _get_docking_model(self, molecule, restraints):
        """Builds a suitable docking model for this scoring function"""
        residues = [residue for chain in molecule.chains for residue in chain.residues]
        tobi_residues = []
        list_of_coordinates = []
        parsed_restraints = {}
        for structure in range(molecule.num_structures):
            coordinates = []
            for residue in residues:
                try:
                    residue_index = TOBIBAHARPotential.recognized_residues.index(
                        residue.name
                    )

                    cx = 0.0
                    cy = 0.0
                    cz = 0.0
                    count = 0
                    chain_id = ""
                    for atom in residue.atoms:
                        if not atom.is_hydrogen():
                            current_atom = "%s%s" % (residue.name, atom.name)
                            ax = molecule.atom_coordinates[structure][atom.index][0]
                            ay = molecule.atom_coordinates[structure][atom.index][1]
                            az = molecule.atom_coordinates[structure][atom.index][2]

                            for atom_type in range(len(TOBIBAHARPotential.atom_types)):
                                if current_atom in TOBIBAHARPotential.atom_types[atom_type]:
                                    cx += ax
                                    cy += ay
                                    cz += az
                                    count += 1
                            if atom.name == "N":
                                coordinates.append([ax, ay, az])
                                tobi_residues.append(20)
                            if atom.name == "O":
                                coordinates.append([ax, ay, az])
                                tobi_residues.append(21)
                            chain_id = atom.chain_id
                    cx /= float(count)
                    cy /= float(count)
                    cz /= float(count)

                    coordinates.append([cx, cy, cz])
                    tobi_residues.append(residue_index)

                    res_id = (
                        f"{chain_id}.{residue.name}.{residue.number}{residue.insertion}"
                    )
                    if restraints and res_id in restraints:
                        parsed_restraints[res_id] = []

                except (ValueError, ZeroDivisionError):
                    continue

            list_of_coordinates.append(SpacePoints(coordinates))

        return DockingModel(tobi_residues, list_of_coordinates, parsed_restraints)


class TOBIBAHAR(ScoringFunction):
    """Implements TOBI potential"""

    def __init__(self, weight=1.0):
        super(TOBIBAHAR, self).__init__(weight, anm_support=False)
        self.function = self._default
        self.potential = TOBIBAHARPotential()
        self.cutoff = DEFAULT_CONTACT_RESTRAINTS_CUTOFF

    def __call__(self, receptor, receptor_coordinates, ligand, ligand_coordinates):
        return self.function(receptor, receptor_coordinates, ligand, ligand_coordinates)

    def _default(self, receptor, receptor_coordinates, ligand, ligand_coordinates):
        energy = 0.0

        dist_matrix = scipy.spatial.distance.cdist(
            receptor_coordinates, ligand_coordinates
        )

        interface_receptor = []
        interface_ligand = []
        for rec_index, rec_tobi in enumerate(receptor.objects):
            for lig_index, lig_tobi in enumerate(ligand.objects):
                d = dist_matrix[rec_index][lig_index]

                if d <= 8.0:
                    if rec_tobi >= 20 and lig_tobi >= 20:
                        # Small distance, backbone-backbone
                        if d <= 4.0:
                            energy += self.potential.tobibahar[rec_tobi][lig_tobi]
                    else:
                        # Medium distance, backbone-sidechain
                        if rec_tobi >= 20 or lig_tobi >= 20:
                            if d <= 5.6:
                                energy += self.potential.tobibahar[rec_tobi][lig_tobi]
                        else:
                            # Large distance, sidechain-sidechain
                            if d <= 6.8:
                                energy += self.potential.tobibahar[rec_tobi][lig_tobi]

                if d <= self.cutoff:
                    interface_receptor.append(rec_index)
                    interface_ligand.append(lig_index)

        interface_receptor = set(interface_receptor)
        interface_ligand = set(interface_ligand)
        energy *= -1.0
        perc_receptor_restraints = ScoringFunction.restraints_satisfied(
            receptor.restraints, interface_receptor
        )
        perc_ligand_restraints = ScoringFunction.restraints_satisfied(
            ligand.restraints, interface_ligand
        )
        return (
            energy + perc_receptor_restraints * energy + perc_ligand_restraints * energy
        ) * self.weight


# Needed to dynamically load the scoring functions from command line
DefinedScoringFunction = TOBIBAHAR
DefinedModelAdapter = TOBIBAHARAdapter
