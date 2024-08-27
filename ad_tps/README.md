# Demo: Transition Path Sampling of Solvated Alanine Dipeptide

## Overview

This tutorial gives a good overview of a realistic process for setting up a
biomolecular transition path sampling simulation using OpenPathSampling.

1. Use `openmm-setup` to interactively create the input files for OPS.
2. Use the `openpathsampling` CLI to generate an initial trajectory using a
   high-temperature engine.
3. Use the `openpathsampling` CLI to run the TPS simulation.
4. Use `patheract` to visualize the results.

## Manifest

* `ad.pdb`: Initial conditions snapshot
* `ad_tps.yaml`: OPS CLI YAML input file
* `system_amber96.xml`: Pre-made AMBER96 
* `misc/`: Scripts used in setup. In particular, includes the script to create
  the `system_amber96.xml` file (the AMBER96 force field is not available in
  `openmm-setup`, since it is extremely outdated).
* `environment.yaml`: Environment file for `conda`

## Steps

### Create and activate the conda environment

We use a different environment for each demo in this repository.  

1. Create the environment with `conda env `
2. Activate with `conda activate

### Use `openmm-setup` to create input files

1.  Run the command `openmm-setup` to launch the app
2.  Select PDB as file type
3.  Browse to select the `ad.pdb` file from this directory as the input file.
    Force field and water model don't matter here, but in real situations you
    should use the best choices for your system. In this case, we can also
    select "No. My file is ready to simulate." However, in real use cases you
    might need additional cleanup.
4.  Under Integrator, first use the defaults.
5.  Under Simulation, set the simulation length and equilibration length to
    0 steps. We're use using this to generate XML output files. You probably
    also need to set the platform to CPU.
6.  Under Output, check the box to "Save simulation setup as XML files."
7.  Click on the "Run Simulation" button at the top.
8.  Change the working directory to be subdirectory called `setup` within this
    demo directory, and press "Start."
9.  Create the high-temperature integrator: Press your browser's "Back" button
    to go back to the setup screen.
10. Under the "Integrator" tab, set the temperature to 500.
11. Under the "Output" tab, rename the integrator XML output file to
    `hi_temp_integrator.xml`.
12. Check that you still have 0 steps of equilibration/production MD, and click
    the "Run Simulation" button again.
13. Again set the path to the `setup` subdirectory of this directory, and click
    "Start" to create the files.

You can check the `setup` directory to see the two integrator files. These are
human-readable XML files; you should be able to confirm that you have the right
temperatures set in each.

### Use the `openpathsampling` CLI to generate an initial trajectory

1. Compile the YAML to create an OPS database file:

   ```bash
   openpathsampling compile ad_tps.yaml -o tps_setup.db
   ```

2. Load the initial snapshot into the database.

    ```bash
    openpathsampling load_trajectory ad.pdb -a tps_setup.db --tag "initial_snapshot"
    ```

3. Use the high-temperature engine to create an initial trajectory.

    ```bash
    openpathsampling visit-all -o init_traj.db -s C_7eq -s alpha_R -e hi_temp_integrator tps_setup.db
    ```

4. [Skipped in live demo] Equilibrate the trajectory. First, copy the move
   scheme over to the `equil.db` file

    ```bash
    openpathsampling append --scheme one-way-scheme -a init_traj.db tps_setup.db
    openpathsampling equilibrate -o equil.db init_traj.db
    ```

5. Copy the equilibrated trajectory back to the main setup database.

    ```bash
    openpathsampling append --tag equilibrated --save-tag initial_conditions -a tps_setup.db equil.db
    ```

### Use the `openpathsampling` CLI to run the TPS simulation

```bash
openpathsampling pathsampling tps_setup.db -o tps_run.db -n 100
```

### Use `patheract` to visualize the results

In the demo, we'll cheat and load a pre-run simulation

```bash
openpathsampling patheract tps_run.db
```
