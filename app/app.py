from flask import Flask,jsonify,make_response,request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from models import db, User, Transaction, Category  # Import models but do not re-initialize db

app = Flask(__name__)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username',None)
    password = data.get('password',None)
    
    user = User.query.filter_by(username=username) .first()

    if user:
        if check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token),200
        else:
            return make_response('Could not verify!', 401,{'WWW-Authenticate':'Basic realm="Login required!"'})
        

@app.route('/protected',methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user),200


@app.route('/logout',methods=['POST'])
@jwt_required
def logout():
    return jsonify(logged_out=True), 200


@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    # Check if the user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return make_response('User already exists!', 409, {'WWW-Authenticate': 'Basic realm="Register required!"'})
    else:
        # Create a new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User created successfully!'), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password,
        }
        user_list.append(user_data)
        return jsonify(user_list),200
    
@app.route('/user/<int:id>', methods=['GET']) 
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password,

        }
        return jsonify(user_data),200
    else:
         return jsonify('User not found!', 404, {'WWW-Authenticate': 'Basic realm="User not found!"'})


@app.route('/user/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email',user.email)
        db.session.commit()
        return jsonify(message='User updated successfully!'),200
    else:
        return jsonify(message = 'User not found!'),404
    

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify('User deleted successfully!'),200
    else:
         return jsonify('User not found!', 404, {'WWW-Authenticate': 'Basic realm="User not found!"'})





@app.route('/transactions', methods= ['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    task_list = []
    for transaction in transactions:
        transaction_data = {
            'id':transaction.id,
            'amount':transaction.amount,
            'date':transaction.date,
            'description':transaction.description,
            'type':transaction.type,
        }





if __name__ == '__main__':
    app.run(debug=True, port=5000)
