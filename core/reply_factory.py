from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        responses.append(BOT_WELCOME_MESSAGE)

    success, error = save_current_answer(message, session)

    if not success:
        return [error]

    next_question, next_question_id = fetch_next_question(session)

    if next_question:
        responses.append(next_question)
    else:
        final_message = create_final_response(session)
        responses.append(final_message)

    session["current_question_id"] = next_question_id
    session.save()

    return responses

def save_current_answer(answer, session):
    '''
    Validates and stores the current answer in the Django session.
    '''
    if not isinstance(answer, str) or not answer.strip():
        return False, "Invalid answer. Please provide a valid response."

    user_data = session.get("user_data", {"answers": []})
    user_data['answers'].append(answer)
    session["user_data"] = user_data

    return True, None

def fetch_next_question(session):
    '''
    Retrieves the next question from PYTHON_QUESTION_LIST based on the current question ID.
    '''
    user_data = session.get("user_data", {"answers": []})
    questions = PYTHON_QUESTION_LIST

    current_index = len(user_data['answers'])
    if current_index >= len(questions):
        return None, None

    next_question = questions[current_index]
    next_question_id = current_index + 1
    return next_question, next_question_id

def create_final_response(session):
    '''
    Generates a final message including the user's score based on their answers.
    '''
    user_data = session.get("user_data", {"answers": []})
    answers = user_data['answers']
    correct_answers = [q['answer'] for q in PYTHON_QUESTION_LIST]

    score = sum(1 for user_ans, correct_ans in zip(answers, correct_answers) if user_ans == correct_ans)
    total_questions = len(correct_answers)

    return f"Quiz completed! Your score: {score}/{total_questions}"
