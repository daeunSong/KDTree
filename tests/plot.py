import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

class Surface:
    fileName = '../input/curved_surface_yz.obj'
    faces = []
    mid_y = 0
    min_z = 0

    def readMesh (self):
        vertices = []
        normals = []
        min_y = min_z = 1000
        max_y = max_z = -1000
        try:
            f = open(self.fileName, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split()
                if line[0] == 'v': # vertex
                    coord = list(map(float,line[1:]))
                    min_y = min(min_y, coord[1])
                    min_z = min(min_z, coord[2])
                    max_y = max(max_y, coord[1])
                    max_z = max(max_z, coord[2])
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

        self.mid_y = (min_y+max_y)/2
        self.min_z = min_z
        

def plot_faces (surf, ax, plot_normals = True):
    faces = surf.faces
    for face in faces:
        face['vertex'].append(face['vertex'][0])
        face['normal'].append(face['normal'][0])
        xs = []; ys =[]; zs = []
        for i in range(len(face['vertex'])):
            vertex = face['vertex'][i]
            normal = face['normal'][i]
            xs.append(vertex[0])
            ys.append(vertex[1] - surf.mid_y)
            zs.append(vertex[2] - surf.min_z)
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
        f = open('vector_input/prague/'+fileName, 'r')
        f_ = open('vector_input/prague/converted/'+fileName,'w')
        lines = f.readlines()
        xs = []; ys =[]; zs = []
        ratio = 0.0
        first_line = True
        cnt = 0
        x_prev = None
        y_prev = None
        
        line = lines[0]
        line = line.split()
        width = float(line[0])
        height = float(line[1])
        ratio = width/height
        f_.write(str(width)+" "+str(height)+"\n")

        for line in lines[1:]:
            if line == "#\n":
                x_prev = None
                y_prev = None
                if len(xs) > 2 :
                    ax.plot(xs,ys,color=color_,linewidth='0.9')
                    plt.ion()
                    plt.draw()
                    for i in range(len(xs)):
                        f_.write(str(xs[i]/width)+" "+str(-ys[i]/height)+"\n")
                    f_.write("End\n")
                xs = []; ys =[]; zs = []
            else:
                line = line.split(',')
                x = float(line[0])
                y = -float(line[1])
                #print(x, y)
                if x_prev != None:
                    dist = (x - x_prev)**2 + (y - y_prev)**2
                    #print(dist)
                    if (dist > 1000):
                        for i in range(len(xs)):
                            f_.write(str(xs[i]/width)+" "+str(-ys[i]/height)+"\n")
                        f_.write("End\n")
                        ax.plot(xs,ys,color=color_,linewidth='0.9')
                        plt.ion()
                        plt.draw()
                        xs = []; ys =[];
                xs.append(x)
                ys.append(y)
                x_prev = x
                y_prev = y
                # zs.append((float(line[2])))

                # if(cnt % 900 == 0 and plot_n):
                #     pt = [float(line[0]), float(line[1]), float(line[2])]
                #     normal= [float(line[3]), float(line[4]), float(line[5])]
                #     # ax.scatter(pt[0],pt[1],pt[2], color="black")
                #     plot_normal(pt, normal, ax)
            cnt += 1
        f_.close()
                
    except:
        print("Error opening the file")

if __name__ == "__main__":
    # plotting
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection="3d")
    ax = fig.add_subplot()
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.grid(False)
    SCALE = 0.3 # normal drawing scale
    NORMAL = False

    # # plot wall
    # surf = Surface()
    # surf.fileName = '../input/bee_hive_three.obj'
    # surf.readMesh()
    # plot_faces(surf, ax, False)

    # plot drawing - C
    # fileName = '../output/normal/bee_hive_three_hello_world_path_k.txt'
    # fileName = 'dogs_r.txt'
    # draw(fileName, ax, SCALE, 'r', NORMAL)
    # fileName = 'dogs_y.txt'
    # draw(fileName, ax, SCALE, 'y', NORMAL)
    fileName = 'prague_k.txt'
    draw(fileName, ax, SCALE, 'k', NORMAL)
    # plot drawing - M
    #fileName = '../output/normal/bee_hive_2_face_ewha_full_path_m.txt'
    #draw(fileName, ax, SCALE, 'm', NORMAL)
    # plot drawing - Y
    #fileName = '../output/normal/bee_hive_2_face_ewha_full_path_y.txt'
    #draw(fileName, ax, SCALE, 'y', NORMAL)
    # plot drawing - K
    #fileName = '../output/normal/bee_hive_2_face_ewha_full_path_k.txt'
    #draw(fileName, ax, SCALE, 'k', NORMAL)

    # ax.auto_scale_xyz([-1, 1], [-1, 1], [0, 2])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show(block=True)


    



