import cairo
from handd import HDD
import random


class Ligne:
    liste = []

    def __init__(self, A, B):
        self.A = A
        self.B = B

    def est_vertical(self):
        return self.A[0] == self.B[0]

    def a_une_inter(self):
        reponse = False
        for C, D in Ligne.liste:
            if self.A[0] == self.B[0] == C[0] == D[0]:
                reponse = C[1] <= self.A[1] <= D[1] or C[1] <= self.B[1] <= D[1]
            elif self.A[1] == self.B[1] == C[1] == D[1]:
                reponse = C[0] <= self.A[0] <= D[0] or C[0] <= self.B[0] <= D[0]
            elif self.A[0] == self.B[0] and C[0] == D[0]:
                pass
            elif self.A[0] == self.B[0]:
                reponse = (self.A[1] <= C[1] <= self.B[1] or
                           self.B[1] <= C[1] <= self.A[1]) and (C[0] <= self.A[0] <= D[0] or
                                                                D[0] <= self.A[0] <= C[0])
            elif self.A[1] == self.B[1] and C[1] == D[1]:
                pass
            elif self.A[1] == self.B[1]:
                reponse = (self.A[0] <= C[0] <= self.B[0] or
                           self.B[0] <= C[0] <= self.A[0]) and (C[1] <= self.A[1] <= D[1] or
                                                                D[1] <= self.A[1] <= C[1])
            if reponse:
                break
            
        return reponse

    def trace(self, exact=False):
        Ligne.liste.append((self.A, self.B))
        if exact:
            ctx.move_to(*self.A)
            ctx.line_to(*self.B)
            ctx.stroke()
        else:
            return ctx.lline_hdd([self.A, self.B])


W = 800
H = 800
offset = 30
img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = HDD(img)
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, W, H)
ctx.fill()

ctx.set_line_width = 1
ctx.set_source_rgba(1, 1, 1, .3)

N = 1_500
while len(Ligne.liste) < N:
    if random.random() > .5:
        x1, x2 = random.randrange(W), random.randrange(W)
        y1 = y2 = random.randrange(H)
        while abs(x1 - x2) < 20 or abs(x1 - x2) > W / 3:
            x1, x2 = random.randrange(W), random.randrange(W)
    else:
        x1 = x2 = random.randrange(W)
        y1, y2 = random.randrange(H), random.randrange(H)
        while abs(y1 - y2) < 20 or abs(y1 - y2) > W / 3:
            y1, y2 = random.randrange(H), random.randrange(H)
    ligne = Ligne((x1, y1), (x2, y2))
    if not ligne.a_une_inter():
        if ligne.est_vertical():
            y1, y2 = min(y1, y2), max(y1, y2)
            while y1 >= offset and y2 < H - offset and y1 != y2 and not ligne.a_une_inter():
                y1 -= 1
                y2 += 1
                ligne = Ligne((x1, y1), (x2, y2))
        else:
            x1, x2 = min(x1, x2), max(x1, x2)
            while x1 >= offset and x2 < W - offset and x1 != x2 and not ligne.a_une_inter():
                x1 -= 1
                x2 += 1
                ligne = Ligne((x1, y1), (x2, y2))
        ligne.trace(False)
        ligne = Ligne((x1, y1), (x2, y2))
        ligne.trace(True)

img.write_to_png("test8.png")
