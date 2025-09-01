# ⚡ TITAN: A Foundation Model for Op-Amp Design

TITAN is a foundation model for the topology and sizing optimization of operational amplifiers.

The model is capable of optimizing the following primary specs:  

- Gain  
- Unity-Gain Bandwidth (UGBW)  
- Phase Margin (PM)  
- Power  

While simulations compute 11 performance metrics:  

1. Gain  
2. Unity-Gain Bandwidth (UGBW)
3. Phase Margin (PM)  
4. Power  
5. Common-Mode Rejection Ratio (CMRR)  
6. Input Offset Voltage (Vos)  
7. Output Voltage Swing  
8. Gain Linearity  
9. Integrated Noise  
10. Slew Rate  
11. Settling Time  

## 📍 Features (Version 0.0.2)

- Automated .yaml config handling (NEW)
- 3 demo netlists included for testing and experimentation
- An end-to-end pipeline that runs Cadence simulations and TuRBO optimization on netlists

## 📖 How to Use: 

**Requirements:** 
- Linux/Unix environment
- Cadence Virtuoso + Spectre simulator
- Conda environment with dependencies specified in `rlenv38.yml`.  

**1. Clone Repository:**

  ```
  bash
  git clone <repo_url>
  cd titan_foundation_model
  ```

**2. Update Absolute Paths:**
   
   The pipeline currently uses absolute paths in `demo_configs/`, `demo_netlists/`, and `turbo_optimizer/`. Modify paths in the relevant scripts/config files to match your local directories.
   
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
  
  This script will load your netlists and configuration files, run the TuRBO optimization on the specified specs (gain, UGBW, PM, power), perform repeated Spectre simulations to compute all 11 performance metrics, and save optimized topology, sizing, and metrics to the results/ folder.
  
  Ensure all absolute paths are updated before running the pipeline. For multiple netlists, repeat ./run_optimizer.sh or modify the config to include additional files. The pipeline assumes Linux-style paths compatible with Cadence simulations.
