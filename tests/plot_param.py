import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np
from math import sqrt

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2) # return index

'''
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)

def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors

def find_quad (list, point):
    quad = [0,0,0,0]
    for candidate in list:
        # TOP RIGHT
        if candidate[0] >= point[0] and candidate[1] >= point[1]:
            if quad[0] != 0: quad[0] = candidate
        # TOP LEFT
        elif candidate[0] < point[0] and candidate[1] >= point[1]:
            if quad[1] != 0: quad[1] = candidate
        elif candidate[0] < point[0] and candidate[1] < point[1]:
            if quad[2] != 0: quad[2] = candidate
        elif candidate[0] >= point[0] and candidate[1] < point[1]:
            if quad[3] != 0: quad[3] = candidate
    return quad
'''

def mapping (surface, drawing):
    f = open('../output/half_sphere_grid.txt', 'w')
    for stroke in drawing.strokes:
        for point in stroke:
            index = closest_node(point, surface.uvs)
            vertex = surface.vertices[index]
            normal = surface.normals[index]
            f.write(str(vertex[0])+" "+str(vertex[1])+" "+str(vertex[2])+" "+str(normal[0])+" "+str(normal[1])+" "+str(normal[2])+"\n")
        f.write('End\n')
    f.close()

class Drawing:
    fileName = '../intput/grid_fix.txt'
    strokes = []
    strokes_3d = []
    ratio = 1.0
    target_size = 0.1 # 10cm

    def __init__(self, fileName):
        self.fileName = fileName
        self.readFile()

    def readFile (self):
        f = open(self.fileName, 'r')
        lines = f.readlines()
        line = lines[0]
        line = line.split()
        self.ratio = float(line[0])/float(line[1])
        stroke = []
        for line in lines[1:]:
            if line == "End\n":
                self.strokes.append(stroke)
                stroke = []
            else:
                line = line.split()
                x = float(line[0])* 0.5 + 0.25 # fit in uv space
                y = float(line[1])* 0.5 + 0.25 # fit in uv space
                stroke.append([x,y])
        f.close()

    def plot_param_drawing (self, ax):
        for stroke in self.strokes:
            xs = np.array(stroke).T[0]
            ys = np.array(stroke).T[1]
            ax.plot(xs,ys,color='black',linewidth='0.5')
            plt.ion()
            plt.draw()

    def plot_3d_drawing (self, ax):
        f = open('../output/half_sphere_grid.txt', 'r')
        lines = f.readlines()
        stroke = []
        for line in lines:
            if line == "End\n":
                self.strokes_3d.append(stroke)
                stroke = []
            else:
                line = line.split()
                x = float(line[0])
                y = float(line[1])
                z = float(line[2])
                stroke.append([x,y,z])
        for stroke in self.strokes_3d:
            xs = np.array(stroke).T[0]
            ys = np.array(stroke).T[1]
            zs = np.array(stroke).T[2]
            ax.plot(xs,ys,zs,color='black',linewidth='0.5')

class Surface:
    fileName = '../input/half_sphere_out.obj'
    faces = []  # contains vertices, uvs, normals per face
    vertices = [] # contains vertices, uvs, normals
    uvs = []
    normals = []
    num_ver = 0

    def __init__(self, fileName):
        self.fileName = fileName
        self.readMesh()

    def readMesh (self):
        vertices = []
        normals = []
        uvs = []
        init = False
        check_index = []
        try:
            f = open(self.fileName, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split()
                # point = {'vertex':[], 'uv':[], 'normal':[]}
                if line[0] == 'v': # vertex
                    coord = list(map(float,line[1:]))
                    vertices.append(coord)
                    self.num_ver = self.num_ver + 1
                    # point['vertex'] = coord
                elif line[0] == 'vt': # uv
                    coord = list(map(float,line[1:]))
                    uvs.append(coord)
                    # point['uv'] = coord
                elif line[0] == 'vn': # vertex normal
                    coord = list(map(float,line[1:]))
                    normals.append(coord)
                    # point['normal'] = coord
                elif line[0] == 'f': # face
                    face = {'vertex':[], 'uv':[], 'normal':[]}
                    line = line[1:]
                    if not init :
                        check_index = list(np.zeros(self.num_ver))
                        init = True
                    for el in line:
                        indicies = list(map(int,el.split('/')))
                        face['vertex'].append(vertices[indicies[0]-1])
                        face['uv'].append(uvs[indicies[1]-1])
                        face['normal'].append(normals[indicies[2]-1])
                        if check_index[indicies[0]-1] == 0:
                            self.vertices.append(vertices[indicies[0]-1])
                            self.uvs.append(uvs[indicies[1]-1])
                            self.normals.append(normals[indicies[2]-1])
                            check_index[indicies[0]-1] = 1
                    self.faces.append(face)
                # self.points.append(point)
        except:
            print("Error opening the file")


    def plot_param (self, ax):
        for face in self.faces:
            # face['vertex'].append(face['vertex'][0])
            face['uv'].append(face['uv'][0])
            face['normal'].append(face['normal'][0])
            xs = []; ys =[]
            for i in range(len(face['vertex'])):
                # vertex = face['vertex'][i]
                vertex = face['uv'][i]
                normal = face['normal'][i]
                xs.append(vertex[0])
                ys.append(vertex[1])
                # if plot_normals:
                #     plot_normal (vertex, normal, ax)

            ax.plot(xs,ys,color='gray',linewidth='0.5')
            plt.ion()
            plt.draw()

    def plot_surf (self, ax, plot_normals = False):
        for face in self.faces:
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
                    self.plot_normal (vertex, normal, ax)

            ax.plot(xs,ys,zs,color='gray',linewidth='0.5')
            plt.ion()
            plt.draw()

    def plot_normal (self, vertex, normal, ax, scale=0.3):
        p1 = vertex
        p2 = list(np.array(vertex) + np.array(normal)* scale)
        xs = [p1[0], p2[0]]
        ys = [p1[1], p2[1]]
        zs = [p1[2], p2[2]]

        ax.plot(xs,ys,zs,color='red',linewidth='1.0')

        plt.ion()
        plt.draw()


if __name__ == "__main__":
    surf = Surface('../input/half_sphere_out.obj')
    input = Drawing('../input/grid_fix.txt')

    # plotting
    fig = plt.figure(figsize=plt.figaspect(2.))

    # 2d uv space
    ax = fig.add_subplot(1, 2, 1)
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.grid(False)
    # surf.plot_param(ax)
    input.plot_param_drawing(ax)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show(block=True)

    # 3d surface
    # ax = fig.add_subplot(1, 2, 2, projection="3d")
    # ax.set_xlabel('$X$')
    # ax.set_ylabel('$Y$')
    # ax.set_zlabel('$Z$')
    # ax.grid(False)
    # surf.plot_surf(ax, False)
    mapping(surf, input)
    # input.plot_3d_drawing(ax)

