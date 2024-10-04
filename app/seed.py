from datetime import datetime
from app import app, db, User, Category, Transaction

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        {'username': "john", 'email': 'john123@gmail.com', 'password': 'password123456'}
    ]

    for user_data in users:
        user = User(username=user_data['username'], email=user_data['email'])
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        print("Sample users added successfully!!")

    transactions = [
        {'amount': '3000', 'date': datetime.strptime("2024-08-28 10:00:00", "%Y-%m-%d %H:%M:%S"),
         'description': 'Grocery shopping', 'type': 'Expense'}
    ]

    for transaction_data in transactions:
        transaction = Transaction(amount=transaction_data['amount'], date=transaction_data['date'],
                                   description=transaction_data['description'], type=transaction_data['type'])
        db.session.add(transaction)
        db.session.commit()
        print("Sample Transaction added successfully!!")

    categories = [
        {'name': 'Food', 'created_at': datetime.strptime("2024-08-28", "%Y-%m-%d")}
    ]

    for category_data in categories:
        category = Category(name=category_data['name'], created_at=category_data['created_at'])
        db.session.add(category)
        db.session.commit()

    print("Sample Category added successfully!!")
