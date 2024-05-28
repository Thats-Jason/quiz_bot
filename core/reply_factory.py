from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST
def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0  # Start from the first question

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)
        next_question_id = None  # End the question sequence

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return False, "No current question."

    # Assuming answers are stored in a dictionary within the session
    answers = session.get("answers", {})
    answers[current_question_id] = answer
    session["answers"] = answers

    return True, ""

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0

    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, None

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answers", {})
    score = 0

    for question_id, answer in answers.items():
        correct_answer = get_correct_answer_for_question(question_id)
        if answer == correct_answer:
            score += 1

    result_message = f"Your final score is {score} out of {len(PYTHON_QUESTION_LIST)}."
    return result_message

def get_correct_answer_for_question(question_id):
    '''
    A mock function to get the correct answer for a question. This should be replaced
    with actual logic to fetch correct answers.
    '''
    # Example: Returning a dummy correct answer for simplicity
    correct_answers = {
        0: "correct_answer_1",
        1: "correct_answer_2",
        2: "correct_answer_3",
        # Add correct answers for all questions
    }

    return correct_answers.get(question_id, "")
