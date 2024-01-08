import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import h5py  # Import the h5py library
import scienceplots

plt.style.use(["science", "ieee", "vibrant"])

joint_indices = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
joint_indices_measured = [4, 5, 6, 0, 1, 2, 7, 8, 9, 10]
joint_names = [
    "torso pitch",
    "torso roll",
    "torso yaw",
    "neck pitch",
    "neck roll",
    "neck yaw",
    "shoulder pitch",
    "shoulder roll",
    "shoulder yaw",
    "elbow",
]


matfile = h5py.File("./experiments/robot_logger_device_2023_09_14_13_13_26.mat", "r")

joints_mann = np.squeeze(
    matfile["robot_logger_device"]["walking"]["joints_state"]["positions"]["mann"][
        "data"
    ]
)
joints_desired = np.squeeze(
    matfile["robot_logger_device"]["walking"]["joints_state"]["positions"]["desired"][
        "data"
    ]
)
joints_measured = np.squeeze(
    matfile["robot_logger_device"]["joints_state"]["positions"]["data"]
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

fig, axs = plt.subplots(2, 5, sharex=True, sharey=False, figsize=(7.5, 2))
# add spacing between the subplots
fig.subplots_adjust(hspace=0.45, wspace=0.45)

# add space for the y and x labels
fig.subplots_adjust(left=0.08, bottom=0.2)


# plot all the joints
for i in range(2):
    for j in range(5):
        index = i * 5 + j

        # plot the joint with a given thickness
        axs[i][j].plot(
            time, joints_mann[:, joint_indices[index]], label="postural", linewidth=0.5
        )
        # axs[i][j].plot(time, joints_desired[:, joint_indices[index]], label="desired", linewidth=0.5)
        axs[i][j].plot(
            time_measured,
            joints_measured[:, joint_indices_measured[index]],
            label="measured",
            linewidth=0.5,
        )
        # set the title
        axs[i][j].set_title(joint_names[index])
        # set the x limits
        axs[i][j].set_xlim([time[0], time[-1]])


fig.supxlabel("time (s)")
fig.supylabel("joint angle (rad)")


# move the legend outside the plot put it at the same hight of the x label
plt.legend(bbox_to_anchor=(-0.1, -0.85), loc="lower center", ncol=2)
plt.savefig("joints_postural.pdf")
