import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return nodes[np.argmin(dist_2)]

class Drawing:
    fileName = '../intput/grid_fix.txt'
    strokes = []
    ratio = 1.0
    target_size = 0.1 # 10cm

    def readFile (self):
        f = open(self.fileName, 'r')
        lines = f.readlines()
        line = lines[0]
        line = line.split()
        self.ratio = float(line[0])/float(line[1])
        for line in lines[1:]:
            stroke = []
            if line == "End\n":
                stroke = []
                self.strokes.append(stroke)
            else:
                line = line.split()
                x = float(line[0])* 0.5 + 0.5 # fit in uv space
                y = float(line[1])* 0.5 + 0.5 # fit in uv space
                stroke.append([x,y])
        f.close()

    def plot_param_drawing (self, surface):

        for stroke in self.strokes:

        # plt.plot(xs,ys,color='black',linewidth='0.5')
        # plt.ion()
        # plt.draw()


class Surface:
    fileName = '../input/half_sphere_out.obj'
    faces = []  # contains vertices, uvs, normals per face
    points = [] # contains vertices, uvs, normals

    def __init__(self, fileName):
        self.fileName = fileName
        self.readMesh()

    def readMesh (self):
        vertices = []
        normals = []
        uvs = []
        try:
            f = open(self.fileName, 'r')
            lines = f.readlines()
            for line in lines:
                line = line.split()
                point = {'vertex':[], 'uv':[], 'normal':[]}
                if line[0] == 'v': # vertex
                    coord = list(map(float,line[1:]))
                    vertices.append(coord)
                    point['vertex'] = coord
                elif line[0] == 'vt': # uv
                    coord = list(map(float,line[1:]))
                    uvs.append(coord)
                    point['uv'] = coord
                elif line[0] == 'vn': # vertex normal
                    coord = list(map(float,line[1:]))
                    normals.append(coord)
                    point['normal'] = coord
                elif line[0] == 'f': # face
                    face = {'vertex':[], 'uv':[], 'normal':[]}
                    line = line[1:]
                    for el in line:
                        indicies = list(map(int,el.split('/')))
                        face['vertex'].append(vertices[indicies[0]-1])
                        face['uv'].append(uvs[indicies[1]-1])
                        face['normal'].append(normals[indicies[2]-1])
                    self.faces.append(face)
                self.points.append(point)
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

            ax.plot(xs,ys,color='black',linewidth='0.5')
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

            ax.plot(xs,ys,zs,color='black',linewidth='0.5')
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

    # plotting
    fig = plt.figure(figsize=plt.figaspect(2.))
    # 3d surface
    ax = fig.add_subplot(2, 1, 1, projection="3d")
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$Z$')
    ax.grid(False)
    surf.plot_surf(ax, True)

    # 2d uv space
    ax = fig.add_subplot(2, 1, 2)
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.grid(False)
    surf.plot_param(ax)

    # plt.gca().set_aspect('equal', adjustable='box')
    plt.show(block=True)


