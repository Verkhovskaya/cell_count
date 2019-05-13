from count_cells import convert_image
from bottle import default_app, route, post, request, static_file
import random

@route('/')
def hello_world():
    try:
        return static_file("landing_page.html", root="/home/annav8/cell_counter/website")
    except Exception as e:
        return str(e)

@post('/count_cells')
def count_cells():
    try:
        image = request.files.get('image')
        name = str(int(random.random()*10000)) + '.jpg'
        image.save('/home/annav8/cell_counter/in/' + name)
        num = convert_image('in/'+name, 'out/'+name)
        return '<img src="/img/out/' + name + '"> <br>' + str(num) + ' cells counted'
    except Exception as e:
        return str(e)

@route('/img/<dir>/<name>')
def img(dir, name):
    return static_file(name, root='/home/annav8/cell_counter/'+dir)

application = default_app()
