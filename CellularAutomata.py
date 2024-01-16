# import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

powers_of_two = np.array([[4], [2], [1]])  # shape (3, 1)

def step(x, rule_binary):

    x_shift_right = np.roll(x, 1)  # circular shift to right
    x_shift_left = np.roll(x, -1)  # circular shift to left
    y = np.vstack((x_shift_right, x, x_shift_left)).astype(np.int8)  # stack row-wise, shape (3, cols)
    z = np.sum(powers_of_two * y, axis=0).astype(np.int8)  # LCR pattern as number

    return rule_binary[7 - z]

def cellular_automaton(rule_number, size, steps,
                       init_cond='random', impulse_pos='center'):

    assert 0 <= rule_number <= 255
    assert init_cond in ['random', 'impulse']
    assert impulse_pos in ['left', 'center', 'right']

    rule_binary_str = np.binary_repr(rule_number, width=8)
    rule_binary = np.array([int(ch) for ch in rule_binary_str], dtype=np.int8)
    x = np.zeros((steps, size), dtype=np.int8)

    if init_cond == 'random':  # random init of the first step
        x[0, :] = np.array(np.random.rand(size) < 0.5, dtype=np.int8)

    if init_cond == 'impulse':  # starting with an initial impulse
        if impulse_pos == 'left':
            x[0, 0] = 1
        elif impulse_pos == 'right':
            x[0, size - 1] = 1
        else:
            x[0, size // 2] = 1

    for i in range(steps - 1):
        x[i + 1, :] = step(x[i, :], rule_binary)

    return x

rule_number = 165  # select the update rule
size = 100  # number of cells in one row
steps = 300  # number of time steps
init_cond='impulse'  # start with only one cell
impulse_pos='center'  # start with the central cell

x = cellular_automaton(rule_number, size, steps, init_cond, impulse_pos)
steps_to_show = 100  # number of steps to show in the animation window
iterations_per_frame = 1 # how many steps to show per frame
frames = int(steps // iterations_per_frame)  # number of frames in the animation
interval=50  # interval in ms between consecutive frames

fig = plt.figure(figsize=(10, 10))

ax = plt.axes()
ax.set_axis_off()

def animate(i):
    ax.clear()  # clear the plot
    ax.set_axis_off()  # disable axis

    Y = np.zeros((steps_to_show, size), dtype=np.int8)  # initialize with all zeros
    upper_boundary = (i + 1) * iterations_per_frame  # window upper boundary
    lower_boundary = 0 if upper_boundary <= steps_to_show else upper_boundary - steps_to_show  # window lower bound.
    for t in range(lower_boundary, upper_boundary): # assign the values
      Y[t - lower_boundary, :] = x[t, :]

    img = ax.imshow(Y, interpolation='none',cmap='binary')
    return [img]

# call the animator
anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval, blit=True)
plt.show()