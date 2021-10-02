import matplotlib.pylab as plt
import mpl_toolkits.mplot3d as a3
import numpy as np


class Stroke :
    xs = []
    ys = []

    def __init__ (self):
        self.xs = []
        self.ys = []

    def append (self, coord):
        self.xs.append(coord[0])
        self.ys.append(coord[1])

    def getPoint (self, index):
        return np.array([self.xs[index], self.ys[index]])

    def getSize (self):
        return len(self.xs)

class Drawing:
    path = '../input/ewha/'
    file_name = 'ewha_color_path_'
    color = 'c'
    file_extension = '.txt'
    file_name_full = path+file_name+color+file_extension

    size = [0.5, 0.5] # width, height
    target_size = 0.6 # target height
    ratio = size[0]/ size[1] # width / height
    max_range = 0.35 # splitting range
    ranges = []

    # drawing
    strokes = []
    strokes_by_range = []

    def readDrawing (self):
        self.setFileName()
        stroke = Stroke()

        try:
            f = open(self.file_name_full, 'r')
            lines = f.readlines()

            # read the first line and set ratio
            self.size = list(map(float,lines[0].split()))
            self.setRatio()
            self.setTargetSize()
            lines = lines[1:]
            self.strokes = []

            # read lines and save strokes
            for line in lines:
                if line != 'End\n':
                    coord = list(map(float,line.split()))
                    stroke.append(self.getResizedCoord(coord))
                elif line == 'End\n':
                    self.strokes.append(stroke)
                    stroke = Stroke()
                if not line:
                    break
        except:
            print("Error opening the file")

    def setRatio (self):
        self.ratio = self.size[0]/ self.size[1]

    def setTargetSize (self):
        width = self.ratio * self.target_size
        height = self.target_size
        self.size = [width, height]

    def setFileName (self):
        self.file_name_full = self.path+self.file_name+self.color+self.file_extension

    # calculate coord by target size
    def getResizedCoord (self, coord):
        x = (coord[0] - 0.5) * self.ratio * self.target_size
        y = (-coord[1] + 0.5) * self.target_size
        return [x, y]

    # remove the long distanced line
    def splitLongDist (self):
        new_strokes = []
        for stroke_ in self.strokes:
            stroke = Stroke()
            coord_prev = stroke_.getPoint(0)
            stroke.append(coord_prev)
            for i in np.arange(1,stroke_.getSize()):
                coord = stroke_.getPoint(i)
                dist = np.linalg.norm(coord - coord_prev)
                if dist > 0.025: ## 3cm
                    if len(stroke.xs) > 2:
                        new_strokes.append(stroke)
                    stroke = Stroke()
                    stroke.append(coord)
                else:
                    stroke.append(coord)
                coord_prev = coord
            new_strokes.append(stroke)
        self.strokes = new_strokes

    # set the canvas range
    def setCanvasRange (self):
        width = self.size[0]
        range_num = int(width/self.max_range)+1
        r = np.arange(-self.max_range*range_num/2, self.max_range*range_num/2, self.max_range)
        # r = np.arange(-width/2, width/2, self.max_range)
        self.ranges = []
        bot = r[0]
        for val in r[1:]:
            self.ranges.append([bot, val])
            bot = val
        self.ranges.append([bot, width/2])

    # split drawings by range
    def splitByRange (self):
        self.setCanvasRange()
        strokes_by_range = []
        indices = []

        for stroke_ in self.strokes:
            stroke = Stroke()
            stroke.append(stroke_.getPoint(0))   # first drawing point
            range_index = self.detectRange(stroke_.xs[0])

            for p in np.arange(1, stroke_.getSize()):
                coord = stroke_.getPoint(p)
                i = self.detectRange(coord[0])
                if range_index != i: # split the stroke
                    contact = list(set(self.ranges[range_index])-(set(self.ranges[range_index])-set(self.ranges[i])))[0]
                    stroke.append([contact, coord[1]])
                    if len(stroke.xs) > 2:
                        if range_index not in indices:
                            indices.append(range_index)
                            strokes_by_range.append([stroke])
                        else:
                            strokes_by_range[indices.index(range_index)].append(stroke)
                    stroke = Stroke()
                    stroke.append([contact, coord[1]])
                    range_index = i
                else :
                    stroke.append(coord)

            if range_index not in indices:
                indices.append(range_index)
                strokes_by_range.append([stroke])
            else:
                strokes_by_range[indices.index(range_index)].append(stroke)
        self.strokes_by_range = strokes_by_range

    def reCenterDrawings (self):
        for i, strokes  in enumerate(self.strokes_by_range):
            diff = (self.ranges[i][1] + self.ranges[i][0])/2
            for stroke in strokes:
                stroke.xs = list(np.array(stroke.xs) - diff)

    def detectRange (self, val):
        for i, r in enumerate(self.ranges):
            if r[0] < val < r[1]:
                return i
        return -1


