from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, joinedload
from database_setup import Base, Category, ListItems, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import requests
import random
import json
import httplib2
import string
from flask import session as login_session
from flask import make_response
from flask import Flask, render_template, url_for, request
from flask import redirect, flash, jsonify
from functools import wraps
import logging


app = Flask(__name__)


engine = create_engine('sqlite:///categorywithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "CatalogApp"

categories = session.query(Category).order_by(asc(Category.name))



def login_required(f):
    """ View decorator to avoid repeated code """
    @wraps(f)

    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return decorated_function


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
# The current session state is %s"% login_session['state']
# STATE =state is added to set the login state on POST


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    # comparing client id with google id
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        logging.info("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    print '*********'+login_session['access_token']
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if the user exists if not make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;height: 300px;'
    'border-radius:150px;-webkit-border-radius: '
    '150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    # print "done!"
    return output


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            # del login_session['credentials']
        # if login_session['provider']=='facebook':
            # fbdisconnect()
            # del login_session['facebook_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        del login_session['user_id']

        flash("You have successfully been logged out.")
        return redirect(url_for('showlistItems'))
    else:
        flash("You were not logged in to begin with.")
        return redirect(url_for('showlistItems'))


# code to implement logout
# @app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')

    if access_token is not None:
        print 'In gdisconnect access token is %s', access_token
        print 'User name is: '
        print login_session['username']
        url = 'https://accounts.google.com/o/oauth2/'
        'revoke?token=%s' % access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
    else:
        logging.info("Access Token None")
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog.JSON')
def catalogJSON():
    categories = session.query(Category).options(joinedload
                                                 (Category.listitems)).all()
    data = dict(Catalog=[dict(c.serialize,
                              items=[i.serialize for i in c.listitems])
                         for c in categories])
    return jsonify(data)


@app.route('/')
def showlistItems():
    items = session.query(ListItems).order_by(desc(ListItems.id))
    # if 'username' not in login_session:
    # return render_template('lists.html', categories = categories,items=items)

    return render_template('list_private.html',
                           categories=categories, items=items)


@app.route('/catalog/<string:catalogItem>')
def showCatalogItems(catalogItem):
    try:
        c_item = session.query(Category).filter_by(name=catalogItem).one()
        items = session.query(ListItems).filter_by(category_id=c_item.id)
        if 'username' not in login_session:
            return render_template('catalog_public.html',
                                   categories=categories,
                                   items=items, catalogItem=catalogItem)
        return render_template('catalogitem.html',
                               categories=categories,
                               items=items, catalogItem=catalogItem)
# "this page will show all the items in the catalog "+ catalogItem

    except NoResultFound:
        c_item = []  #


@app.route('/catalog/<string:catalogItem>/<string:item>')
def showItemDescription(catalogItem, item):
    item = session.query(ListItems).filter_by(name=item).first()
    return render_template('description.html',
                           categories=categories, item=item)
# "this page will "+item+" description in the catalog "+ catalogItem


@app.route('/new', methods=['GET', 'POST'])
@login_required
def addNewCategory():
    # if 'username' not in login_session:
    #    return redirect('/login')
    if request.method == 'POST':
        if request.form['name'] == '':
            flash("Please enter a category to add")
            return render_template('addCategory.html', categories=categories)
        else:
            newCategory = Category(name=request.form['name'],
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
            flash('Successfully Added %s' % newCategory.name)
            return redirect(url_for('showlistItems'))
    else:
        return render_template('addCategory.html', categories=categories)


def checkValid():
    if request.form['name'] == '':
        print "name is blank"
        return False
    elif request.form['desc'] == '':
        return False
    elif request.form['category'] == '':
        return False

    return True


@app.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def addNewItem():
    # if 'username' not in login_session:
        # return redirect('/login')
    if request.method == 'POST':

        if checkValid():
            newItem = ListItems(name=request.form['name'],
                                description=request.form['desc'],
                                category_id=request.form['category'],
                                user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            flash('Successfully Added %s' % newItem.name)
            return redirect(url_for('showlistItems'))
        else:
            flash('All the form fields are required.')
            return render_template('additem.html', categories=categories)
    else:
        return render_template('additem.html', categories=categories)


@app.route('/catalog/<int:itemid>/edit', methods=['GET', 'POST'])
@login_required
def editItem(itemid):
    editeditem = session.query(ListItems).filter_by(id=itemid).one()
    user_id = login_session['user_id']
    if request.method == 'POST':
        if user_id == editeditem.user_id:
            if request.form['name']:
                editeditem.name = request.form['name']
            if request.form['desc']:
                editeditem.description = request.form['desc']
            if request.form['category']:
                editeditem.category_id = request.form['category']
            session.add(editeditem)
            session.commit()
            flash('Successfully Edited %s' % editeditem.name)
            return redirect(url_for('showlistItems'))
        else:
            flash('You are not authorized to edit item %s' % editeditem.name)
            return redirect(url_for('showlistItems'))
    else:
        return render_template('editItem.html',
                               categories=categories, item=editeditem)


@app.route('/catalog/<int:itemid>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(itemid):
    deleteitem = session.query(ListItems).filter_by(id=itemid).first()
    user_id = login_session['user_id']
    if request.method == 'POST':
        if user_id == deleteitem.user_id:
            session.delete(deleteitem)
            session.commit()
            flash('Successfully Deleted %s' % deleteitem.name)
            return redirect(url_for('showlistItems'))
        else:
            flash('You are not authorized to delete item %s' % deleteitem.name)
            return redirect(url_for('showlistItems'))
    else:
        return render_template('deleteItem.html',
                               categories=categories, item=deleteitem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
