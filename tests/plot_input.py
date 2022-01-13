import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

def draw(fileName, ax, TARGET_SIZE, plot_x=True):
    try:
        f = open(fileName, 'r')
        lines = f.readlines()
        xs = []; ys =[]; zs = []
        for line in lines:
            ax.plot(xs,ys,zs,color='black',linewidth='0.5')
            line = line.split(';')[1].split(',')
            xs.append((float(line[0])))
            ys.append((float(line[1])))
            zs.append((float(line[2])))
        ax.plot(xs,ys,zs)
    except:
        print("Error opening the file")

if __name__ == "__main__":
    # fileName = '../output/normal/curved_surface_ewha_full_path_m.txt'
    fileName = '../input/hello'
    # plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.grid(False)
    SCALE = 0.3 # normal drawing scale

    draw(fileName, ax, SCALE)

    # ax.auto_scale_xyz([-3, 3], [-2.5, 2.5], [-1, 4])
    plt.show(block=True)


