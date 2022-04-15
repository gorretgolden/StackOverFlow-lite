
class User(object):
       
    def __init__(self, username:str,email:str,phone_number:str, user_password:str,user_id:str,date_created:str):
        self.user_id = user_id
        self.username = username
        self.user_password = user_password
        self.email    = email
        self.phone_number  = phone_number
        self.date_created = date_created
        
    def __str__(self):
        return "User(username='%s')" % self.username


    def tojson(self):
        return self.__dict__
    

  

class Question(object):
    
    def __init__(self,questionId,title:str, body:str,date_posted:str,user_id:str):
        self.question_id = questionId
        self.user_id = user_id
        self.title = title
        self.body = body
        self.date_posted = date_posted
       
    def __str__(self):
        return "Question(id='%s')" % self.id
     
    def tojson(self):
            return self.__dict__
    

class Answer(object):
    
    def __init__(self,answer_id,questionId,title:str, body:str,date_answered:str,is_answered:bool=False):
        self.answer_id = answer_id
        self.title = title
        self.body = body
        self.questionId = questionId
        self.is_answered = is_answered
        self.date_answered = date_answered
       
    def __str__(self):
        return "Question(id='%s')" % self.answer_id       