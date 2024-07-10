from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(session)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # Validate the answer (example validation)
    if not isinstance(answer, str) or not answer.strip():
        return False, "Invalid answer. Please provide a valid response."

    # Store the answer (example storage)
    user_data = session.get("user_data", {"answers": []})
    user_data['answers'].append(answer)
    session["user_data"] = user_data

    return True, None

def get_next_question(session):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    user_data = session.get("user_data", {"answers": []})
    questions = PYTHON_QUESTION_LIST

    # Determine the next question index
    current_index = len(user_data['answers'])
    if current_index >= len(questions):
        return None, None

    next_question = questions[current_index]
    next_question_id = current_index + 1
    return next_question, next_question_id

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_data = session.get("user_data", {"answers": []})
    answers = user_data['answers']
    correct_answers = [q['answer'] for q in PYTHON_QUESTION_LIST]

    # Calculate performance
    score = sum(1 for user_ans, correct_ans in zip(answers, correct_answers) if user_ans == correct_ans)
    total_questions = len(correct_answers)

    return f"Quiz completed! Your score: {score}/{total_questions}"
