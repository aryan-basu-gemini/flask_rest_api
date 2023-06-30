from flask import Flask,request

from flask_restful import Resource,Api

from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app=Flask(__name__)

api=Api(app)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///rest_api.db"
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class UserModel(db.Model):
    tablename='users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String())
    password=db.Column(db.String())
    email=db.Column(db.String(),unique=True,nullable=False)

    def init(self,username,password,email):
        self.username=username
        self.password=password
        self.email=email
    
    def repr(self):
        return f"<User {self.username}>"
    
@app.route('/users',methods=['POST','GET'])
def users():
    if request.method == 'POST':
        if request.is_json:
            data=request.get_json()
            new_user=UserModel(
                username=data['username'],
                password=data['password'],
                email=data['email'],
            )
            db.session.add(new_user)
            db.session.commit()
            return {"messages":f"user {new_user.username} with email:{new_user.email} has been created successfully"}
        else:
            return {"error":"The request payload is not in JSON format"}
    elif request.method=='GET':
        users=UserModel.query.all()
        results=[
            {
                "username":user.username,
                "password":user.password,
                "email":user.email,
            }for user in users
        ]


        return {"users":results}

@app.route('/users/<user_id>',methods=['GET','PUT','DELETE'])
def user_by_id(user_id):
    user=UserModel().query.get_or_404(user_id)
    if request.method=='GET':
        response={
                "username":user.username,
                "password":user.password,
                "email":user.email

        }
        return {"message":"success","user":response}
    elif request.method=='PUT':
        data=request.get_json()
        user.username=data['username']
        user.password=data['password']
        user.email=data['email']
        db.session.add(user)
        db.session.commit()
        return {"message":f'User {user.username} with email:{user.email} succesfully updated'}
    elif request.method=='DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"message":f'User {user.username} with email:{user.email} succesfully deleted'}
    if __name__=="__main__":
        app.run(debug=True)

    
    

