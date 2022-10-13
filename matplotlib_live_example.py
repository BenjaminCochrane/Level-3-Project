import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import random

start_time = int(round(time.time()))
fig = plt.figure()
axis1 = fig.add_subplot(1,1,1)

xs = []
ys = []

def animate(interval):
    ys.append(random.random())
    xs.append(int(round(time.time())) - start_time)


    axis1.clear()
    axis1.plot(xs, ys)

ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()
