__author__ = "david cobac"
__copyright__ = "Copyright 2021, CC-BY-NC-SA"
__date__ = 20211225

import cairo as _cairo
import random as _random
import math as _math


class HDD:
    _liste_factorielle = [1]
    debug = False

    @classmethod
    def _fac(cls, n):
        dernier = len(cls._liste_factorielle) - 1
        if n <= dernier:
            return cls._liste_factorielle[n]
        else:
            resultat = cls._liste_factorielle[dernier]
            for k in range(n - dernier):
                resultat *= (dernier + k + 1)
                cls._liste_factorielle.append(resultat)
            return resultat

    @classmethod
    def _bezier_bernstein(cls, i, n, t):
        return round(cls._fac(n) /
                     (cls._fac(i) * cls._fac(n - i))) * t**i * (1 - t)**(n - i)

    @classmethod
    def _bezier_un_point_reel(cls, t, liste_points):
        n = len(liste_points) - 1
        x = y = 0
        for i, p in enumerate(liste_points):
            B = cls._bezier_bernstein(i, n, t)
            x += B * p[0]
            y += B * p[1]
        return (x, y)

    @classmethod
    def _bezier_points_reels(cls, liste_points, N=100):
        return [cls._bezier_un_point_reel(u / (N - 1), liste_points)
                 for u in range(N)]

    @staticmethod
    def translation(A, angle_degre, longueur):
        angle_radian = _math.radians(angle_degre)
        return (A[0] + longueur * _math.cos(angle_radian),
                A[1] + longueur * _math.sin(angle_radian))

    @staticmethod
    def rotation(M, angle_degre, centre):
        angle_radian = _math.radians(angle_degre)
        c, s = _math.cos(angle_radian), _math.sin(angle_radian)
        X = centre[0] + (M[0] - centre[0]) * c - (M[1] - centre[1]) * s
        Y = centre[1] + (M[1] - centre[1]) * c + (M[0] - centre[0]) * s
        return (X, Y)

    @classmethod
    def _compute_regular_polygon_vertices(cls, bounding_circle,
                                          n_sides, rotation):
        """
        bounding_circle : (xc, yc, r)
        rotation en degrés
        """

        centre = (bounding_circle[0], bounding_circle[1])
        depart = cls.translation(centre, 0, bounding_circle[2])
        depart = cls.rotation(depart, rotation, centre)
        XY = [depart]
        for _ in range(n_sides - 1):
            depart = cls.rotation(depart, 360 / n_sides, centre)
            XY.append(depart)
        return XY

    @staticmethod
    def _bbox(polygone):
        p = polygone[0]
        mx = Mx = p[0]
        my = My = p[1]
        for p in polygone:
            x, y = p
            if x < mx:
                mx = x
            if x > Mx:
                Mx = x
            if y < my:
                my = y
            if y > My:
                My = y
        return [(mx, my), (Mx, My)]

    @staticmethod
    def _points_regulierement_repartis(debut, fin, N=10):
        """ renvoie N+1 points (N étapes du premier au dernier)
        """

        return [(debut[0] + k * (fin[0] - debut[0]) / N,
                 debut[1] + k * (fin[1] - debut[1]) / N)
                for k in range(N + 1)]

    @staticmethod
    def _points_regulierement_repartis_cercle(centre, rayon, a_deb, a_fin):
        """
        """

        points = []
        a = a_deb
        while a <= a_fin:
            points.append((centre[0] + rayon * _math.cos(_math.radians(a)),
                           centre[1] + rayon * _math.sin(_math.radians(a))))
            a += 10
        return points

    @staticmethod
    def _distance(p1, p2):
        return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** .5

    @staticmethod
    def _est_dans_poly(x, y, poly):
        """Determine if the point is in the path.
        de https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
        Args:
        x -- x coordinate of point.
        y -- y coordinate of point.
        poly -- a list of tuples [(x, y), (x, y), ...]

        Returns:
          True if the point is in the poly
        """

        num = len(poly)
        i = 0
        j = num - 1
        c = False
        for i in range(num):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                    (x < poly[i][0] + (poly[j][0] - poly[i][0]) *
                     (y - poly[i][1]) / (poly[j][1] - poly[i][1])):
                c = not c
            j = i
        return c

    def __init__(self, cairo_surface, size=None):
        self._ctx = _cairo.Context(cairo_surface)
        self._ctx.set_line_cap(_cairo.LINE_CAP_ROUND)
        self.size = size or (cairo_surface.get_width(),
                             cairo_surface.get_height())
        self.units = (1, 1)
        self.origin = (0, self.size[1])

    @property
    def ctx(self):
        return self._ctx

    def _trace_par_couple(self, liste_de_points):
        """avec la méthode line_to de cairo
        """

        liste = zip(liste_de_points, liste_de_points[1:])
        for couple in liste:
            debut, fin = couple
            self._ctx.move_to(*debut)
            self._ctx.line_to(*fin)

    def _points_devies(self, liste_points, deviation=5):
        """ renvoie une liste de points déviés
        fonction à grandement améliorer
        """

        liste = []
        for point in liste_points:
            x, y = point
            nv_x = _random.normalvariate(x, deviation)
            nv_y = _random.normalvariate(y, deviation)
            liste.append((nv_x, nv_y))
            # if HDD.debug:
            #    self._ctx.point(liste, fill="white")
        return liste

    def regular_polygon_hdd(self, bounding_circle, n_sides, rotation=0):
        """ renvoie les sommets et une bbox
        """

        xy = self._compute_regular_polygon_vertices(bounding_circle,
                                                    n_sides, rotation)
        self.polygon_hdd(xy)
        return xy, self._bbox(xy)

    def polygon_hdd(self, xy):
        """ renvoie les sommets et une une bbox
        """

        xy += [xy[0]]
        self.line_hdd(xy)
        return xy, self._bbox(xy)

    def rectangle_hdd(self, xy):
        x0, y0 = xy[0]
        x1, y1 = xy[1]
        xy = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)] + [(x0, y0)]
        return self.polygon_hdd(xy)

    def point_hdd(self, xy):
        ecart = 5
        for point in xy:
            x, y = point
            self.line_hdd([(x - ecart, y - ecart), (x + ecart, y + ecart)])
            self.line_hdd([(x - ecart, y + ecart), (x + ecart, y - ecart)])

    def line_hdd(self, xy):
        """ xy est une liste de point
        line est une ligne brisée
        """

        # on fait les couples de lignes
        liste = zip(xy, xy[1:])
        for couple in liste:
            debut, fin = couple
            # on met 6 points de contrôle pour 100 pixels
            # avec au moins 1 !
            r = max(1, round(self._distance(debut, fin) / 100) * 6)
            # points uniformément répartis
            liste_points = self._points_regulierement_repartis(debut, fin, r)
            # points déviés des points précédents -> points de contrôle
            # déviation à revoir
            liste_points = self._points_devies(liste_points, r / 4)
            # points qu'on va tracer réellement
            reels = self._bezier_points_reels(liste_points)
            # ligne entre deux points successifs
            self._trace_par_couple(reels)
            # on trace chaque ligne pour avoir
            # possiblement un effet de superposition
            # avec la transparence (comme un feutre)
            self._ctx.stroke()

    def sector_hdd(self, xy, r, a_debut, a_fin):
        polygone = [xy]
        A = (xy[0] + r * _math.cos(_math.radians(a_debut)),
             xy[1] + r * _math.sin(_math.radians(a_debut)))
        polygone.append(A)
        polygone += self._points_regulierement_repartis_cercle(
            xy, r, a_debut, a_fin)
        polygone.append(xy)
        return self.polygon_hdd(polygone)

    def circle_hdd(self, xy, r):
        polygone = self._points_regulierement_repartis_cercle(
            xy, r, 0, 360)
        return self.polygon_hdd(polygone)

    def hatch_hdd(self, polygone, bbox, nb=10, angle=45):
        """Hachures
        angle est transformé pour apartenir à ]-90;90]
        0 et 90 étant traités comme cas particuliers
        """

        angle = -angle + 90
        angle = angle % 360 - 180
        if angle > 90:
            angle -= 180
        elif angle < -90:
            angle += 180
        elif angle == -90:
            angle = 90
        # bbox -> carre
        inf_gche = bbox[0]
        sup_droit = bbox[1]
        w, h = sup_droit[0] - inf_gche[0], sup_droit[1] - inf_gche[1]
        if w < h:
            d = (h - w) / 2
            inf_gche = (inf_gche[0] - d, inf_gche[1])
            sup_droit = (sup_droit[0] + d, sup_droit[1])
        elif h > w:
            d = (w - h) / 2
            inf_gche = (inf_gche[0], inf_gche[1] - d)
            sup_droit = (sup_droit[0], sup_droit[1] + d)
        if HDD.debug:
            self.rectangle_hdd(bbox)
            self.rectangle_hdd([inf_gche, sup_droit])
        # la droite perp. aux hachures passant par le centre
        centre = [(inf_gche[i] + sup_droit[i]) / 2 for i in range(2)]
        if angle != 0 and angle != 90:
            pente = _math.tan(_math.radians(angle))
            invpente = 1 / pente
            droite = lambda x: pente * (x - centre[0]) + centre[1]
            invdroite = lambda y: (y - centre[1] + pente * centre[0]) * invpente
            if -45 <= angle <= 45:
                debut = (inf_gche[0], droite(inf_gche[0]))
                fin = (sup_droit[0], droite(sup_droit[0]))
            else:
                debut = (invdroite(inf_gche[1]), inf_gche[1])
                fin = (invdroite(sup_droit[1]), sup_droit[1])
        elif angle == 90:
            debut = (centre[0], inf_gche[1])
            fin = (centre[0], sup_droit[1])
        elif angle == 0:
            debut = (inf_gche[0], centre[1])
            fin = (sup_droit[0], centre[1])
        if HDD.debug:
            self.line_hdd([debut, fin], color=(0, 1, 0))
        # on répartit des points sur cette droite
        liste_diag = self._points_regulierement_repartis(debut, fin, nb)
        if HDD.debug:
            self.point_hdd(liste_diag)
        #
        # on trace les perpendiculaires
        for xy in liste_diag:
            xp, yp = xy
            # les limites des hachures
            if angle != 0 and angle != 90:
                droite = lambda x: -invpente * (x - xp) + yp
                invdroite = lambda y: -pente * (y - yp) + xp
                if 0 < angle <= 45:
                    debut = (invdroite(sup_droit[1]), sup_droit[1])
                    fin = (invdroite(inf_gche[1]), inf_gche[1])
                    if debut[0] < inf_gche[0]:
                        debut = (inf_gche[0], droite(inf_gche[0]))
                        if fin[0] > sup_droit[0]:
                            fin = (sup_droit[0], droite(sup_droit[0]))
                elif 45 < angle < 90:
                    debut = (inf_gche[0], droite(inf_gche[0]))
                    fin = (sup_droit[0], droite(sup_droit[0]))
                    if debut[1] > sup_droit[1]:
                        debut = (invdroite(sup_droit[1]), sup_droit[1])
                    if fin[1] < inf_gche[1]:
                        fin = (invdroite(inf_gche[1]), inf_gche[1])
                elif -45 <= angle < 0:
                    debut = (invdroite(sup_droit[1]), sup_droit[1])
                    fin = (invdroite(inf_gche[1]), inf_gche[1])
                    if debut[0] > sup_droit[0]:
                        debut = (sup_droit[0], droite(sup_droit[0]))
                    if fin[0] < inf_gche[0]:
                        fin = (inf_gche[0], droite(inf_gche[0]))
                elif -90 < angle < -45:
                    debut = (inf_gche[0], droite(inf_gche[0]))
                    fin = (sup_droit[0], droite(sup_droit[0]))
                    if debut[1] < inf_gche[1]:
                        debut = (invdroite(inf_gche[1]), inf_gche[1])
                    if fin[1] > sup_droit[1]:
                        fin = (invdroite(sup_droit[1]), sup_droit[1])
            elif angle == 90:
                debut = (inf_gche[0], yp)
                fin = (sup_droit[0], yp)
            elif angle == 0:
                debut = (xp, inf_gche[1])
                fin = (xp, sup_droit[1])
            if HDD.debug:
                self.line_hdd([debut, fin])
            # découverte des zones
            liste_pts = self._points_regulierement_repartis(debut, fin, 2 * nb)
            zones = []
            xv, yv = liste_pts[0]
            dans_zone = self._est_dans_poly(xv, yv, polygone)
            if dans_zone:
                zones.append([])
            i_zone = 0
            for p in liste_pts:
                xv, yv = p
                if self._est_dans_poly(xv, yv, polygone):
                    if dans_zone:
                        zones[i_zone].append(p)
                    else:
                        dans_zone = True
                        if len(zones) != 0:
                            i_zone += 1
                        zones.append([])
                        zones[i_zone] = [p]
                else:
                    dans_zone = False
            # tracé des zones
            for zone in zones:
                if len(zone) > 1:
                    self.line_hdd([zone[0], zone[-1]])

    def dot_hdd(self, polygone, bbox, sep=5):
        """ polygone : liste de tuples
        bbox : [(x0, y0), (x1, y1)]
        """

        x0, y0 = bbox[0]
        x1, y1 = bbox[1]

        liste = []
        for x in range(round(x0), round(x1), sep):
            for y in range(round(y0), round(y1), sep):
                if self._est_dans_poly(x, y, polygone):
                    liste.append((x, y))
        self.point_hdd(self._points_devies(liste))

    def axes_hdd(self, xy, units=None):
        if units:
            self.units = units
        self.origin = xy
        x, y = xy
        self.line_hdd([(0, y), (self.size[0], y)])
        self.line_hdd([(x, self.size[1]), (x, 0)])

    def _calc_vers_img(self, xy):
        xc, yc = self.origin
        i, j = self.units
        x, y = xy
        X = xc + i * x
        Y = yc - j * y
        return X, Y

    def _img_vers_calc(self, xy):
        pass

    def function_hdd(self, f, xmin, xmax, nb=15):
        liste_x = [xmin + k * (xmax - xmin) / nb for k in range(nb + 1)]
        liste_y = [f(x) for x in liste_x]
        pts = [self._calc_vers_img(xy) for xy in zip(liste_x, liste_y)]
        # idée : les points sont utilisés comme points de contrôle
        # dans un bézier
        pts = self._points_devies(pts, nb)
        reels = self._bezier_points_reels(pts)
        # ligne entre deux points successifs
        self._trace_par_couple(reels)

    def data(self, fichier):
        pts = []
        with open(fichier) as fh:
            for l in fh:
                l = [float(d) for d in l.strip().split()]
                pts.append((self._calc_vers_img(l)))
        pts = self._points_devies(pts, 10)
        reels = self._bezier_points_reels(pts)
        # ligne entre deux points successifs
        self._trace_par_couple(reels)