def plot_strokes (strokes, ax, c_='c', dimension='2d'):
    colors = ['c','m','y']
    for i, stroke in enumerate(strokes):
        if c_ == 0: c = colors[i%len(colors)]
        else: c = c_
        if dimension == '2d':
            ax.plot(stroke.xs, stroke.ys, color=c, linewidth='0.5')
        else:
            ax.plot(np.zeros(stroke.getSize()), stroke.xs,stroke.ys, color=c, linewidth='0.5')
        plt.ion()
        plt.draw()

def plot_auto_scale (strokes, ax, dimension='2d'):
    min_ = []
    max_ = []
    for stroke in strokes:
        min_.append(np.array(stroke.xs).min())
        min_.append(np.array(stroke.ys).min())
        max_.append(np.array(stroke.xs).max())
        max_.append(np.array(stroke.ys).max())

    # min = np.array(min_).min()
    max = np.array(max_).max()
    max = max*1.05

    if dimension == '2d':
        ax.set_xlim(-max, max)
        ax.set_ylim(-max, max)
    else:
        ax.auto_scale_xyz([-1.0, 1.0], [-max, max], [-max, max])

if __name__ == "__main__":
    draw = Drawing()

    draw.path = '../input/ewha/'
    draw.file_name = 'ewha_color_path_'
    # draw.path = '../input/university/'
    # draw.file_name = 'university_color_path_'
    draw.color = 'c'

    draw.readDrawing()

    # plotting
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection="3d")
    ax = fig.add_subplot()
    ax.grid(False)

    plot_strokes(draw.strokes, ax, draw.color)

    plot_auto_scale(draw.strokes, ax)
    plt.show(block=False)

    ###################################### split long distance
    draw.splitLongDist()

    # plotting
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection="3d")
    ax = fig.add_subplot()
    ax.grid(False)

    plot_strokes(draw.strokes, ax, 0)
    strokesss = draw.strokes

    plot_auto_scale(draw.strokes, ax)
    plt.show(block=False)

    ###################################### split by range
    draw.splitByRange()
    draw.reCenterDrawings()

    # plotting
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection="3d")
    ax = fig.add_subplot()
    ax.grid(False)

    for i, strokes in enumerate(draw.strokes_by_range):
        colors = ['c','m','y','k']
        plot_strokes(strokes, ax, colors[i%len(colors)])

    plot_auto_scale(draw.strokes, ax)
    plt.show(block=False)



    # draw.color = 'm'
    # draw.readDrawing()
    # draw.splitLongDist()
    # plot_strokes(draw.strokes, ax, draw.color)
    # plt.show(block=False)
    #
    # draw.color = 'y'
    # draw.readDrawing()
    # draw.splitLongDist()
    # plot_strokes(draw.strokes, ax, draw.color)
    # plt.show(block=False)
    #
    # draw.color = 'k'
    # draw.file_name = 'ewha_outline_path_'
    # draw.readDrawing()
    # draw.splitLongDist()
    # plot_strokes(draw.strokes, ax, draw.color)
    # plt.show(block=False)
    #
    # draw.file_name = 'ewha_outline_x_path_'
    # draw.readDrawing()
    # draw.splitLongDist()
    # plot_strokes(draw.strokes, ax, draw.color)
    # plt.show(block=False)
