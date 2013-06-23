from bottle import route, run, template, static_file, request
import proj

@route('/')
def index():
    return static_file('index.html', root='.')

@route('/tools/distance')
def distance():
    a = tuple(map(float, request.query.a.split(',')))
    b = tuple(map(float, request.query.b.split(',')))
    return str(proj.distance(a,b))

@route('/static/<filename:path>')
def static(filename):
    print filename
    return static_file(filename, root='static')

run(host='localhost', port=8080)