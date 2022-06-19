import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

def draw(fileName, TARGET_SIZE = 0.5, c='black'):
    try:
        f = open(fileName, 'r')
        w = open('../input/grid_fix.txt', 'w')
        lines = f.readlines()
        xs = []; ys =[]
        stroke_num = 0
        prev_stroke_num = 0
        for line in lines:
            line = line.split()
            stroke_num = int(line[0])
            if stroke_num != prev_stroke_num:
                plt.plot(xs,ys,color=c,linewidth='0.5')
                plt.ion()
                plt.draw()
                xs = []; ys = []
                w.write('End\n')
            xs.append((float(line[1])-0.25)*2)
            ys.append((float(line[2])-0.25)*2)
            prev_stroke_num = stroke_num
            w.write(str((float(line[1])-0.25)*2)+" "+str((float(line[2])-0.25)*2)+"\n")
        plt.plot(xs,ys,color=c, linewidth='0.5')
        w.write('End\n')
        w.close()
        f.close()
    except:
        print("Error opening the file")

if __name__ == "__main__":
    fileName = '../input/grid.txt'
    # plotting
    fig = plt.figure()
    TARGET_SIZE = 0.5 # normal drawing scale

    draw(fileName, TARGET_SIZE, 'k')

    # ax.auto_scale_xyz([-3, 3], [-2.5, 2.5], [-1, 4])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show(block=True)


