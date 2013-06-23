import pyproj
import math

def utm_zone(latitude):
    return int(math.floor((latitude + 180) / 6) % 60 + 1)

def distance(a, b):
    """ Get distance in meters between two (lon,lat) WGS84 points """
    utm = pyproj.Proj("+proj=utm +zone=%d +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs" % utm_zone(a[0]))
    wgs84 = pyproj.Proj("+init=EPSG:4326")

    a_utm = pyproj.transform(wgs84, utm, *a)
    b_utm = pyproj.transform(wgs84, utm, *b)
    return math.sqrt(math.pow(a_utm[0] - b_utm[0],2) + math.pow(a_utm[1] - b_utm[1],2))


def convert_points(pts, dst):
    """ Move (translate) points to a different origin point
        Parameters:
            pts -- list of points as WGS84 (lon,lat) pairs
            ref -- new reference point, first element of pts will be moved there
        Returns:
            list of new (lat, lon) coordinates
    """
    origin = pts[0]    

    utm_from = pyproj.Proj("+proj=utm +zone=%d +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs" % utm_zone(origin[0]))
    utm_to = pyproj.Proj("+proj=utm +zone=%d +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs" % utm_zone(dst[0]))
    wgs84 = pyproj.Proj("+init=EPSG:4326")

    pts_utm_from = [pyproj.transform(wgs84, utm_from, *p) for p in pts]

    origin_utm_from = pyproj.transform(wgs84, utm_from, *origin)
    dst_utm_to = pyproj.transform(wgs84, utm_to, *dst)

    pts_utm_to = []
    for p in pts_utm_from:
        x = dst_utm_to[0] + (p[0] - origin_utm_from[0])
        y = dst_utm_to[1] + (p[1] - origin_utm_from[1])
        pts_utm_to.append((x,y))

    return [pyproj.transform(utm_to, wgs84, *p) for p in pts_utm_to]