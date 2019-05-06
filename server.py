from count_cells import convert_image
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, post, request, static_file
import random

@route('/')
def hello_world():
    return '''
    <h1> Count the number of cells in an image </h1>
    <br>
    <form action="/count_cells" method="post" enctype="multipart/form-data">
    Image: <input type="file" name="image" value="Choose file">
    <br>
    Minimum cell side length (pixels): <input type="number" name="size" value="10">
    <br>
    <input type="submit" value="submit">
    </form>
    <br>
    <h2> Example: </h2>
    <h3> In </h3>
    <img src="/img/in/8312.jpg">
    <br>
    <h3> Out </h3>
    <img src="/img/out/8312.jpg">
    <br>
    79 cells counted
    <br>

    '''

@post('/count_cells')
def count_cells():
    side = int(request.forms.get('size'))
    image = request.files.get('image')
    name = str(int(random.random()*10000)) + '.jpg'
    image.save('/home/annav8/cell_counter/in/' + name)
    num = convert_image('in/'+name, 'out/'+name, side)
    return '<img src="/img/out/' + name + '"> <br>' + str(num) + ' cells counted'

@route('/img/<dir>/<name>')
def img(dir, name):
    return static_file(name, root='/home/annav8/cell_counter/'+dir)


application = default_app()

