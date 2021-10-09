import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

class Surface:
    fileName = '../input/bee_hive_1_face.obj'
    faces = []

    def readMesh (self):
        vertices = []
        normals = []
        try:
            f = open(self.fileName, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split()
                if line[0] == 'v': # vertex
                    coord = list(map(float,line[1:]))
                    vertices.append(coord)
                elif line[0] == 'vn': # vertex normal
                    coord = list(map(float,line[1:]))
                    normals.append(coord)
                elif line[0] == 'f': # face
                    face = {'vertex':[],'normal':[]}
                    line = line[1:]
                    for el in line:
                        indicies = list(map(int,el.split('//')))
                        face['vertex'].append(vertices[indicies[0]-1])
                        face['normal'].append(normals[indicies[1]-1])
                    self.faces.append(face)
        except:
            print("Error opening the file")

def plot_faces (faces, ax, plot_normals = True):
    for face in faces:
        face['vertex'].append(face['vertex'][0])
        face['normal'].append(face['normal'][0])
        xs = []; ys =[]; zs = []
        for i in range(len(face['vertex'])):
            vertex = face['vertex'][i]
            normal = face['normal'][i]
            xs.append(vertex[0])
            ys.append(vertex[1])
            zs.append(vertex[2])
            if plot_normals:
                plot_normal (vertex, normal, ax)

        ax.plot(xs,ys,zs,color='black',linewidth='0.1')
        plt.ion()
        plt.draw()

def plot_normal (vertex, normal, ax):
    p1 = vertex
    p2 = list(np.array(vertex) + np.array(normal)*SCALE)
    xs = [p1[0], p2[0]]
    ys = [p1[1], p2[1]]
    zs = [p1[2], p2[2]]

    ax.plot(xs,ys,zs,color='black',linewidth='1.0')
    
    plt.ion()
    plt.draw()

def draw(fileName, ax, TARGET_SIZE, color_, plot_n=True):
    try:
        f = open(fileName, 'r')
        lines = f.readlines()
        xs = []; ys =[]; zs = []
        ratio = 0.0
        first_line = True
        cnt = 0
        for line in lines:
            if line == "End\n":
                ax.plot(xs,ys,zs,color=color_,linewidth='0.5')
                plt.ion()
                plt.draw()
                xs = []; ys =[]; zs = []
            elif first_line:
                line = line.split()
                ratio = float(line[0])/float(line[1])
                first_line = False
            else:
                line = line.split()
                xs.append((float(line[0])))
                ys.append((float(line[1])))
                zs.append((float(line[2])))

                if(cnt % 900 == 0 and plot_n):
                    pt = [float(line[0]), float(line[1]), float(line[2])]
                    normal= [float(line[3]), float(line[4]), float(line[5])]
                    # ax.scatter(pt[0],pt[1],pt[2], color="black")
                    plot_normal(pt, normal, ax)
            cnt += 1
                
    except:
        print("Error opening the file")

if __name__ == "__main__":
    # plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.grid(False)
    SCALE = 0.3 # normal drawing scale

    # plot wall
    surf = Surface()
    surf.fileName = '../input/bee_hive_2_face.obj'
    surf.readMesh()
    plot_faces(surf.faces, ax, False)

    # plot drawing - C
    fileName = '../output/normal/bee_hive_2_face_ewha_full_path_c.txt'
    draw(fileName, ax, SCALE, 'c', True)
    # plot drawing - M
    fileName = '../output/normal/bee_hive_2_face_ewha_full_path_m.txt'
    draw(fileName, ax, SCALE, 'm', True)
    # plot drawing - Y
    fileName = '../output/normal/bee_hive_2_face_ewha_full_path_y.txt'
    draw(fileName, ax, SCALE, 'y', True)
    # plot drawing - K
    fileName = '../output/normal/bee_hive_2_face_ewha_full_path_k.txt'
    draw(fileName, ax, SCALE, 'k', True)

    ax.auto_scale_xyz([-1, 1], [-1.8, 0.2], [0, 2])
    plt.show(block=True)


