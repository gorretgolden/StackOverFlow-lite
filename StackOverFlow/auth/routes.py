from flask import  jsonify, request, Blueprint
import validators
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import  create_access_token
from StackOverFlow.models.models import User
import random
import string
import datetime

auth = Blueprint('auth', __name__, url_prefix='/auth')
users_list = [] 


#signup endpoint
@auth.route('/signup', methods= ['POST','GET'])
def register_user():
  
  if request.method == "POST":
        
        user_id = ''.join(random.choice(string.ascii_uppercase) for i in range(5))
        date_created = datetime.datetime.now()
        username = request.json['username']
        email = request.json['email']
        phone_number = request.json['phone_number']
        password1 = request.json['user_password']
        
     
        #checking if email exists
        for user in users_list:
              if user['email'] == email:
                     return jsonify({'error':'Email address already exists!'}),409
        #checking if username exists
        for user in users_list:
              if user['username'] == username:
                     return jsonify({'error':'Username already exists!'}),409
          
       #checking if phonenumber exists
        for user in users_list:
              if user['phone_number'] == phone_number:
                     return jsonify({'error':'Phone number already in use!'}),409
          
       
        
        if len(password1) < 4:
          jsonify({"error":"Password is too short"})  
        
        #username alphabetic
        if username.isalpha():
          jsonify({'error':'Username must be alphabetic'})  
          
         #validate email
        if not validators.email(email):
          jsonify({'error':'Please enter a valid email address'})      
        
        #creating a hashed password in the database
        hashed_password = generate_password_hash(password1,method="sha256")
        
        #inserting values
        new_user = User(username=username,email=email,phone_number=phone_number,user_password=hashed_password,user_id=user_id,date_created=date_created)
        
        users_list.append(new_user.tojson())
        for i in users_list:
              
          print(i)
        return jsonify({'message':'new user created','userId':user_id,'username':username,'email':email,'phone number':phone_number,'password':hashed_password,'date_created':date_created})
  return jsonify({'error':'wrong credentials'}) 


#login endpoint
@auth.route('/login', methods= ['POST'])

def login_user():
      
   
        if request.method == 'POST':
          email = request.json["email"]
          password = request.json['user_password']
        
          #check if email exits
          for user in users_list:
                  if user['email'] == email:
                      #check if userpassword matches the sha password in db
                      password_check = check_password_hash(user['user_password'],password)
                      print(password_check)
                      if password_check:
                        #create refresh and acces tokens
                        access_token = create_access_token(identity=user['user_id'], fresh=True)
                        #refresh_token = create_refresh_token(identity=['user_id'])
                        print(access_token)
                        return jsonify({'message':" You logged in successfully!",'access_token':access_token,'user_email':user['email'],'user_id':user['user_id']})
                        
                      else:
                          return jsonify({'error':'wrong password'})
                              
                    
                  else:
                       return jsonify({'error':'Email address doesnt exist!'})
                
          return jsonify({'error':'user doesnt exists'})
          
        

#function to get all users
def get_users():
      
  return [user for user in users_list]


#all users endpoint
@auth.route('/users')
def users():

  all_users =  get_users()
  return jsonify(all_users)

 


