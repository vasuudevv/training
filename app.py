from flask import Flask, render_template, Blueprint, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# import flask_whooshalchemy as wa

# posts = Blueprint('posts',__name__, template_folder='templates')

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['WHOOSH_BASE'] = 'whoosh'
db = SQLAlchemy(app)

class todo(db.Model):
    __searchable__ = []
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# wa.whoosh_index(app, todo)

@app.route('/')
def index():
    todo_list = todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    new_todo = todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    tod = todo.query.filter_by(id=todo_id).first()
    tod.complete = not tod.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    tod = todo.query.filter_by(id=todo_id).first()
    db.session.delete(tod)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/search',methods=['GET','POST'])
def search():
    if request.methods == 'POST':
        form = request.form
        search_val = form['search']
        search = "%{0}%".format(search_val)
        result = todo.query.filter(todo.title.like(search)).all()
        return render_template('base.html',todo_list=result)
    else:
        return redirect('/')
    
if __name__ == "__main__":
    db.create_all()
    
    app.run(debug=True)