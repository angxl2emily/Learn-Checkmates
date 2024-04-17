from flask import Flask
from flask import render_template
from flask import Response, request, abort, jsonify, json
app = Flask(__name__)

questions = [
    {
        "id": 1,
        "type": "helper",
        "image_path": "/static/helper1.png",
        "answer":"blah"
    },
    {
        "id": 2,
        "type": "smother",
        "image_path": "/static/helper2.png",
        "answer":"blah2"

    },
    {
        "id": 3,
        "type": "ladder",
        "image_path": "/static/helper3.png",
        "answer":"blah3"
    },
    {
        "id": 4,
        "type": "random",
        "image_path": "/static/helper3.png",
        "answer":"blah4"
    },
    # Add more questions as needed, each with an id, type, and image path
]
answers = [
    {
        "question_id": 1,
        "user_answer": "",
        "correct": True  # This should be True if the answer is correct, False otherwise
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

        # Get the correct answer from the question
        correct_answer = question['answer']
        # Determine if the user's answer is correct
        correct = user_answer.strip().lower() == correct_answer.strip().lower()

        # Update the answer entry with the user's answer and correctness
        answer_entry['user_answer'] = user_answer
        answer_entry['correct'] = correct

        print(answers)

        # Return the result as JSON
        return jsonify({'correct': correct})

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