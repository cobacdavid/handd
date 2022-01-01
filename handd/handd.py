__author__ = "david cobac"
__copyright__ = "Copyright 2021, CC-BY-NC-SA"
__date__ = 20211225

import cairo as _cairo
import random as _random
import math as _math


class HDD(_cairo.Context):
    _liste_factorielle = [1]
    debug = False
    debug_color = (1, 1, 1)
    deviation = 3

    @classmethod
    def _fac(cls, n):
        """méthode privée permettant le calcul des factoriels

        :param n: rang du terme cherché
        :type n: int
        :rtype: int
        """

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
        """calcul du coefficient de Bernstein pour les Bézier

        :param i: entier entre 0 et n
        :type i: int
        :param n: degré du polynôme
        :type n: int
        :param t: réel dans [0, 1]
        :type t: float
        :rtype: float
        """

        return round(cls._fac(n) / (cls._fac(i) * cls._fac(n - i))) *\
            t**i * (1 - t)**(n - i)

    @classmethod
    def _bezier_un_point_reel(cls, t, xy):
        """renvoie une position issue d'un calcul avec le polynôme
        de Bernstein

        :param t:  réel dans [0, 1]
        :type t: float
        :param xy: liste des points (de contrôle et/ou de la courbe)
        :type xy: list(tuple)
        :rtype: tuple(float)
        """

        n = len(xy) - 1
        x = y = 0
        for i, p in enumerate(xy):
            B = cls._bezier_bernstein(i, n, t)
            x += B * p[0]
            y += B * p[1]
        return (x, y)

    @classmethod
    def _bezier_points_reels(cls, xy, N=100):
        """renvoie la liste des points à tracer à partir de la liste
        des points calculés

        :param xy: liste des points (de contrôle et/ou de la courbe)
        :type xy: list(tuple)
        :rtype: list(tuple)
        """

        return [cls._bezier_un_point_reel(u / (N - 1), xy)
                 for u in range(N)]

    @classmethod
    def is_in(cls, x, y, path):
        """Renseigne sur l'appartenance d'un point à l'intérieur du chemin
        :param x: colonne
        :type x: float or int
        :param y: ligne
        :type y: float or int
        :rtype: boolean
        """

        return cls._est_dans_poly(x, y, path)

    @staticmethod
    def translation(M, angle, dist):
        """Renvoie les coordonnées de l'image de M
        par une translation

        :param M: point à translater
        :type M: tuple
        :param angle: angle en radian (vecteur orienté)
        :type angle: float
        :param dist: norme du vecteur
        :type dist: float
        :rtype: tuple(float)
        """

        return (M[0] + dist * _math.cos(angle),
                M[1] + dist * _math.sin(angle))

    @staticmethod
    def rotation(M, angle, center):
        """Renvoie les coordonnées de l'image de M
        par une rotation

        :param M: point à transformer
        :type M: tuple
        :param angle: angle en radian (vecteur orienté)
        :type angle: float
        :param center: centre de rotation
        :type center: tuple
        :rtype: tuple(float)
        """

        c, s = _math.cos(angle), _math.sin(angle)
        X = center[0] + (M[0] - center[0]) * c - (M[1] - center[1]) * s
        Y = center[1] + (M[1] - center[1]) * c + (M[0] - center[0]) * s
        return (X, Y)

    @classmethod
    def _compute_regular_polygon_vertices(cls, bounding_circle,
                                          n_sides, angle):
        """Renvoie les cordonnées des sommets d'un polygone régulier

        :param bounding_circle: xcentre, ycentre et rayon
        :type bounding_circle: tuple(float)
        :param n_sides: nombre de côtés du polygone
        :type n_sides: int
        :param angle: angle de "départ" en radian
        :type angle: float
        :rtype: list(tuple)
        """

        centre = (bounding_circle[0], bounding_circle[1])
        depart = cls.translation(centre, 0, bounding_circle[2])
        depart = cls.rotation(depart, angle, centre)
        XY = [depart]
        for _ in range(n_sides - 1):
            depart = cls.rotation(depart, _math.tau / n_sides, centre)
            XY.append(depart)
        return XY

    @staticmethod
    def _bbox(path):
        """Renvoie la bounding box d'un chemin

        :param path: chemin
        :type path: list(tuple)
        :rtype: list(tuple)
        """

        p = path[0]
        mx = Mx = p[0]
        my = My = p[1]
        for p in path:
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
    def _points_regulierement_repartis(start, end, N=10):
        """Renvoie N+1 points (N étapes du premier au dernier)
        pour aller de start à end

        :param start: point de départ
        :type start: tuple(float)
        :param end: point d'arrivée
        :type end: tuple(float)
        :rtype: list(tuple)

        """

        return [(start[0] + k * (end[0] - start[0]) / N,
                 start[1] + k * (end[1] - start[1]) / N)
                for k in range(N + 1)]

    @staticmethod
    def _points_regulierement_repartis_cercle(center, radius, a_start, a_end,
                                              step=.01):
        """Renvoie des points cocycliques régulièrement répartis
        allant de angle_start à angle_end

        :param center: centre du cercle
        :type center: tuple(float)
        :param radius: rayon du cercle
        :type radius: float
        :param a_start: point de départ
        :type a_start: tuple(float)
        :param a_end: point d'arrivée
        :type a_end: tuple(float)
        :param step: pas à respecter pour les angles
        :type step: float
        :rtype: list(tuple)
        """

        points = []
        a = a_start
        while a < a_end:
            points.append((center[0] + radius * _math.cos(a),
                           center[1] + radius * _math.sin(a)))
            a += step
        points.append((center[0] + radius * _math.cos(a_end),
                       center[1] + radius * _math.sin(a_end)))
        return points

    @staticmethod
    def _distance(p1, p2):
        """Calcule la distance entre deux points (norme 2)

        :param p1: un point
        :type p1: tuple(float)
        :param p2: un point
        :type p2: tuple(float)
        :rtype: float
        """

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
        # super().__init__(cairo_surface)
        # self._ctx = self # _cairo.Context(cairo_surface)
        self.set_line_cap(_cairo.LINE_CAP_ROUND)
        self.size = size or (cairo_surface.get_width(),
                             cairo_surface.get_height())
        self.units = (1, 1)
        self.origin = (0, self.size[1])

    def _trace_par_couple(self, xy):
        """Définit une ligne "courante" au sens cairo

        :param xy: liste des points de la ligne
        :type xy: list(tuple)
        :rtype: None
        """

        self.move_to(*xy[0])
        for couple in xy:
            self.line_to(*couple)

    def _points_devies(self, xy):
        """ renvoie une liste de points déviés
        (fonction à grandement améliorer)

        :param xy: liste des points à dévier
        :type xy: list(tuple)
        :rtype: list(tuple)
        """

        liste = []
        for point in xy:
            x, y = point
            nv_x = _random.normalvariate(x, HDD.deviation)
            nv_y = _random.normalvariate(y, HDD.deviation)
            liste.append((nv_x, nv_y))
            if HDD.debug:
                self.save()
                self.set_source_rgb(*HDD.debug_color)
                self.set_line_width(1)
                self.lround_point_hdd(liste)
                self.stroke()
                self.restore()
        return liste

    def lline_hdd(self, xy):
        """Trace une ligne définit par la liste des points

        :param xy: liste des points à relier
        :type xy: list(tuple)
        :rtype: None

        .. note:: méthode centrale dans HDD

        .. note:: faut-il lancer stroke() à la fin ? si on ne le
                  fait pas, on a un unique tracé au prochain
                  stroke() donc pas d'effet de transparence dans
                  les hachres (par exemple)
        """

        # on fait les couples de lignes
        liste = zip(xy, xy[1:])
        for couple in liste:
            debut, fin = couple
            # on met 6 points de contrôle pour 100 pixels
            # avec au moins 1 !
            r = max(1, round(self._distance(debut, fin) / 100 * 6))
            # points uniformément répartis
            liste_points = self._points_regulierement_repartis(debut, fin, r)
            # points déviés des points précédents -> points de contrôle
            liste_points = self._points_devies(liste_points)
            # points qu'on va tracer réellement
            reels = self._bezier_points_reels(liste_points)
            # ligne entre deux points successifs
            self._trace_par_couple(reels)
            # on trace chaque ligne pour avoir
            # possiblement un effet de superposition
            # avec la transparence (comme un feutre)
            self.stroke()

    def lpolygon_hdd(self, xy):
        """Trace un polygone définit par une liste de points

        :param xy: liste des points du polygone
        :type xy: list(tuple)
        :rtype: tuple(list)
        """

        xy += [xy[0]]
        self.lline_hdd(xy)
        return xy, self._bbox(xy)

    def lpoint_hdd(self, xy, radius=5):
        """Trace une croix aux coordonnées spécifiées par la liste

        :param xy: liste des points
        :type xy: list(tuple)
        :rtype: None
        """

        for point in xy:
            x, y = point
            self.lline_hdd([(x - radius, y - radius),
                            (x + radius, y + radius)])
            self.lline_hdd([(x - radius, y + radius),
                            (x + radius, y - radius)])

    def lround_point_hdd(self, xy):
        """Trace un cercle aux coordonnées spécifiées par la liste
        Pas de tracé à la main dans cette méthode

        :param xy: liste des points
        :type xy: list(tuple)
        :rtype: None
        """

        for coords in xy:
            self.arc(coords[0], coords[1], 2, 0, _math.tau)

    def rectangle_hdd(self, x, y, w, h):
        """Trace un rectangle

        :param x: colonne sup gche
        :type x: float
        :param y: ligne sup gche
        :type y: float
        :param w: largeur
        :type w: float
        :param h: hauteur
        :type h: float
        :rtype: tuple(list)
        """

        x1, y1 = x + w, y + h
        xy = [(x, y), (x1, y), (x1, y1), (x, y1)]
        return self.lpolygon_hdd(xy)

    def regular_polygon_hdd(self, x, y, radius, n_sides, angle=0):
        """Trace un polygone régulier

        :param x: absc. centre du cercle
        :type x: float
        :param y: ord. centre du cercle
        :type y: float
        :param radius: rayon du cercle
        :type radius: float
        :param n_sides: nombre de côtés du polygone
        :type n_sides: int
        :param angle: angle de "départ" en radian
        :type angle: float
        :rtype: list(tuple)
        """

        xy = self._compute_regular_polygon_vertices((x, y, radius),
                                                    n_sides, angle)
        self.lpolygon_hdd(xy)
        return xy, self._bbox(xy)

    def disc_hdd(self, x, y, radius, a_start, a_end=None):
        """Définit un chemin "courant" au sens cairo en forme de disque ou
        de partie de disque

        :param x: absc. centre du cercle
        :type x: float
        :param y: ord. centre du cercle
        :type y: float
        :param radius: rayon du cercle
        :type radius: float
        :param a_start: point de départ
        :type a_start: tuple(float)
        :param a_end: point d'arrivée
        :type a_end: tuple(float)
        :rtype: list(tuple)
        """

        if not a_end:
            a_end = a_start + _math.tau
        polygone = self._points_regulierement_repartis_cercle(
            (x, y), radius, a_start, a_end)
        xy = self._points_devies(polygone)
        reels = self._bezier_points_reels(xy)
        self._trace_par_couple(reels)
        return reels, self._bbox(reels)

    def sector_hdd(self, x, y, radius, a_start, a_end, dev=3):
        """Trace un chemin "courant" au sens cairo en forme de secteur
        angulaire

        :param x: absc. centre du cercle
        :type x: float
        :param y: ord. centre du cercle
        :type y: float
        :param radius: rayon du cercle
        :type radius: float
        :param a_start: point de départ
        :type a_start: tuple(float)
        :param a_end: point d'arrivée
        :type a_end: tuple(float)
        :param dev: écrat-type
        :type dev: float
        :rtype: list(tuple)

        """
        save_dev = HDD.deviation
        HDD.deviation = dev
        polygone = []
        polygone = self._points_regulierement_repartis_cercle(
            (x, y), radius, a_start, a_end)
        xy = self._points_devies(polygone)
        reels = self._bezier_points_reels(xy)
        self._trace_par_couple(reels)
        HDD.deviation = save_dev
        self.lline_hdd([(x, y), reels[0]])
        self.lline_hdd([(x, y), reels[-1]])
        return [(x, y)] + reels + [(x, y)], self._bbox(reels)
        # en-dessous solution essayée mais non retenue
        # pts = self._points_devies(polygone, 10)
        # reels = self._bezier_points_reels(pts)
        # self._trace_par_couple(reels)
        # return reels, self._bbox(reels)

    def real_circle_hdd(self, x, y, radius, step=.005):
        """Trace un cercle cairo véritable

        :param x: absc. centre du cercle
        :type x: float
        :param y: ord. centre du cercle
        :type y: float
        :param radius: rayon du cercle
        :type radius: float
        :param step: pas à respecter pour les angles
        :type step: float
        :rtype: list(tuple)
        """

        A = (x + radius, y)
        polygone = self._points_regulierement_repartis_cercle(
            (x, y), radius, 0, _math.tau, step=step)
        polygone.append(A)
        bbox = [(x - radius, y - radius), (x + radius, y + radius)]
        self.arc(x, y, radius, 0, _math.tau)
        return polygone, bbox

    def circle_hdd(self, x, y, radius, dev=3, step=.01):
        """Trace un cercle

        :param x: absc. centre du cercle
        :type x: float
        :param y: ord. centre du cercle
        :type y: float
        :param radius: rayon du cercle
        :type radius: float
        :param dev: écrat-type
        :type dev: float
        :param step: pas à respecter pour les angles
        :type step: float
        :rtype: list(tuple)
        """

        save_dev = HDD.deviation
        HDD.deviation = dev
        debut = _random.random() * _math.tau
        fin = debut + _math.tau
        polygone = self._points_regulierement_repartis_cercle(
            (x, y), radius, debut, fin, step=step)
        xy = self._points_devies(polygone)
        reels = self._bezier_points_reels(xy)
        self._trace_par_couple(reels)
        HDD.deviation = save_dev
        return polygone, self._bbox(polygone)

    def hatch_hdd(self, path, bbox, n=10, angle=_math.pi / 4,
                  condition=lambda x, y: True):
        """Hachure la zone définie par le chemin (fermé)

        :param path: chemin
        :type path: list(tuple)
        :param bbox: bounding box du chemin
        :type bbox: list(tuple)
        :param n: densité de hachures
        :type n: int
        :param angle: angle des hachures
        :type angle: float
        :rtype: None
        """

        # angle est transformé pour appartenir à ]-90;90]
        # 0 et 90 étant traités comme cas particuliers
        angle = _math.degrees(angle)
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
        elif h < w:
            d = (w - h) / 2
            inf_gche = (inf_gche[0], inf_gche[1] - d)
            sup_droit = (sup_droit[0], sup_droit[1] + d)
        if HDD.debug:
            self.save()
            self.set_source_rgb(*HDD.debug_color)
            self.set_line_width(1)
            self.rectangle_hdd(bbox[0][0], bbox[0][1], w, h)
            self.rectangle_hdd(inf_gche[0],
                               inf_gche[1],
                               sup_droit[0] - inf_gche[0],
                               sup_droit[1] - inf_gche[1])
            self.stroke()
            self.restore()
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
            self.save()
            self.set_source_rgb(*HDD.debug_color)
            self.set_line_width(1)
            self.lline_hdd([debut, fin])
            self.stroke()
            self.restore()
        # on répartit des points sur cette droite
        liste_diag = self._points_regulierement_repartis(debut, fin, n)
        if HDD.debug:
            self.save()
            self.set_source_rgb(*HDD.debug_color)
            self.set_line_width(1)
            self.lround_point_hdd(liste_diag)
            self.stroke()
            self.restore()
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
                self.save()
                self.set_source_rgb(*HDD.debug_color)
                self.set_line_width(1)
                try:
                    self.lline_hdd([debut, fin])
                except:
                    pass
                self.stroke()
                self.restore()
            # découverte des zones
            liste_pts = self._points_regulierement_repartis(debut, fin, 10 * n)
            zones = []
            xv, yv = liste_pts[0]
            dans_zone = self._est_dans_poly(xv, yv, path) and condition(xv, yv)
            if dans_zone:
                zones.append([])
            i_zone = 0
            for p in liste_pts:
                xv, yv = p
                if self._est_dans_poly(xv, yv, path) and condition(xv, yv):
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
                    self.lline_hdd([zone[0], zone[-1]])

    def dot_hdd(self, path, bbox, sep=5):
        """Remplit de points la zone définit pas path

        :param path: chemin
        :type path: list(tuple)
        :param bbox: bounding box du chemin
        :type bbox: list(tuple)
        :rtype: None
        """

        x0, y0 = bbox[0]
        x1, y1 = bbox[1]

        liste = []
        for x in range(round(x0), round(x1), sep):
            for y in range(round(y0), round(y1), sep):
                if self._est_dans_poly(x, y, path):
                    liste.append((x, y))
        self.lpoint_hdd(self._points_devies(liste))

    def axes_hdd(self, x, y, units=None):
        """Trace des axes orientés usuellement et centrés sur (x, y)

        :param x: absc. origine
        :type x: float
        :param y: ord. origine
        :type y: float
        :param units: unités utilisés en pixels
        :type units: tuple(float)
        :rtype: None
        """

        if units:
            self.units = units
        self.origin = (x, y)
        self.lline_hdd([(0, y), (self.size[0], y)])
        self.lline_hdd([(x, self.size[1]), (x, 0)])

    def _calc_vers_img(self, x, y):
        """Convertit image par la fonction en positionnement sur le canevas
        cairo

        :param x: absc d'un point
        :type x: float
        :param y: ord d'un point
        :type y: float
        :rtype: tuple
        """

        xc, yc = self.origin
        i, j = self.units
        X = xc + i * x
        Y = yc - j * y
        return X, Y

    def _img_vers_calc(self, xy):
        pass

    def function_hdd(self, f, xmin, xmax, n=15):
        """Définit un chemin "courbe représentative de f"

        :param f: une expression algébrique de fonction
        :type f: function
        :param xmin: x minimum
        :type xmin: float
        :param xmax: x maximum
        :type xmax: float
        :param n: nb de points (précision)
        :type n: int
        :rtype: None
        """

        liste_x = [xmin + k * (xmax - xmin) / n for k in range(n + 1)]
        liste_y = [f(x) for x in liste_x]
        pts = [self._calc_vers_img(x, y) for x, y in zip(liste_x, liste_y)]
        # idée : les points sont utilisés comme points de contrôle
        # dans un bézier
        pts = self._points_devies(pts)
        reels = self._bezier_points_reels(pts)
        # ligne entre deux points successifs
        self._trace_par_couple(reels)

    def data_hdd(self, a_file):
        """Définit un chemin de point en point en suivant les data
        de type :
        120 300
        50 76
        54 78
        ...

        :param a_file: fichier à traiter
        :type a_file: str
        """

        pts = []
        with open(a_file) as fh:
            for l in fh:
                l = [float(d) for d in l.strip().split()]
                pts.append((self._calc_vers_img(l)))
        pts = self._points_devies(pts)
        reels = self._bezier_points_reels(pts)
        # ligne entre deux points successifs
        self._trace_par_couple(reels)
