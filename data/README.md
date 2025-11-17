# NASA C-MAPSS Dataset

## Overview
This directory contains the NASA Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) dataset for turbofan engine degradation simulation.

## Dataset Source
- **Kaggle**: [NASA C-MAPSS Dataset](https://www.kaggle.com/datasets/behrad3d/nasa-cmaps)
- **Original Source**: NASA Ames Prognostics Data Repository

## Download Instructions
The dataset is automatically downloaded using the setup script. Alternatively, you can download it manually:

```bash
curl -L -o nasa-cmaps.zip https://www.kaggle.com/api/v1/datasets/download/behrad3d/nasa-cmaps
unzip nasa-cmaps.zip
```

## Dataset Description

The dataset consists of four different sub-datasets (FD001-FD004), each representing different operating conditions and fault modes:

### FD001
- **Train trajectories**: 100
- **Test trajectories**: 100
- **Conditions**: ONE (Sea Level)
- **Fault Modes**: ONE (HPC Degradation)

### FD002
- **Train trajectories**: 260
- **Test trajectories**: 259
- **Conditions**: SIX
- **Fault Modes**: ONE (HPC Degradation)

### FD003
- **Train trajectories**: 100
- **Test trajectories**: 100
- **Conditions**: ONE (Sea Level)
- **Fault Modes**: TWO (HPC Degradation, Fan Degradation)

### FD004
- **Train trajectories**: 248
- **Test trajectories**: 249
- **Conditions**: SIX
- **Fault Modes**: TWO (HPC Degradation, Fan Degradation)

## Data Format

Each dataset file contains 26 columns separated by spaces:

1. **Unit number**: Engine identifier
2. **Time (cycles)**: Operational cycle number
3. **Operational setting 1**: Operating condition parameter
4. **Operational setting 2**: Operating condition parameter
5. **Operational setting 3**: Operating condition parameter
6-26. **Sensor measurements 1-21**: Various sensor readings from the engine

## Files Structure

```
CMaps/
├── train_FD001.txt         # Training data for FD001
├── test_FD001.txt          # Test data for FD001
├── RUL_FD001.txt           # True RUL values for FD001 test set
├── train_FD002.txt         # Training data for FD002
├── test_FD002.txt          # Test data for FD002
├── RUL_FD002.txt           # True RUL values for FD002 test set
├── train_FD003.txt         # Training data for FD003
├── test_FD003.txt          # Test data for FD003
├── RUL_FD003.txt           # True RUL values for FD003 test set
├── train_FD004.txt         # Training data for FD004
├── test_FD004.txt          # Test data for FD004
├── RUL_FD004.txt           # True RUL values for FD004 test set
└── readme.txt              # Original dataset documentation
```

## Problem Statement

The objective is to predict the **Remaining Useful Life (RUL)** - the number of remaining operational cycles before engine failure. This is a regression problem in the predictive maintenance domain.

### Key Characteristics:
- Time series data from turbofan engines
- Multiple operating conditions
- Sensor noise contamination
- Normal initial wear and manufacturing variation
- Fault develops over time until failure

## Reference
A. Saxena, K. Goebel, D. Simon, and N. Eklund, "Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation", in the Proceedings of the 1st International Conference on Prognostics and Health Management (PHM08), Denver CO, Oct 2008.
