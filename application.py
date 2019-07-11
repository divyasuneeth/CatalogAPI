from flask import Flask,render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, ListItems

app= Flask(__name__)


engine= create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


categories = session.query(Category).order_by(asc(Category.name))

@app.route('/')
def showlistItems():
    items = session.query(ListItems).order_by(asc(ListItems.name))
    return render_template('lists.html', categories = categories,items=items)


@app.route('/catalog/<string:catalogItem>/items')
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

if __name__ =='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=8000, threaded = False)
