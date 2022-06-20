import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np
from math import sqrt

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2) # return index

def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)

# def get_neighbors(train, test_row, num_neighbors):
#     distances = list()
#     for train_row in train:
#         dist = euclidean_distance(test_row, train_row)
#         distances.append((train_row, dist))
#     distances.sort(key=lambda tup: tup[1])
#     neighbors = list()
#     for i in range(num_neighbors):
#         neighbors.append(distances[i][0])
#     return neighbors

def get_neighbors (nodes, node, num_neighbors):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist = np.einsum('ij,ij->i', deltas, deltas)
    distances = list()
    for (i,el) in enumerate(dist):
        distances.append((nodes[i],el,i))
    distances.sort(key=lambda tup:tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append((distances[i][0],distances[i][2]))
    return neighbors

def find_quad (list, point):
    quad = [0,0,0,0]
    for candidate in list:
        index = candidate[1]
        candidate = candidate[0]
        # LEFT BOTTOM 0
        if candidate[0] >= point[0] and candidate[1] >= point[1]:
            if quad[0] is 0: quad[0] = (candidate,index)
        # RIGHT BOTTOM 1
        elif candidate[0] < point[0] and candidate[1] >= point[1]:
            if quad[1] is 0: quad[1] = (candidate,index)
        # RIGHT TOP 2
        elif candidate[0] < point[0] and candidate[1] < point[1]:
            if quad[2] is 0: quad[2] = (candidate,index)
        # LEFT TOP 3
        elif candidate[0] >= point[0] and candidate[1] < point[1]:
            if quad[3] is 0: quad[3] = (candidate,index)
    return quad

def find_triangle (surface, point):
    for face in surface.faces:
        a = np.array(face['uv'][0])
        b = np.array(face['uv'][1])
        c = np.array(face['uv'][2])
        p = np.array(point)
        if np.cross(a-p, b-p) >= 0:
            if np.cross(b-p, c-p) >= 0 and np.cross(c-p, a-p) >= 0:
                return face
        elif np.cross(a-p, b-p) <= 0:
            if np.cross(b-p, c-p) <= 0 and np.cross(c-p, a-p) <= 0:
                return face
    return -1

def conformal_mapping (surface, drawing):
    f = open('../output/half_sphere_grid.txt', 'w')
    for stroke in drawing.strokes:
        for point in stroke:
            face = find_triangle(surface, point)
            v1 = face['uv'][0]
            v2 = face['uv'][1]
            v3 = face['uv'][2]

            # Barycentric coordinates method
            w_v1 = ((v2[1]-v3[1])*(point[0]-v3[0])+(v3[0]-v2[0])*(point[1]-v3[1]))/((v2[1]-v3[1])*(v1[0]-v3[0])+(v3[0]-v2[0])*(v1[1]-v3[1]))
            w_v2 = ((v3[1]-v1[1])*(point[0]-v3[0])+(v1[0]-v3[0])*(point[1]-v3[1]))/((v2[1]-v3[1])*(v1[0]-v3[0])+(v3[0]-v2[0])*(v1[1]-v3[1]))
            w_v3 = 1-w_v1-w_v2

            v1_3d = np.array(face['vertex'][0])
            v2_3d = np.array(face['vertex'][1])
            v3_3d = np.array(face['vertex'][2])
            vertex = v1_3d*w_v1 + v2_3d*w_v2 + v3_3d*w_v3

            n1 = np.array(face['normal'][0])
            n2 = np.array(face['normal'][1])
            n3 = np.array(face['normal'][2])
            normal = n1*w_v1 + n2*w_v2 + n3*w_v3

            f.write(str(vertex[0])+" "+str(vertex[1])+" "+str(vertex[2])+" "+str(normal[0])+" "+str(normal[1])+" "+str(normal[2])+"\n")
        f.write('End\n')
    f.close()

'''
def conformal_mapping (surface, drawing, ax1, ax2):
    f = open('../output/half_sphere_grid.txt', 'w')
    plot = True
    for stroke in drawing.strokes:
        for point in stroke:
            # find closest first
            index = closest_node(surface.uvs, point)
            vertex = surface.vertices[index]
            normal = surface.normals[index]
            if euclidean_distance(surface.uvs[index], point) < 0.001:
                x = vertex[0]; y = vertex[1]; z = vertex[2]
                n = normal
                # print ('hey')
            else:   # find quad
                list_10 = get_neighbors(surface.uvs, point, 10)
                quad_uv_ = find_quad(list_10, point)
                if 0 in quad_uv_:
                    list_20 = get_neighbors(surface.uvs, point, 30)
                    quad_uv_ = find_quad(list_20, point)
                    if 0 in quad_uv_:
                        list_100 = get_neighbors(surface.uvs, point, 10000)
                        quad_uv_ = find_quad(list_100, point)
                        # print(list_100, point)
                        # print(quad_uv_)
                # print(list_10, point)
                # print(surface.uvs[closest_node(surface.uvs, point)])
                quad_uv = []; quad_vert = []; quad_normal = []
                for el in quad_uv_:
                    index = el[1]
                    quad_uv.append(el[0])
                    quad_vert.append(surface.vertices[index])
                    quad_normal.append(surface.normals[index])

                if plot:
                    xs = np.array(quad_vert).T[0]
                    ys = np.array(quad_vert).T[1]
                    zs = np.array(quad_vert).T[2]
                    ax2.scatter(xs, ys, zs, color='red')

                    xs = np.array(quad_uv).T[0]
                    ys = np.array(quad_uv).T[1]
                    ax1.scatter(xs, ys, color='red')
                    ax1.scatter([point[0]], [point[1]], color='blue')


                dx = quad_uv[1][0] - point[0]
                dy = quad_uv[2][1] - point[1]
                A = (1-dx)*(1-dy)
                B = dx*(1-dy)
                C = dx*dy
                D = (1-dx)*dy

                # X value
                fx1 = (quad_uv[1][0]-point[0])*quad_vert[0][0] + (point[0]-quad_uv[0][0])*quad_vert[1][0]
                fx1 = fx1/(quad_uv[1][0]-quad_uv[0][0])
                fx2 = (quad_uv[1][0]-point[0])*quad_vert[3][0] + (point[0]-quad_uv[0][0])*quad_vert[2][0]
                fx2 = fx2/(quad_uv[1][0]-quad_uv[0][0])

                x = (quad_uv[3][1]-point[1])*fx1 + (point[1]-quad_uv[0][1])*fx2
                x = x/(quad_uv[3][1]-quad_uv[0][1])

                # Y value
                fy1 = (quad_uv[1][0]-point[0])*quad_vert[0][1] + (point[0]-quad_uv[0][0])*quad_vert[1][1]
                fy1 = fy1/(quad_uv[1][0]-quad_uv[0][0])
                fy2 = (quad_uv[1][0]-point[0])*quad_vert[3][1] + (point[0]-quad_uv[0][0])*quad_vert[2][1]
                fy2 = fy2/(quad_uv[1][0]-quad_uv[0][1])

                y = (quad_uv[3][1]-point[1])*fy1 + (point[1]-quad_uv[0][1])*fy2
                y = y/(quad_uv[3][1]-quad_uv[0][1])

                # Z value
                fz1 = (quad_uv[1][0]-point[0])*quad_vert[0][2] + (point[0]-quad_uv[0][0])*quad_vert[1][2]
                fz1 = fz1/(quad_uv[1][0]-quad_uv[0][0])
                fz2 = (quad_uv[1][0]-point[0])*quad_vert[3][2] + (point[0]-quad_uv[0][0])*quad_vert[2][2]
                fz2 = fz2/(quad_uv[1][0]-quad_uv[0][1])

                z = (quad_uv[3][1]-point[1])*fz1 + (point[1]-quad_uv[0][1])*fz2
                z = z/(quad_uv[3][1]-quad_uv[0][1])

                if plot:
                    ax2.scatter([x], [y], [z], color='blue')
                    plot = False

                # print(point, quad_uv)
                n = []
                for i in range(3):
                    n.append(A*quad_normal[0][i]+B*quad_normal[1][i]+C*quad_normal[2][i]+D*quad_normal[3][i])

            f.write(str(x)+" "+str(y)+" "+str(z)+" "+str(n[0])+" "+str(n[1])+" "+str(n[2])+"\n")
        f.write('End\n')
    f.close()
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
            ax.plot(xs,ys,color='black',linewidth='1.0')
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
            ax.plot(xs,ys,zs,color='black',linewidth='1.0')
        print ('plot done')

class Surface:
    fileName = '../input/half_sphere_simple_out.obj'
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


    # def plot_param (self, ax):
    #     for face in self.faces:
    #         # face['vertex'].append(face['vertex'][0])
    #         face['uv'].append(face['uv'][0])
    #         face['normal'].append(face['normal'][0])
    #         xs = []; ys =[]
    #         for i in range(len(face['vertex'])):
    #             # vertex = face['vertex'][i]
    #             vertex = face['uv'][i]
    #             normal = face['normal'][i]
    #             xs.append(vertex[0])
    #             ys.append(vertex[1])
    #             # if plot_normals:
    #             #     plot_normal (vertex, normal, ax)
    #
    #         ax.plot(xs,ys,color='gray',linewidth='0.5')
    #         plt.ion()
    #         plt.draw()

    def plot_param (self, ax, plot_normals = False):
        for face in self.faces:
            face['uv'].append(face['uv'][0])
            xs = []; ys =[]
            for i in range(len(face['uv'])):
                vertex = face['uv'][i]
                xs.append(vertex[0])
                ys.append(vertex[1])
            ax.plot(xs,ys,color='gray',linewidth='0.3')
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

            ax.plot(xs,ys,zs,color='gray',linewidth='0.3')
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
    surf = Surface('../input/half_sphere_simple_out.obj')
    input = Drawing('../input/grid_fix.txt')

    # plotting
    fig = plt.figure(figsize=plt.figaspect(0.5))

    # 2d uv space
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_xlabel('$X$')
    ax1.set_ylabel('$Y$')
    ax1.grid(False)
    surf.plot_param(ax1)
    input.plot_param_drawing(ax1)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show(block=False)

    # 3d surface
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.set_xlabel('$X$')
    ax2.set_ylabel('$Y$')
    ax2.set_zlabel('$Z$')
    ax2.grid(False)
    surf.plot_surf(ax2, False)
    conformal_mapping(surf, input)
    input.plot_3d_drawing(ax2)

    # ax.plot([surf.vertices[0][0]],[surf.vertices[0][1]], [surf.vertices[0][2]], color='red', linewidth='1.0')
    # surf.plot_normal(surf.vertices[0], surf.normals[0], ax)

    plt.show(block=False)
    plt.savefig('result.pdf')
    plt.savefig('result.png')




