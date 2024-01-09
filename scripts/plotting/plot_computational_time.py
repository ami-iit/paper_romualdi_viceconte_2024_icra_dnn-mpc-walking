import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import h5py  # Import the h5py library
import scienceplots

plt.style.use(["science", "ieee", "vibrant"])

matfile = h5py.File("./experiments/robot_logger_device_2023_09_14_13_13_26.mat", "r")
mpc_time = np.squeeze(
    matfile["robot_logger_device"]["walking"]["computation_time"]["CentroidalMPC"][
        "data"
    ]
)
mann_time = np.squeeze(
    matfile["robot_logger_device"]["walking"]["computation_time"]["AdherentMPC"]["data"]
)
wbc_time = np.squeeze(
    matfile["robot_logger_device"]["walking"]["computation_time"]["WholeBodyQP"]["data"]
)

time = np.squeeze(
    matfile["robot_logger_device"]["walking"]["joints_state"]["positions"]["desired"][
        "timestamps"
    ]
)
time_measured = np.squeeze(
    matfile["robot_logger_device"]["joints_state"]["positions"]["timestamps"]
)

time_measured = time_measured - time[0]
time = time - time[0]


# create a subplot with 2 rows and 5 columns and set the size of the figure

fig, ax = plt.subplots(1, sharex=True, sharey=False, figsize=(3.41, 1.5))

ax.plot(time, mann_time, label="Trajectory generation", linewidth=0.5)
ax.plot(time, wbc_time, label="Trajectory control", linewidth=0.5)
ax.plot(time, mpc_time, label="Trajectory optimization", linewidth=0.5)
ax.set_ylim([-0.005, 0.075])
ax.set_xlim([time[0], time[-1]])

print("max mann time: ", np.max(mann_time))
print("average mann time: ", np.average(mann_time))

print("max mpc time: ", np.max(mpc_time))
print("average mpc time: ", np.average(mpc_time))

print("max wbc time: ", np.max(wbc_time))
print("average wbc time: ", np.average(wbc_time))

print("mann + mpc max time", np.max(mann_time + mpc_time))
print("mann + mpc average time", np.average(mann_time + mpc_time))

print("mpc stance", np.average(np.hstack((mpc_time[0:750], mpc_time[8000:]))))
print("mpc wealking", np.average(mpc_time[800:7900]))


ax.set_xlabel("time (s)")
ax.set_ylabel("computation time (s)")

# move the legend outside the plot put it at the same hight of the x label
plt.legend(loc="best", ncol=1)

plt.savefig("time.pdf")
