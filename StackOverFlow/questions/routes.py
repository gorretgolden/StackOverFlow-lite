import datetime
import random
import string
from flask import  jsonify, request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

from StackOverFlow.models.models import Answer, Question

questions = Blueprint('questions', __name__,url_prefix="/questions")
questions_list = []
answers_list = []


def get_all_questions():
      
  return [question for question in questions_list]
#get all answers for a question
def get_all_answers():
      
  return [answer for answer in answers_list]

#return the id of the question
def get_question_id(questionId):
      
  return [question for question in questions_list if question['question_id']==questionId]


#return the id of the answer
def get_answer_id(answer_id):
      
  return [answer for answer in answers_list if answer['question_id']==answer_id]

#return the id of the user for an answer
def get_user_id(user_id):
      
  return [answer for answer in answers_list if answer['user_id']==user_id]

#retrieving all questions 
@questions.route("/", methods=['GET'])
@jwt_required()
def all_questions():
    #ensuring that a user has logged in

    all_questions = get_all_questions()
    return jsonify(all_questions)


#retrieving single questions item
@questions.route("/<string:questionId>", methods=['GET'])
def single_question(questionId):
    single_question = get_question_id(questionId)
  
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
        tag = request.json['tag']
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
        new_question = Question(questionId=question_id,title=title,body=body,user_id=user_id,tag=tag, date_posted=date_posted)
        
        questions_list.append(new_question.tojson()) 
         
  
    return jsonify({'message':'new question posted','question_id':question_id,'tag':tag,'title':title,'body':body,'user_id':user_id,'date_posted':date_posted}),200
    


 
# #deleting a questions item from the database
@questions.route("/remove/<string:questionId>", methods=['DELETE'])
@jwt_required()
def delete_questions(questionId):

     for question in range(len(questions_list)):
       if get_question_id(questionId) == questionId:
          del questions_list[question]
          break
     
     return jsonify({'message':"Question deleted"})


#creating answers
@questions.route("/<string:questionId>/answers", methods=["POST"])
@jwt_required()
def new_answers(questionId):
    if request.method == "POST":
        answer_id = ''.join(random.choice(string.ascii_uppercase) for i in range(3))
        question_id =  get_question_id(questionId) 
        user_id = get_jwt_identity()
        body = request.json['body']
        date_posted = datetime.datetime.now()
       
        #checking if body exists
        for answer in answers_list:
            if answer['body'] == body:
        
                 return jsonify({'error':"This answer to the question exists"}),409
        
           

              #inserting values into the questions_list
        new_answer = Answer(answer_id=answer_id, questionId=question_id,body=body,user_id=user_id, date_answered=date_posted)
        
        answers_list.append(new_answer.tojson()) 
         
  
    return jsonify({'message':'new answer posted','answer_id':answer_id,'question':question_id,'body':body,'user_id':user_id,'date_answered':date_posted}),200
    

#Viewing an answer by id
@questions.route("/<string:answer_id>/answers", methods=["POST"])
@jwt_required()
def single_answer(answer_id):
    single_answer = get_answer_id(answer_id)
  
    return jsonify(single_answer)

#retrieving all answers for a specific user
@questions.route("/answers/<string:user_id>", methods=['GET'])
@jwt_required()
def user_answers(user_id):
    #ensuring that a user has logged in
    
    answers = get_user_id(user_id)
    return jsonify(answers)

#retrieving all answers
@questions.route("/questions/answers", methods=['GET'])
@jwt_required()
def all_answers():
    #ensuring that a user has logged in

    all_answers = get_all_answers()
    return jsonify(all_answers)