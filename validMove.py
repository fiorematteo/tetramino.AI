class validMove:
    def __init__(self, x, y, nRotation, piece, pieces,holesFactor,linesFactor,heightFactor):
        self.x = x
        self.y = y
        self.nRotation = nRotation
        self.piece = piece
        self.pieces = pieces
        self.score = self.score(holesFactor,linesFactor,heightFactor)
    @staticmethod
    def normalize(min, max, value):
        return value-min/max-min
    def score(self,holesFactor,linesFactor,heightFactor):
        nHoles = 4

        flag = False

        for tetra in self.piece.tetras:
            for piece in self.pieces:
                if tetra.x == piece.x and tetra.y == piece.y - piece.height:
                    nHoles -= 1
                    break
            for k in self.piece.tetras:
                if tetra.x == k.x and tetra.y == k.y - k.height:
                    nHoles -= 1
                    break
            if tetra.y + tetra.height == 1025:
                nHoles -= 1
                break

        grid = []
        rows = []
        linesCleared = 0

        for piece in self.pieces:
            grid.append(piece.y)
        
        for tetra in self.piece.tetras: 
            grid.append(tetra.y)

        Y = 25
        while Y <= 1050:
            rows.append([Y, 0])
            Y += 50

        for item in grid:
            for row in rows:
                if item == row[0]:
                    row[1] += 1
        
        for row in rows:
            if row[1] == 10:
                linesCleared = 1

        maxY = -10
        for tetra in self.piece.tetras:
            maxY = tetra.y if tetra.y > maxY else maxY
        maxY = self.normalize(0,1025,maxY)
        nHoles = self.normalize(0,3,nHoles)
        linesCleared = self.normalize(0,4,linesCleared)
        return (maxY*heightFactor) + (linesCleared*linesFactor) - (nHoles*holesFactor)
