API REFERENCE

GETTING STARTED

Pre-requisites and local development
    Developers using this project should have python3, pip and node installed on theirlocal machines

Backend
    From the backend folder, run:
        pip3 install -r requirements.txt
    To start the backend server, run:
        export FLASK_APP=flaskr
        export FLASK_ENV=development
        flask run
    The commands above puts the application in development and uses the __init__.py file in our flaskr folder
    The applicationruns on http://127.0.0.1:5000/ by default

Fronend
    From the frontend folder, run:
        npm install // only once to install dependencies
        npm start

Error Handling
    Errors are returned as Json objects in theformat below:
        {
            'success': False,
            'error': 422,
            'message': 'cannot be processed'
        }
    The errors the api will return includes 400, 404, 422 and 500 
    

ENDPOINTS

GET '/categories'
    Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    Request Arguments: None
    Returns: An object with success and categories keys, that contains an object of id: category_string key: value pairs as shown below:
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
    
- GET '/questions'
    Returns: An object with keys(success, categories, questions, total questions, current_category) that contain success value, categories dictionary, list of question objects with result paginated in a group of 10, and current cateory respectively
    respone body:
   [{'success': True, 'questions': [{'id': 13, 'question': 'What is the largest lake in Africa?', 'answer': 'Lake Victoria', 'category': 3, 'difficulty': 2}, {'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?', 'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3}], 'total_questions': 20, 'categories': {1: 'Science', 2: 'Art', 3: 'Geography', 4: 'History', 5: 'Entertainment', 6: 'Sports'}, 'current_category': 0}]
   
DELETE '/questions/<int:id>'
    Given an id, it deletes question of the given id from the database if it exists
    Returns: Success Value as an object
    {
        'success': True
    }

POST /question
    creates a new question in the database using the submitted question, answer, difficulty, and category parameters
    Returns a succes object
    {
        'success': True
    }


POST /questions
    searches the database for a question that matches the search term inputed.
    Returns an object with success value, list of questions that matched the search term, length of matched questions and current category
    {'success': True, 'questions': [{'id': 5, 'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", 'answer': 'Maya Angelou', 'category': 4, 'difficulty': 2}, {'id': 6, 'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 'answer': 'Edward Scissorhands', 'category': 5, 'difficulty': 3}], 'total_questions': 2, 'current_category': 0}
    
    
GET '/categories/<int:id>/questions'
    Find questions based on a particular category
    Returns: An object with keys(success, categories, questions, total questions, current_category) that contain success value, categories dictionary, list of question objects with result paginated in a group of 10, and current category respectively
    respone body:
   [{'success': True, 'questions': [{'id': 13, 'question': 'What is the largest lake in Africa?', 'answer': 'Lake Victoria', 'category': 3, 'difficulty': 2}, {'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?', 'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3}], 'total_questions': 20, 'categories': {1: 'Science', 2: 'Art', 3: 'Geography', 4: 'History', 5: 'Entertainment', 6: 'Sports'}, 'current_category': 0}]
    
    
POST '/quizzes'
    This endpoint takes category and previous question parameters
    Return a random questions within the given category, and that is not one of the previous questions and success value as an object
    {
        'success': True,
        'question': {'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?', 'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3}
    }