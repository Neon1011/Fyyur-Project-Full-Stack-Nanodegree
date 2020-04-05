from flask import Flask , render_template, request , redirect, jsonify
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column , ForeignKey, Integer, String
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# data= [ { 'travel':'Egypt'} , {'travel':'Germany'},{'travel':'USA'}  ] # access via d.travel


class List(db.Model):
    __tablename__ = 'lists'
    id = Column(Integer,primary_key = True)
    name = Column(String(),nullable = False)
    def __repr__ (self):
        return 'List ' + str(self.id) + ': ' + self.name

class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer,primary_key = True)
    content = Column(String(),nullable = False)
    lid = Column(Integer,ForeignKey('lists.id'))

    def __repr__ (self):
        return  self.content

# db.create_all()
# db.session.commit()

@app.route('/')
def index():    
    return render_template('index.html',data=Item.query.all())

# ****************** FORM get data via request.form **************************
@app.route('/register',methods=["POST"])
def register():
    print("*******************")
    print(request.form.get('name') )
    print(request.form.get('r') )
    # redirect emits the /registrans route to be listened in the registerans function
    return redirect('/registerans')

@app.route('/registerans')
def registerans():
    return render_template('index.html',data=List.query.all())
# ***************************************************

# recevie msgs from view via the url    /ray2?ray2=54
# method is by default is GET
@app.route('/ray2')
def getUserURLInput():
    print(request.args.get('ray2'))
    return render_template('index.html')

@app.route('/create_new_todo',methods=["POST"])
def create_new_todo():
    body = ''
    error = False
    try:
        # get_json data
        json_data = request.get_json()
        Content = json_data['content']
        item = Item(content=Content,lid=0)
        # we just do that because we can't used the item.content in the return value after we commit the database
        body = item.content 
        db.session.add(item)
        # if any exception is throw before that line so it will not commit and will go to the except block to rollback
        db.session.commit()
    except:
        # clear the pending transactions or pending SQL Instructions (uncommited transactions)
        db.session.rollback()
        print(sys.exc_info())
        error=True
    finally:
        db.session.close()

    print(jsonify({"content":body}),"  ", body)
    # check for exception not to return a rubbish json
    if not error:
        # returns json response not an html , this is an API
        return jsonify(     {"content":body}    )

if __name__ == '__main__':
    app.run()
