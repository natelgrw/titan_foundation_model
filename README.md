# ASPECTOR: Analog Circuit Simulation Pipline

The Analog Simulation Performance Extraction and Collection Toolkit for Organized Research (**ASPECTOR**) is a Cadence Spectre based simulation pipeline that searches a wide Analog design space and fine tunes sizing and bias parameters to meet target circuit performance specs.

Current Version: **0.1.3**


![Simulation Pipeline](turbo_optimizer/simulation_pipeline.png)


## ⚡ Current Features

ASPECTOR is capable of optimizing the following primary specs on op-amp Spectre netlists:  

- Gain  
- Unity-Gain Bandwidth (UGBW)  
- Phase Margin (PM)  
- Power  

While simulations compute 11 performance metrics:  

- Gain  
- Unity-Gain Bandwidth (UGBW)
- Phase Margin (PM)  
- Power  
- Common-Mode Rejection Ratio (CMRR)  
- Input Offset Voltage (Vos)  
- Output Voltage Swing  
- Gain Linearity  
- Integrated Noise  
- Slew Rate  
- Settle Time  

Additional repository features include:

- User prompting for vdd, vcm, tempc, transistor cards, and netlist selection
- Compatibility for both single ended and differential operational amplifiers
- 6 demo netlists included for testing and experimentation

## 📖 How to Use

**Requirements:** 
- Linux/Unix environment
- Cadence Spectre, Virtuoso, and ViVA software
- Conda environment with all dependencies specified in `rlenv38.yml`

**1. Clone Repository:**

  ```
  git clone https://github.com/natelgrw/aspector_pipeline.git
  cd aspector_pipeline
  ```

**2. Update Absolute Paths:**
   
   The pipeline currently uses absolute paths in `demo_netlists/`, `rlenv38.yml`, `run_optimizer.sh` and `turbo_optimizer/`. Modify paths in the relevant scripts/config files to match your local directories.
   
**3. Create & Activate Conda Environment:**

  ```
  conda env create -f rlenv38.yml
  conda activate rlenv38
  ```

**4. Run Optimization Pipeline:**

  ```
  cd turbo_optimizer
  chmod +x run_optimizer.sh
  ./run_optimizer.sh
  ```
  
  This script will prompt you to select a demo netlist for simulation, run the TuRBO optimization on the specified specs (gain, UGBW, PM, power), perform repeated Spectre simulations to compute all 11 performance metrics, and save optimized topology, sizing, and metrics to the `results/` folder.
  
  Ensure all absolute paths are updated before running the pipeline. For multiple netlists, repeat `./run_optimizer.sh` or modify the config to include additional files. The pipeline assumes Linux-style paths compatible with Cadence simulations.
