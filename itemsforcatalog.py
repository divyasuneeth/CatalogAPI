from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, ListItems, User

engine = create_engine('sqlite:///categorywithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# create dummy user

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/'
             '18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# items for Soccer
category1 = Category(name="Soccer", user_id=1,)

session.add(category1)
session.commit()

catalogItem1 = ListItems(user_id=1, name="Two shingaurds",
                         description="Description for two shingaurd ",
                         category=category1)

session.add(catalogItem1)
session.commit()


catalogItem2 = ListItems(user_id=1, name="Shingaurds",
                         description="Description for shingaurd",
                         category=category1)

session.add(catalogItem2)
session.commit()


# items for Basketball
category2 = Category(user_id=1, name="Basketball")

session.add(category2)
session.commit()


# items for Snowboarding
category3 = Category(user_id=1, name="Snowboarding")

session.add(category3)
session.commit()


catalogItem1 = ListItems(user_id=1, name="Goggles",
                         description="Description for Goggles",
                         category=category3)

session.add(catalogItem1)
session.commit()


catalogItem2 = ListItems(user_id=1, name="Snowboard",
                         description="Snowboarding is a winter sport"
                         " that involves descending a slope that is covered "
                         "with snow while standing on a board attached to a "
                         "rider's feet, using a special boot set onto a"
                         " mounted"
                         " binding. The development of snowboarding was "
                         "inspired by skateboarding, sledding, surfing and "
                         "skiing.", category=category3)

session.add(catalogItem2)
session.commit()


print "added category items!"
