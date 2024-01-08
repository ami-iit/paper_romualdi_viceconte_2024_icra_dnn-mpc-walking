import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import h5py  # Import the h5py library
import scienceplots
from PIL import ImageColor

plt.style.use(["science", "ieee", "vibrant"])

external_push_index = [5447, 6120]

# limit = 8348
limit = None


matfile = h5py.File("./experiments/robot_logger_device_2023_09_14_13_13_26.mat", "r")
left_foot = np.squeeze(
    matfile["robot_logger_device"]["walking"]["left_foot"]["position"]["desired"][
        "data"
    ]
)
right_foot = np.squeeze(
    matfile["robot_logger_device"]["walking"]["right_foot"]["position"]["desired"][
        "data"
    ]
)
left_foot_orientation = np.squeeze(
    matfile["robot_logger_device"]["walking"]["left_foot"]["orientation"]["desired"][
        "data"
    ]
)
right_foot_orientation = np.squeeze(
    matfile["robot_logger_device"]["walking"]["right_foot"]["orientation"]["desired"][
        "data"
    ]
)
left_foot_nominal = np.squeeze(
    matfile["robot_logger_device"]["walking"]["contact"]["left_foot"]["position"][
        "nominal"
    ]["data"]
)
right_foot_nominal = np.squeeze(
    matfile["robot_logger_device"]["walking"]["contact"]["right_foot"]["position"][
        "nominal"
    ]["data"]
)

if not limit:
    limit = left_foot.shape[0]

external_push = np.squeeze(
    matfile["robot_logger_device"]["walking"]["external_wrench"]["filtered"]["data"]
)

com = np.squeeze(
    matfile["robot_logger_device"]["walking"]["com"]["position"]["mpc_output"]["data"]
)
com_mann = np.squeeze(
    matfile["robot_logger_device"]["walking"]["com"]["position"]["mann"]["data"]
)

chunk_index_left = find_non_zero_chunks_with_threshold(left_foot[:limit, 2], 0.00001)
chunk_index_right = find_non_zero_chunks_with_threshold(right_foot[:limit, 2], 0.00001)

print(chunk_index_left)
print(chunk_index_right)

color_left = [0.4940, 0.1840, 0.5560, 0.8]
color_left = to_rgb("#7eb0d5", 0.9)
color_right = color_left

color_left_nominal = [0.4660, 0.6740, 0.1880, 0.8]
color_left_nominal = to_rgb("#b2e061", 0.9)
color_right_nominal = color_left_nominal

color_arrow = [0.6350, 0.0780, 0.1840]

fig, ax = plt.subplots(1, sharex=True, sharey=False, figsize=(3.41, 3.41))
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
# ax.set_xlim(-0.15, 1.65)
ax.set_ylim(-0.75, 0.25)

# set axis equal aspect ratio
ax.set_aspect("equal", "box")

plot_rectangle_2D(
    ax, left_foot_nominal[0, :], left_foot_orientation[0, :], color_left_nominal
)
plot_rectangle_2D(
    ax, right_foot_nominal[0, :], right_foot_orientation[0, :], color_right_nominal
)

plot_rectangle_2D(ax, left_foot[0, :], left_foot_orientation[0, :], color_left)
plot_rectangle_2D(ax, right_foot[0, :], right_foot_orientation[0, :], color_right)

label = "Nominal"
for i in range(chunk_index_left.shape[0]):
    plot_rectangle_2D(
        ax,
        left_foot_nominal[chunk_index_left[i, 1] + 10, :],
        left_foot_orientation[chunk_index_left[i, 1] + 10, :],
        color_left_nominal,
        label=label,
    )
    label = None

for i in range(chunk_index_right.shape[0]):
    plot_rectangle_2D(
        ax,
        right_foot_nominal[chunk_index_right[i, 1] + 10, :],
        right_foot_orientation[chunk_index_right[i, 1] + 10, :],
        color_right_nominal,
    )

label = "Adjusted"
for i in range(chunk_index_left.shape[0]):
    plot_rectangle_2D(
        ax,
        left_foot[chunk_index_left[i, 1] + 10, :],
        left_foot_orientation[chunk_index_left[i, 1] + 10, :],
        color_left,
        label=label,
    )
    label = None

for i in range(chunk_index_right.shape[0]):
    plot_rectangle_2D(
        ax,
        right_foot[chunk_index_right[i, 1] + 10, :],
        right_foot_orientation[chunk_index_right[i, 1] + 10, :],
        color_right,
    )


# plot the com  and com_mann
ax.plot(
    com[:limit, 0],
    com[:limit, 1],
    linewidth=1,
    label="CoM MPC",
    color=to_rgb("#ef9b20"),
)
ax.plot(
    com_mann[:limit, 0],
    com_mann[:limit, 1],
    linewidth=1,
    label="CoM nominal",
    color=to_rgb("#9b19f5"),
)

for i in external_push_index:
    draw_arrow(
        ax,
        com[i, 0],
        com[i, 1],
        external_push[i, 0] / 2,
        external_push[i, 1] / 2,
        arrow_length=0.05,
        color=color_arrow,
        label=label,
    )

    print("push force ", np.linalg.norm(external_push[i, :]) * 56)
    label = None

# show legend
ax.legend(ncol=2)

plt.savefig("steps_and_com.pdf")


# print the distance of the footsteps
for i in range(chunk_index_right.shape[0]):
    print(
        "right foot distance",
        np.linalg.norm(
            right_foot[chunk_index_right[i, 1], :]
            - right_foot_nominal[chunk_index_right[i, 1] + 10, :]
        ),
    )


for i in range(chunk_index_left.shape[0]):
    print(
        "left foot distance",
        np.linalg.norm(
            left_foot[chunk_index_left[i, 1], :]
            - left_foot_nominal[chunk_index_left[i, 1] + 10, :]
        ),
    )
