from flask import Flask, request, jsonify,render_template,session,url_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_

app = Flask(__name__)
db_url = 'mysql+pymysql://root:123456@127.0.0.1:3306/library'
db = create_engine(db_url, echo=True)


Base = declarative_base()

class Lib(Base):
    __tablename__ = 'Lib'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name',String)
    author = Column('author',String)
    price = Column('price',String)
    def __str__(self) -> str:
        return "id: {}, name: {}, author: {},price:{}".format(
            self.id, self.name, self.author,self.price
        )


#查询数据
@app.route('/query',methods=["GET"])
def query():
    name = request.args.get("name","default name")
    author = request.args.get("author","default author")
    price = request.args.get("price","default price")

    session = sessionmaker(bind=db, expire_on_commit=False)()
    try:
        resp = {
            "res": [],
        }
        for rd in session.query(Lib).filter(or_(Lib.name == name, Lib.author == author)).all():
            resp["res"].append({
                "id": rd.id,
                "name": rd.name,
                "author": rd.author,
                "price":rd.price,
            })
        return jsonify(resp)

    except Exception as e:
        print(e)
        return "error"

# 增加数据
@app.route("/add",methods=["POST"])
def add():
    name=request.form.get("name","default name")
    author=request.form.get("author","default author")
    price=request.form.get("price","default author")
    rd=Lib(name=name,author=author,price=price)
    session=sessionmaker(bind=db,expire_on_commit=False)()
    try:
        session.add(rd)
        session.commit()
    except Exception as e:
        print(e)
        return "add error"

    resp={
        "id":rd.id,
        "name":rd.name,
        "author":rd.author,
        "price":rd.price,
    }
    return jsonify(resp)






if __name__ == '__main__':
    app.run(debug=True)
