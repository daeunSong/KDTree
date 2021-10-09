import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

def draw(fileName, ax, TARGET_SIZE):
    try:
        f = open(fileName, 'r')
        lines = f.readlines()
        xs = []; ys =[]; zs = []
        ratio = 0.0
        first_line = True
        for line in lines:
            if line == "End\n":
                ax.plot(ys,zs,color='black',linewidth='0.5')
                plt.ion()
                plt.draw()
                xs = []; ys =[]; zs = []
            elif first_line:
                line = line.split()
                ratio = float(line[0])/float(line[1])
                first_line = False
            else:
                line = line.split()
                ys.append((float(line[0])))#-0.5) * ratio * TARGET_SIZE)
                zs.append((float(line[1])))# * TARGET_SIZE)
                
    except:
        print("Error opening the file")

if __name__ == "__main__":
    fileName = '../input/drawing_input_logs/graffiti_pink/final_path/ewha/ewha_full_path_k.txt'
    # plotting
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(False)
    SCALE = 0.3 # normal drawing scale

    draw(fileName, ax, SCALE)

    # ax.auto_scale_xyz([-3, 3], [-2.5, 2.5], [-1, 4])
    plt.show(block=True)


