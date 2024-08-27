"""

"""

import openmm as mm
from openmm import app
from openmm import unit


def create_system(pdb_filename):
    pdb = app.PDBFile(pdb_filename)
    forcefield = app.ForceField('amber96.xml', 'tip3p.xml')

    system = forcefield.createSystem(
        topology=pdb.topology,
        nonbondedMethod=app.PME,
        nonbondedCutoff=1.0*unit.nanometers,
        constraints=app.HBonds,
        rigidWater=True,
        ewaldErrorTolerance=0.0005,
    )
    return system


if __name__ == "__main__":
    import sys
    pdb_filename = sys.argv[1]
    system = create_system(pdb_filename)
    serialized = mm.XmlSerializer.serialize(system)
    with open("system_amber96.xml", mode='w') as f:
        f.write(serialized)
