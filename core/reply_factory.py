
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    question  = PYTHON_QUESTION_LIST[current_question_id]
    if question['answer'] == answer:
        is_correct = True
    else:
        is_correct = False
    session['answer'][current_question_id] = {'answer':answer, 'correct':is_correct}
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id + 1 < len(PYTHON_QUESTION_LIST):
        next_question_id = current_question_id +1
        next_question = PYTHON_QUESTION_LIST[next_question_id]
        return next_question, -1'
    else:
        return "no more question ",-1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answer = session['answer']
    total_questions  = len(PYTHON_QUESTION_LIST)
    currect_answer = sum(1 for answer in answer.values() if answer['correct'])
    score = (correct_answer / total_questions)* 100
    result = f"Your final score is {score:.2f}%. You answered {correct_answer} out of {total_questions} question correctly."
    return result
