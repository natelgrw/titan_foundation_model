# ⚡ TITAN: A Foundation Model for Op-Amp Design

TITAN is a foundation model for the topology and sizing optimization of operational amplifiers, currently under active development.

Current Version: **0.1.1**

The model is capable of optimizing the following primary specs:  

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
- Settling Time  

## 📍 Current Features

- User prompting for demo netlist selection (NEW)
- Compatibility for both single ended and differential operational amplifiers
- 6 demo netlists included for testing and experimentation
- An automated end-to-end pipeline that runs Cadence simulations and TuRBO optimization on demo netlists

## 📖 How to Use

**Requirements:** 
- Linux/Unix environment
- Cadence Virtuoso + Spectre simulator
- Conda environment with dependencies specified in `rlenv38.yml`.  

**1. Clone Repository:**

  ```
  git clone https://github.com/natelgrw/titan_foundation_model.git
  cd titan_foundation_model
  ```

**2. Update Absolute Paths:**
   
   The pipeline currently uses absolute paths in `demo_netlists/` and `turbo_optimizer/`. Modify paths in the relevant scripts/config files to match your local directories.
   
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
  
  This script will prompt you toselect a demo netlist for simulation, run the TuRBO optimization on the specified specs (gain, UGBW, PM, power), perform repeated Spectre simulations to compute all 11 performance metrics, and save optimized topology, sizing, and metrics to the results/ folder.
  
  Ensure all absolute paths are updated before running the pipeline. For multiple netlists, repeat ./run_optimizer.sh or modify the config to include additional files. The pipeline assumes Linux-style paths compatible with Cadence simulations.