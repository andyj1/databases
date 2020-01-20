# ref: https://edykim.com/ko/post/getting-started-with-sqlalchemy-part-2/

import sqlalchemy
print(sqlalchemy.__version__)

# solve privilege issue from https://stackoverflow.com/questions/37239970/connect-to-mysql-server-without-sudo
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://user@localhost:3306/sailors', echo=True)

# use existing database sailor
engine.execute("use sailors")

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

# class structure example
class User(Base):
    __tablename__ = 'users'
    # use Sequence to use like Firebird/Oracle
    # id = Column(Integer, Sequence('user_id_seq'), primary_key=True) 

    # can specify varlength: Column(String(50)), but not necessary
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

# 1. adding an instance
# tmp = Sailor(sid=98, sname='joe', rating=7, age=25)
# s.add(tmp)
# s.commit()

# 2. querying for instances
# sailors = s.query(Sailor)

# 3. see name label for Columns: 
# for row in session.query(User.name.label('name_label')).all():
#       print(row.name_label)

# 4. labels for Class entities using 'aliased'
# from sqlalchemy.orm import aliased
# user_alias = aliased(User, name='user_alias')
# for row in session.query(user_alias, user_alias.name).all():
#       print(row.user_alias)

# 5. filter operator
# EQUALS: query.filter(User.name == 'ed')
# NOT EQUALS: query.filter(User.name != 'ed')
# LIKE: query.filter(User.name.like('%ed%'))
# IN: query.filter(User.name.in_(['ed','wendy','jack']))
# SUBQUERY: query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))))
# NOT IN: query.filter(~User.name.in_(['ed','wendy','jack']))
# IS NULL: filter(User.name == None)
# AND: 
#   from sqlalchemy import and_
#   filter(and_(User.name == 'ed', User.fullname == 'Edward')) --> or chain with '.'
# OR:
#   from sqlalchemy import or_
#   filter(or_(User.name=='ed', User.name =='wendy'))
# MATCH: query.filter(User.name.match('wendy'))

# 6. aliasing for multiple table queries
# from sqlalchemy.orm import aliased
# adalias1 = aliased(Address)
# adalias2 = aliased(Address)
# for username, email1, email2 in \
#     session.query(User.name, adalias1.email_address, adalias2.email_address).\
#     join(adalias1, User.addresses).\
#     join(adalias2, User.addresses).\
#     filter(adalias1.email_address=='jack@gmail.com').\
#     filter(adalias2.email_address=='jack@yahoo.com'):
#     print username, email1, email2
# # jack jack@gmail.com jack@yahoo.com

# 7. subquery statement
# from sqlalchemy.sql import func
# stmt = session.query(Address.user_id, func.count('*').label('address_count')).\
#         group_by(Address.user_id).subquery()
# --> translates to the subquery in 
#       SELECT users.*, adr_count.address_count
#    FROM users
#    LEFT OUTER JOIN (
#            SELECT user_id, count(*) AS address_count
#            FROM addresses GROUP BY user_id
#        ) AS adr_count
#        ON users.id = adr_count.user_id
# --> and then use like this:
#   for u, count in session.query(User, stmt.c.address_count).\
#         outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
#         print u, count
# # <User('wendy', 'Wendy Williams', 'foobar')> None
# # <User('mary', 'Mary Contrary', 'xxg527')> None
# # <User('fred', 'Fred Flinstone', 'blar')> None
# # <User('haruair', 'Edward Kim', '1234')> None
# # <User('jack', 'Jack Bean', 'sadfjklas')> 2

# 7(b). if subquery is for selecting eneity, use aliased
# stmt = session.query(Address).\
#                 filter(Address.email_address != 'jack@yahoo.com').\
#                 subquery()
# adalias = aliased(Address, stmt)
# for user, address in session.query(User, adalias).\
#         join(adalias, User.addresses):
#     print user, address
# # <User('jack', 'Jack Bean', 'sadfjklas')> <Address('jack@gmail.com')>

