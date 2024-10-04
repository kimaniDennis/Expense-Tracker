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

@app.route('/', methods=['GET'], endpoint='index')
def index():
    return jsonify({
        "message": "Welcome to Digishop App."
    }), 200

# Protected login route requiring JWT authentication
@app.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    # Query the database for users
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password matches
    if user:
        if check_password_hash(user.password_hash, password):
            # Create JWT token for the user
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# Protected route
@app.route('/protected', methods=['GET'], endpoint='protected')
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/logout', methods=['GET'], endpoint='logout')
@jwt_required
def logout():
    return jsonify(logged_out=True), 200

# Register route
@app.route('/register', methods=['POST'], endpoint='register')
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
    
#Get all users
@app.route('/users', methods=['GET'], endpoint='users')
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data ={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_active': user.is_active

        }
        user_list.append(user_data)
    return jsonify(user_list), 200

#Get a single user
@app.route('/users/<int:id>', methods=['GET'], endpoint='user')
def get_user(id):
    user = User.query.get(id)
    if user:
        user_data ={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_active': user.is_active
        }
        return jsonify(user_data), 200
    else:
        return jsonify('User not found!', 404, {'WWW-Authenticate': 'Basic realm="User not found!"'})

# Update a user
@app.route('/users/<int:id>', methods=['PUT'], endpoint='update_user')
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.set_password(data.get('password'))  # Assuming you want to update the password
        user.is_active = data.get('is_active', user.is_active)
        db.session.commit()
        return jsonify(message='User updated successfully!'), 200
    else:
        return jsonify(message='User not found!'), 404


#Delete a user
@app.route('/users/<int:id>', methods=['DELETE'], endpoint='delete_user')
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify('User deleted successfully!', 200)
    else:
        return jsonify('User not found!', 404, {'WWW-Authenticate': 'Basic realm="User not found!"'})



@app.route('/transactions', methods= ['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    transaction_list = []
    for transaction in transactions:
        transaction_data = {
            'id':transaction.id,
            'amount':transaction.amount,
            'date':transaction.date,
            'description':transaction.description,
            'type':transaction.type,
        }
        transaction_list.append(transaction_data)
        return jsonify(transaction_list),200
    

@app.route('/transaction/<int:transaction_id>', methods= ['GET'])
def get_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        transaction_data = {
            'id':transaction.id,
            'amount':transaction.amount,
            'date':transaction.date,
            'description':transaction.description,
            'type':transaction.type,
        }
        return jsonify(transaction_data),200
    else:
        return jsonify({"error":"Transaction not found"}),404
    

@app.route('/transaction',methods=['POST'])
def add_transaction():
    data = request.get_json()
    print("Received JSON data:",data)
    amount = data.get('amount',None)
    description = data.get('description',None)
    type = data.get('type',None)

    if amount and description and type is not None:
        new_transaction = Transaction(amount=amount,description=description,type=type)
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(message='Transaction added successfully!'),201
    else:
        return jsonify(message='Transaction is not added! Something wrong'),400
    

@app.route('/transaction/<int:transaction_id>', methods =['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        data = request.json
        transaction.amount = data.get('amount',transaction.amount)
        transaction.description = data.get('description',transaction.description)
        transaction.type = data.get('type',transaction.type)

        db.session.commit()
        return jsonify({"message":"Transaction updated successfully!"}),200
    else:
        return jsonify({"error":"Transaction not updated"}),404
    

@app.route('/transaction/<int:transaction_id>',methods=['GET'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"message":"Transaction deleted successfully"}),200
    else:
        return jsonify({"error":"Transaction not deleted"}),404
    


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = []

    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at
        }
        category_list.append(category_data)
    
    return jsonify(category_list), 200



@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category:
        category_data = {
            'id': category.id,
            'name': category.name,
            'created_at': category.created_at
        }
        return jsonify(category_data), 200
    else:
        return jsonify({"error": "Category not found"}), 404
    


@app.route('/category', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name', None)

    if name:
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category added successfully!"}), 201
    else:
        return jsonify({"message": "Category name is required!"}), 400
    



@app.route('/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if category:
        data = request.get_json()
        category.name = data.get('name', category.name)
        
        db.session.commit()
        return jsonify({"message": "Category updated successfully!"}), 200
    else:
        return jsonify({"error": "Category not found"}), 404
    


@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully!"}), 200
    else:
        return jsonify({"error": "Category not found"}), 404







if __name__ == '__main__':
    app.run(debug=True, port=5000)
