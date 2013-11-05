from gevent import monkey
monkey.patch_all()

from bottle import route, run, template, static_file, request, response
import proj
import json
import urllib2


@route('/')
def index():
    return static_file('index.html', root='.')

@route('/tools/distance')
def distance():
    a = tuple(map(float, request.query.a.split(',')))
    b = tuple(map(float, request.query.b.split(',')))
    return str(proj.distance(a,b))

@route('/tools/polyconvert')
def distance():
    dst = tuple(map(float, request.query.dst.split(',')))
    pts_coords = map(float, request.query.pts.split(','))
    result = proj.convert_points([tuple(pts_coords[i*2:i*2+2]) for i in range(len(pts_coords)/2)], dst)
    response.content_type = 'application/json'
    return json.dumps([{'lng' : x, 'lat': y} for x,y in result])

@route('/craigslist/<area>')
def craigslist(area):
    params = {
    'area' : area,
    'flavor' : request.query.get('flavor', 'sfbay'),
    'min_ask' : request.query.get('min_ask', ''),
    'max_ask' : request.query.get('max_ask', ''),
    'bedrooms' : request.query.get('bedrooms', '')
    }

    url = 'http://%(flavor)s.craigslist.org/jsonsearch/apa/%(area)s?useMap=1&zoomToPosting=&query=&srchType=A&minAsk=%(min_ask)s&maxAsk=%(max_ask)s&bedrooms=%(bedrooms)s' % params
    response.content_type = 'application/json'
    return urllib2.urlopen(url).read()

@route('/static/<filename:path>')
def static(filename):
    print filename
    return static_file(filename, root='static')

run(host='localhost', port=8080, server='gevent')
