import datetime
import random
import string
from flask import  jsonify, request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

from StackOverFlow.models.models import Question

questions = Blueprint('questions', __name__,url_prefix="/questions")
questions_list = []


def get_all_questions():
      
  return [question for question in questions_list]

def get_single_question(questionId):
      
  return [question for question in questions_list if question['question_id']==questionId]

#retrieving all questions iitems
@questions.route("/", methods=['GET'])
@jwt_required()
def all_questions():
    #ensuring that a user has logged in

    all_questions = get_all_questions()
    return jsonify(all_questions)


#retrieving single questions item
@questions.route("/<string:questionId>", methods=['GET'])
def single_questions(questionId):
    single_question = get_single_question(questionId)
  
    return jsonify(single_question)


#creating questions
@questions.route("/", methods=["POST"])
@jwt_required()
def new_questions():
    if request.method == "POST":
        
        question_id =  ''.join(random.choice(string.ascii_uppercase) for i in range(3))
        user_id = get_jwt_identity()
        title = request.json['title']
        body = request.json['body']
        date_posted = datetime.datetime.now()
       
        #checking if title exists
        for question in questions_list:
            if question['title'] == title:
        
                 return jsonify({'error':"Question title already exists"}),409
        
        #checking if body exists
        for question in questions_list:
            if question['body'] == body:
        
                 return jsonify({'error':"Question body already exists"}),409
           

              #inserting values into the questions_list
        new_question = Question(questionId=question_id,title=title,body=body,user_id=user_id,date_posted=date_posted)
        
        questions_list.append(new_question.tojson()) 
         
  
    return jsonify({'message':'new question posted','question_id':question_id,'title':title,'body':body,'user_id':user_id,'date_posted':date_posted}),200
    


 
# #deleting a questions item from the database
@questions.route("/remove/<string:questionId>", methods=['DELETE'])
@jwt_required()
def delete_questions(questionId):

     for question in range(len(questions_list)):
       if questions_list[question]['id'] == questionId:
          del questions_list[question]
          break
     
     return jsonify({'message':"Question deleted"})