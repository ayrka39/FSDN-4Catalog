from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import jsonify, make_response
from flask import session as login_session
from database_setup import Base, User, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from functools import wraps
import json
import random
import string
import httplib2
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "World Maps Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Functions
def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function


app = Flask(__name__)


@app.route('/')
@app.route('/category')
def showCategories():
    # Get all categories
    categories = session.query(Category).all()

    return render_template(
        'categories.html',
        categories=categories)


@app.route('/category/<int:category_id>')
@app.route('/category/<int:category_id>/items')
def showCategory(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).first()
    categoryName = category.name
    Items = session.query(Item).filter_by(category_id=category_id).all()
    ItemsCount = session.query(Item).filter_by(category_id=category_id).count()

    return render_template(
        'category.html',
        categories=categories,
        Items=Items,
        categoryName=categoryName,
        ItemsCount=ItemsCount)


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def newCategory():
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('add_category.html')


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    error = False
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(category)
            session.commit()
            return redirect(url_for('showCategories'))
        else:
            if category.user_id != login_session['user_id']:
                error = True
            return render_template(
                'delete_category.html', category=category, error=error)
    else:
        return redirect(url_for('showCategories'))


@app.route('/category/<int:category_id>/items/<int:item_id>')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    creator = getUserInfo(item.user_id)

    return render_template(
        'items.html',
        item=item,
        creator=creator)


@app.route('/category/items/add', methods=['GET', 'POST'])
@login_required
def newItem():
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category).all()
        return render_template('add_item.html', categories=categories)


@app.route('/category/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    error = False
    editedItem = session.query(Item).filter_by(id=item_id).first()
    if editedItem.user_id == login_session['user_id']:
        if request.method == 'POST':
            if request.form.get('name'):
                editedItem.name = request.form['name']
            if request.form.get('description'):
                editedItem.description = request.form['description']
            if request.form.get('category'):
                editedItem.category_id = request.form['category']
            session.add(editedItem)
            session.commit()
            return redirect(url_for('showItem',
                                    category_id=category_id,
                                    item_id=item_id))
        else:
            if editedItem.user_id != login_session['user_id']:
                error = True
            return render_template('edit_item.html',
                                   item=editedItem,
                                   category_id=category_id,
                                   error=error)
    else:
        return redirect(url_for('showItem'))


@app.route('/category/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    error = False
    item = session.query(Item).filter_by(id=item_id).first()
    if item.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            return redirect(url_for('showCategory', category_id=category_id))
        else:
            if item.user_id != login_session['user_id']:
                error = True
            return render_template(
                'delete_item.html', item=item, error=error)
    else:
        return redirect(url_for('showItem'))


# Create anti-forgery state token
@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/logout')
def logout():
    if login_session['provider'] == 'google':
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']

    del login_session['username']
    del login_session['email']
    del login_session['user_id']
    del login_session['provider']

    return redirect(url_for('showCategories'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate anti-forgery state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        flow = flow_from_clientsecrets('client_secrets.json',
                                       scope='',
                                       redirect_uri='postmessage')
        credentials = flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "Login Successful"


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/category/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/category/<int:category_id>/JSON')
@app.route('/category/<int:category_id>/items/JSON')
def showCategoryJSON(category_id):
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/category/<int:category_id>/items/<int:item_id>/JSON')
def showItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    category = session.query(Category).filter_by(id=category_id).first()
    return jsonify(item=[item.serialize], category=[category.serialize])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'secret_key'
    app.run(host='0.0.0.0', port=5000)
