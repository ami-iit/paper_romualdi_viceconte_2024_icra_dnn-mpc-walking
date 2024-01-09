# 📚 Plotting for Online DNN-driven Nonlinear MPC in Stylistic Humanoid Robot Walking with Step Adjustment

This directory contains the scripts used to create the plots presented in the paper. The plots have been generated using the dataset stored in [Hugging Face 🤗](https://huggingface.co/datasets/ami-iit/paper_romualdi_viceconte_2024_icra_dnn-mpc-walking_dataset). Ensure that the dataset is saved in the `experiments` folder, which should be located in the same directory as this `README`.

## Requirements
The scripts are written in Python, and the necessary packages are listed in [`requirements.txt`](./requirements.txt). To install them, run:
```console
pip install -r requirements.txt
```
⚠️ We recommend using a virtual environment.

## Usage
The following scripts are available:
- `animate_plot_steps_and_com.py`: Generates an animation of the robot walking and plots the steps and CoM trajectories.
- `plot_steps_and_com.py`: Generates plots of the steps and CoM trajectories.
- `plot_joints.py`: Generates plots of the joints trajectories.
- `plot_computational_time.py`: Generates plots of the computational time for MPC and DNN.
