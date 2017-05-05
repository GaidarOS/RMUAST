# from numpy import pi, sin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from math import pi


def induced_drag(weight, dens, vel, span):
    return (weight ** 2) / (dens * (vel ** 2) * (span ** 2))


def lift_coef(dens, vel, area, lift):
    return (2 * lift) / (dens * area * (vel ** 2))


def parasitic_drag(dens, vel, area):
    return 0.5 * dens * (vel ** 2) * area * 0.03  # drag coef of a naca 0012


def total_drag(weight, dens, vel, span, area):
    return (weight ** 2) / (dens * ((vel + i) ** 2) * (span ** 2)) + (0.5 * dens * ((vel + i) ** 2) * area * 0.03)


def coef_of_lift(a):
    return 2 * pi * a


def sliders_on_changed(val):
    # induced_drag.set_ydata(signal(amp_slider.val, freq_slider.val))
    parasitic_drag.set_ydata(lift_coef(dens, vel, area, lift))
    fig.canvas.draw_idle()


def reset_button_on_clicked(mouse_event):
    freq_slider.reset()
    amp_slider.reset()


def color_radios_on_clicked(label):
    induced_drag.set_color(label)
    # parasitic_drag.set_color(label)
    fig.canvas.draw_idle()


def linecolor_radios_on_clicked(label):
    # induced_drag.set_color(label)
    parasitic_drag.set_color(label)
    fig.canvas.draw_idle()


axis_color = "white"  # 'lightgoldenrodyellow'
fig = plt.figure()

# Initialise values
dens = 1.225        # air density (kg/m^3)
vel = 1            # plane velocity (m/s)
area = 0.8          # wing area (m^2)
lift = 1            # kilogram force (kg)
span = 0.8            # wing span
areaf = 0.1         # parasite area (f)
weight = 0.28          # weight of the plane
angle = 5
i = 0
temp = []
velocity = []
# Draw the plot
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.25, bottom=0.25)
t = np.arange(0, 10.0, 1)


[induced_drag] = ax.plot(induced_drag(weight, dens, vel + t, span), linewidth=2, color='red')

[parasitic_drag] = ax.plot(parasitic_drag(dens, vel + t, areaf), linewidth=2, color='blue')
[total_drag] = ax.plot(total_drag(weight, dens, vel + t, span, areaf), linewidth=2, color='green')

while i < 10:
    # print("total drag:", ((weight ** 2) / (dens * ((vel + i) ** 2) * (span ** 2)) + (0.5 * dens * ((vel+i) ** 2) * area * 0.03)), "velocity:", vel + i)
    # print("parasitic drag:", (weight ** 2) / (dens * ((vel + i) ** 2) * (span ** 2)))
    # print("induced drag:", (0.5 * dens * ((vel + i) ** 2) * area * 0.03))
    temp.append(((weight ** 2) / (dens * ((vel + i) ** 2) * (span ** 2)) + (0.5 * dens * ((vel + i) ** 2) * area * 0.03)))
    velocity.append(vel + i)
    i += 0.1
print("min drag: {},\nvelocity: {} m/s or {:.2f} km/h". format(min(temp), velocity[temp.index(min(temp))] + 1, (velocity[temp.index(min(temp))] + 1) * 3.6))

# ax.set_xlim([0, 10])
# ax.set_ylim([-10, 10])

# Add two sliders for tweaking the parameters
amp_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axis_color)
amp_slider = Slider(amp_slider_ax, 'lift', 0.1, 10.0, valinit=lift)
freq_slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axis_color)
freq_slider = Slider(freq_slider_ax, 'Vel', 0.1, 30.0, valinit=vel)

amp_slider.on_changed(sliders_on_changed)
freq_slider.on_changed(sliders_on_changed)


# Add a button for resetting the parameters
reset_button_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')

reset_button.on_clicked(reset_button_on_clicked)


# Add a set of radio buttons for changing color
color_radios_ax = fig.add_axes([0.025, 0.5, 0.15, 0.15], facecolor=axis_color)
color_radios = RadioButtons(color_radios_ax, ('red', 'green', 'blue', 'white'), active=0)
color_radios_ax_line = fig.add_axes([0.025, 0.8, 0.15, 0.15], facecolor=axis_color)
color_radios_line = RadioButtons(color_radios_ax_line, ('red', 'green', 'blue', 'white'), active=0)


color_radios.on_clicked(color_radios_on_clicked)
color_radios_line.on_clicked(linecolor_radios_on_clicked)


plt.show()
