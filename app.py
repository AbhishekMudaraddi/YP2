from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change in production!

# Configure DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Change to your region
users_table = dynamodb.Table('Users')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    try:
        users_table.put_item(
            Item={
                'username': username,
                'password': generate_password_hash(password)
            }
        )
        return redirect(url_for('welcome'))
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        response = users_table.get_item(Key={'username': username})
        if 'Item' in response and check_password_hash(response['Item']['password'], password):
            session['username'] = username
            return redirect(url_for('welcome'))
        return "Invalid credentials"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)