import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

def draw(fileName, ax, TARGET_SIZE, plot_x=True):
    try:
        f = open(fileName, 'r')
        lines = f.readlines()
        xs = []; ys =[]; zs = []
        ratio = 0.0
        first_line = True
        for line in lines:
            if line == "End\n":
                ax.plot(xs,ys,zs,color='black',linewidth='0.5')
                plt.ion()
                plt.draw()
                xs = []; ys =[]; zs = []
            elif first_line:
                line = line.split()
                ratio = float(line[0])/float(line[1])
                first_line = False
            else:
                line = line.split()
                if(plot_x):
                    xs.append((float(line[0])))
                else:
                    xs.append(0.0)
                ys.append((float(line[1])))
                zs.append((float(line[2])))
                
    except:
        print("Error opening the file")

if __name__ == "__main__":
    fileName = '../output/bee_hive_three_ewha_full_path_c.txt'
    # plotting
    fig = plt.figure(figsize=[10,8])
    ax = fig.add_subplot(111, projection="3d")
    ax.grid(False)
    SCALE = 0.3 # normal drawing scale

    draw(fileName, ax, SCALE)

    ax.set_xlim3d(-0.5, 0.5)
    ax.set_ylim3d(-0.5, 0.5)
    ax.set_zlim3d(0.5, 1.5)
    ax.view_init(elev=10., azim=-150)
    plt.show(block=True)


