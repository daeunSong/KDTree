import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

def draw(fileName, TARGET_SIZE = 0.5, c='black'):
    try:
        f = open(fileName, 'r')
        lines = f.readlines()
        xs = []; ys =[]; zs = []
        line = lines[0]
        line = line.split()
        ratio = float(line[0])/float(line[1])
        for line in lines[1:]:
            if line == "End\n":
                plt.plot(xs,ys,color=c,linewidth='0.5')
                plt.ion()
                plt.draw()
            else:
                line = line.split()
                xs.append((float(line[0])*ratio*TARGET_SIZE))
                ys.append(-(float(line[1])*TARGET_SIZE))
        plt.plot(xs,ys,color=c, linewidth='0.5')
    except:
        print("Error opening the file")

if __name__ == "__main__":
    fileName = '../input/ewha/ewha_full_path_c.txt'
    # plotting
    fig = plt.figure()
    TARGET_SIZE = 0.5 # normal drawing scale

    draw('../input/ewha/ewha_full_path_c.txt', TARGET_SIZE, 'c')
    draw('../input/ewha/ewha_full_path_m.txt', TARGET_SIZE, 'm')
    draw('../input/ewha/ewha_full_path_y.txt', TARGET_SIZE, 'y')
    draw('../input/ewha/ewha_full_path_k.txt', TARGET_SIZE, 'k')

    # ax.auto_scale_xyz([-3, 3], [-2.5, 2.5], [-1, 4])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show(block=True)


