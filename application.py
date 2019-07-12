from flask import Flask,render_template,url_for,request,redirect,flash
from sqlalchemy import create_engine, asc,desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, ListItems,User

app= Flask(__name__)


engine= create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


categories = session.query(Category).order_by(asc(Category.name))

@app.route('/')
def showlistItems():
    items = session.query(ListItems).order_by(desc(ListItems.id))
    return render_template('list_private.html', categories = categories,items=items)


@app.route('/catalog/<string:catalogItem>')
def showCatalogItems(catalogItem):
    try:
        c_item= session.query(Category).filter_by(name=catalogItem).one()
        items=session.query(ListItems).filter_by(category_id=c_item.id)
    except NoResultFound:
        c_item = []  #
    return render_template('catalogitem.html',categories = categories,items=items,catalogItem=catalogItem) #"this page will show all the items in the catalog "+ catalogItem


@app.route('/catalog/<string:catalogItem>/<string:item>')
def showItemDescription(catalogItem,item):
    item=session.query(ListItems).filter_by(name=item).first()
    return  render_template('description.html',categories=categories,item=item)  #"this page will "+item+" description in the catalog "+ catalogItem

@app.route('/catalog/new',methods=['GET','POST'])
def addNewItem():
    if request.method=='POST':

        newItem= ListItems(name=request.form['name'],description=request.form['desc'],category_id=request.form['category'])
        session.add(newItem)
        session.commit()
        flash('Successfully Added %s' % newItem.name)
        return redirect(url_for('showlistItem'))
    else:
        return render_template('additem.html',categories=categories)

@app.route('/catalog/<int:itemid>/edit',methods=['GET','POST'])
def editItem(itemid):
    editeditem=session.query(ListItems).filter_by(id=itemid).one()
    if request.method=='POST':
        if request.form['name']:
            editeditem.name = request.form['name']
        if request.form['desc']:
            editeditem.description= request.form['desc']
        if request.form['category']:
            editeditem.category_id=request.form['category']
        flash('Successfully Edited %s' % editeditem.name)
        return redirect(url_for('showlistItems'))
    else:
        return render_template('editItem.html',categories=categories,item=editeditem)


@app.route('/catalog/<int:itemid>/delete',methods=['GET','POST'])
def deleteItem(itemid):
    deleteitem=session.query(ListItems).filter_by(id=itemid).first()
    if request.method=='POST':
        session.delete(deleteitem)
        session.commit()
        flash('Successfully Deleted %s' % deleteitem.name)
        return redirect(url_for('showlistItems'))
    else:
        return render_template('deleteItem.html',categories=categories,item=deleteitem)


if __name__ =='__main__':
    app.secret_key = 'super_secret_key'
    app.debug=True
    app.run(host='0.0.0.0',port=8000, threaded = False)
