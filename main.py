from flask import Flask,request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
from server.validate.validate import validation

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:happy@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)



class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(120))
    Body = db.Column(db.Text())

    def __init__(self, title,body):
        self.Title = title
        self.Body = body

    
    

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        new_post = Blog(title,body)
        db.session.add(new_post)
        db.session.commit()
    

    post = Blog.query.all()



    return render_template('blog.html', posts=post)

@app.route('/currentpost',methods=['POST','GET'])
def currentpost():
    
    title=''
    body=''
    errors=[]

    

    if request.method=='POST':
        if validation(request)==True:
            title=request.form['title']
            body=request.form['body']
            new_post = Blog(title,body)
            db.session.add(new_post)
            db.session.commit()
            postId=(new_post.id)
            return redirect(f'/post?postId={postId}')
        else:
            return render_template('currentpost.html',errors=validation(request),title=title,body=body)
    
    
    return render_template('currentpost.html', errors=errors, title=title,body=body)

@app.route('/blog',methods=['POST','GET'])
def blog():

    post = Blog.query.all()

    return render_template('blog.html', posts=post)

@app.route('/post',methods=['GET'])
def post():
    postId=request.args.get('postId')
    post=Blog.query.filter_by(id=postId).first()
    return render_template('post.html',post=post)    


if __name__=="__main__":
    app.run()
    