
	
import matplotlib.pyplot as plt
	
import matplotlib.animation as animation
	
import time
	
import random
	

	
start_time = int(round(time.time()))
	
fig = plt.figure()

axis1 = fig.add_subplot(1,1,1)
fontA = {'family':'serif','color':'blue','size':20}
fontB = {'family':'serif','color':'darkred','size':15}
title = plt.title("Frequency changes detected sensor", fontdict=fontA)

title.set_weight('bold')
plt.xlabel("Time in seconds",fontdict=fontB)
plt.ylabel("Frequency",fontdict=fontB)	

	
xs = []
	
ys = []
	

	
def animate(interval):
	
    ys.append(random.random())
	
    xs.append(int(round(time.time())) - start_time)
	

	

	
    axis1.clear()
	
    axis1.plot(xs, ys)
    title=plt.title("Frequency changes detected by sensor", fontdict=fontA)
    title.set_weight('bold')
    plt.xlabel("Time in seconds",fontdict=fontB)
    plt.ylabel("Frequency",fontdict=fontB)
	

	
ani = animation.FuncAnimation(fig, animate, interval = 1000)
	
plt.show()


















# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time
# import random
# import numpy as np

# start_time = int(round(time.time()))
# fig = plt.figure()
# fontA = {'family':'serif','color':'blue','size':20}
# fontB = {'family':'serif','color':'darkred','size':15}
# title = plt.title("Frequency changes detected sensor", fontdict=fontA)

# title.set_weight('bold')
# plt.xlabel("Time in seconds",fontdict=fontB)
# plt.ylabel("Frequency",fontdict=fontB)
 
# axis1 = fig.add_subplot(1,1,1 )
# axis1.grid("on")


# xs = []
# ys = []
# x_fill = np.linspace(2, 3, 1000)
# plt.fill_between(xs,ys, alpha=0.5)  
 
# def animate(interval):

#     ys.append(random.random())
#     xs.append(int(round(time.time())) - start_time)


#     axis1.clear()
#     axis1.plot(xs, ys, linewidth=3)
#     title=plt.title("Frequency changes detected by sensor", fontdict=fontA)
#     title.set_weight('bold')
#     plt.xlabel("Time in seconds",fontdict=fontB)
#     plt.ylabel("Frequency",fontdict=fontB)
#     axis1.grid("on")
#     plt.fill_between(xs,ys, alpha=0.5)  
   
    
    

# ani = animation.FuncAnimation(fig, animate, interval = 1000)
# plt.show()
