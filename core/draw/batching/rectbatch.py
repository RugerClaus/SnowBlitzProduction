class RectBatch:

    def __init__(self,shader):

        self.shader = shader

        self.vertices = []

        self.indices = []

    def add(self,x1,y1,x2,y2,color):

        index = len(self.vertices) // 6

        self.vertices.extend([

            x1,y1,*color,
            x2,y1,*color,
            x2,y2,*color,
            x1,y2,*color

        ])

        self.indices.extend([

            index,index + 1,index + 2,
            index,index + 2,index + 3

        ])