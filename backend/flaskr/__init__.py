import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random



from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
        
       
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    CORS(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
     
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = [category.format() for category in categories]
            cat = {}
            for i in formatted_categories:
                cat[i['id']] = i['type']
            return jsonify({
                'success': True,
                'categories': cat
            })
        except:
            abort(422)

    @app.route('/questions')
    def get_questions():
        try:    
            page = request.args.get('page', 1, type=int)
            questions = Question.query.all()
            start = (page-1)*QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            
            formatted_questions = [question.format() for question in questions[start:end]]
            if len(formatted_questions) == 0:
                abort(404)
            categories = Category.query.all()
            formatted_categories = [category.format() for category in categories]
            cat = {}
            for i in formatted_categories:
                cat[i['id']] = i['type']

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions),
                'categories': cat,
                'current_category': 0
            })
        except:
            abort(422)
    
    @app.route('/questions/<int:id>',  methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            question.delete()
            if question is None:
                abort(404)
            return jsonify({
                'success': True
            })
        except:
            abort(422)
        
    @app.route('/question',  methods=['POST'])
    def post_question():
        try:
            data = request.get_json()
            question = Question(
                question =data['question'],
                answer = data['answer'],
                difficulty = data['difficulty'],
                category = data['category']
            )
            question.insert()
            return jsonify({
                'success': True
            })
        except:
            abort(422)
   
   

    @app.route('/questions',  methods=['POST'])
    def search_question():
        try:
            searchTerm = request.get_json()['searchTerm']
            questions = Question.query.filter(Question.question.contains(searchTerm))
                
            formatted_questions = [question.format() for question in questions]
            print('my name:', formatted_questions)
            if formatted_questions == []:
                abort(404)
                
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': 0
            })
        except:
            abort(422)

    """
    @TODO:
    onnnnnnnnnnnnnnnnnnnnnnnnnn
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_question_by_category(id):
        try:
            category = Category.query.filter(Category.id==id).one_or_none()
            formatted_category = category.format()
            questions = Question.query.filter_by(category=id)
            if questions is None:
                abort(404)
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': id
            })
        except:
            abort(422)

        
        
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.+
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes',  methods=['POST'])
    def create_quiz():
        try:
            data = request.json
            quiz_category = data['quiz_category']
            previous_questions = data['previous_questions']

            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category==quiz_category['id'])
            formatted_questions = [question.format() for question in questions]
            if formatted_questions == []:
                abort(404)
            questions_left= []
            for question in formatted_questions:
                if question['id'] not in previous_questions:
                    questions_left.append(question)
            if questions_left:
                next_question= random.choice(questions_left)
            else:
                next_question= ''
            return jsonify({
                'success': True,
                'question': next_question
            })
        except:
            abort(422)
        
        
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'cannot be processed'
        }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'server error'
        }), 500
    

     

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    
   
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
   


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
