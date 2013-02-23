import os
from bottle import route, run, template

@route('/hello/:name')
def index(name='World'):
    return '<b>Hello Cem %s!</b>' % name

@route('/')
def index2():
    titles = ['isim','soyadi']
    items = [['cem','vardar'], ['hulya','hisim']]
    return template('make_table', titles=titles, rows=items)



if __name__ == '__main__':
    # Get required port, default to 5000.
    port = os.environ.get('PORT', 5000)

    # Run the app.
    run(host='0.0.0.0', port=port)
