from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)

#3 '/' means relative and 4 means absolute path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class ToDO(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    created=db.Column(db.DateTime,default=datetime.now)

    def __repr__(self):
        return '<Task %r>' %self.id
    #The repr method is used to get a string representation of a Python object.
    
     

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=ToDO(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue"
    else:
        tasks=ToDO.query.order_by(ToDO.created).all() 
        #oredering by date_created and returning all the data
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete=ToDO.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task=ToDO.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html', task=task)

if __name__=="__main__":
    app.run(debug=True)