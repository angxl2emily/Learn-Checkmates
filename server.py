from flask import Flask
from flask import render_template
from flask import Response, request, abort, jsonify, json
app = Flask(__name__)

questions = [
    {
        "id": 1,
        "type": "helper",
        "image_path": "/static/quiz1.png",
        "answer":"qd7",
        "explanation":"The answer is qd7 since that is the square where the bishop protects the queen, and the queen prevents the king from escaping check."
    },
    {
        "id": 2,
        "type": "helper",
        "image_path": "/static/quiz2.png",
        "answer":"qg8",
        "explanation": "The answer is qg8 since that is the square where the knight protects the queen, and the queen prevents the king from escaping check."

    },
    {
        "id": 3,
        "type": "helper",
        "image_path": "/static/quiz3.png",
        "answer":"qg7",
        "explanation": "The answer is qg7 since that is the square where the rook protects the queen, and the queen prevents the king from escaping check."
    },
    {
        "id": 4,
        "type": "ladder",
        "image_path": "/static/quiz4.png",
        "answer":"ra3",
        "explanation": "The answer is ra3 because while the rook on b2 blocks the b file, ra3 allows the second rook to block the a file, and the king has no place to escape"
    },
    {
        "id": 5,
        "type": "ladder",
        "image_path": "/static/quiz5.png",
        "answer":"rh7",
        "explanation": "The answer is rh7 because that continues to limit the king's available squares in a ladder motion, forcing the king into the last available row, row 8."
    },
    {
        "id": 6,
        "type": "ladder",
        "image_path": "/static/quiz6.png",
        "answer":"rb2",
        "explanation": "The answer is rb2 because that continues to limit the king's available squares in a ladder motion, forcing the king into the last available file, column a."

    },
    {
        "id": 7,
        "type": "smother",
        "image_path": "/static/quiz7.png",
        "answer":"qb8",
        "explanation":"The answer is qb8 because that successfully traps the king, since the only available move for black is to capture the queen with the rook."
    },
    {
        "id": 8,
        "type": "smother",
        "image_path": "/static/quiz8.png",
        "answer":"Nf7",
        "explanation": "The answer is Nf7 because that successfully checkmates the king. There is no option for the king to run away, and knight attacks can't be blocked."
    },
]
answers = [
    {
        "question_id": 1,
        "user_answer": "",
        "correct": False  # This should be True if the answer is correct, False otherwise
    },
    {
        "question_id": 2,
        "user_answer": "",
        "correct": False  # This is False because the user's answer was not correct
    },
    # Add more answers as needed
]

@app.route('/')
def welcome():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/helper')
def helper():
    return render_template('helper.html')
@app.route('/helper2')
def helper2():
    return render_template('helper2.html')

@app.route('/smother')
def smother():
    return render_template('smother.html')
@app.route('/smother2')
def smother2():
    return render_template('smother2.html')

@app.route('/ladder')
def ladder():
    return render_template('ladder.html')
@app.route('/ladder2')
def ladder2():
    return render_template('ladder2.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


# Index of the current question
current_question_index = 0

@app.route('/next-question-image', methods=['GET'])
def get_next_question_image():
    global current_question_index

    # Check if there are more questions in the list
    if current_question_index < len(questions):
        # Get the current question
        current_question = questions[current_question_index]
        # Increment the index for the next request
        current_question_index += 1
    else:
        # If there are no more questions, reset the index (optional)
        current_question_index = 0
        current_question = questions[current_question_index]

    # Return the current question's image path as JSON
    return jsonify({
        "id": current_question["id"],
        "type": current_question["type"],
        "image_url": current_question["image_path"],
        "answer": current_question["answer"]
    })

@app.route('/question-by-type', methods=['GET'])
def get_question_by_type():
    # Get the type from the request arguments
    selected_type = request.args.get('type')
    
    # Find the first question that matches the selected type
    for question in questions:
        if question["type"] == selected_type:
            # Return the question data as JSON
            return jsonify({
                "id": question["id"],
                "image_url": question["image_path"],
                "answer": question.get("answer", "")
            })
    
    # If no question matches the type, return an empty response (optional)
    return jsonify({}), 404

@app.route('/check-answer', methods=['POST'])
def check_answer():
    # Parse the request data
    data = request.get_json()
    question_id = data.get('questionId')
    user_answer = data.get('userAnswer')

    # Find the question with the given ID
    question = next((q for q in questions if q['id'] == question_id), None)

    if question:
        # Find the answer entry in the answers list for the given question ID
        answer_entry = next((ans for ans in answers if ans['question_id'] == question_id), None)

        # Check if the answer entry exists, if not, create a new one
        if not answer_entry:
            answer_entry = {
                'question_id': question_id,
                'user_answer': '',
                'correct': False
            }
            answers.append(answer_entry)

        # Get the correct answer and explanation from the question
        correct_answer = question['answer']
        explanation = question['explanation']

        # Determine if the user's answer is correct
        correct = user_answer.strip().lower() == correct_answer.strip().lower()

        # Update the answer entry with the user's answer and correctness
        answer_entry['user_answer'] = user_answer
        answer_entry['correct'] = correct

        # Return the result along with the explanation as JSON
        return jsonify({'correct': correct, 'explanation': explanation})

    # Return an error response if the question ID is invalid
    return jsonify({'error': 'Invalid question ID'}), 400
    
@app.route('/results')
def results():
    # Calculate the user's score
    total_questions = len(questions)
    correct_answers = sum(1 for ans in answers if ans['correct'])

    # Render the results.html template with the score and total questions
    return render_template('results.html', score=correct_answers, total_questions=total_questions)

if __name__ == '__main__':
   app.run(debug = True)