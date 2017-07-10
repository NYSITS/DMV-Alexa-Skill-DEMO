from __future__ import print_function
import math
import random
import string


# ------- Skill specific business logic -------
GAME_LENGTH = 5
SKILL_NAME = "My DMV"

# When editing your questions pay attention to your punctuation.
# Make sure you use question marks or periods.

QUESTIONS = [
    {"While driving, when you see a triangular road sign, what must you do. 1, Reduce your speed and yield. 2, Come to a complete stop. 3, Increase your speed. 4, Make a right turn?": ["1"]},
    {"What must you do for an emergency vehicle if it is coming towards you with its lights flashing. 1, Slow down and move over to the left lane. 2, Increase your speed and clear the lane. 3, Pull over and stop. 4, Change your lane and proceed with the same speed?": ["3"]},
    {"What must you do if your tire goes flat while driving. 1, Press the brakes hard. 2, Hold the steering wheel firmly. 3, Put your foot on the gas pedal. 4, Press on the accelerator?": ["2"]},
    {"You may not make a U-turn 500 feet in either direction from what. 1, A construction zone. 2, An intersection. 3, The crest of a hill. 4, All of these?": ["3"]},
    {"When confronted by an aggressive driver while driving, how can you avoid conflict. 1, Stopping and getting out of your vehicle. 2, Using gestures. 3, Name calling. 4, Avoiding eye contact?": ["4"]},
    {"When you don't see a posted speed limit in New York City, what miles per hour must you drive at. 1, 55 or less. 2, 40 or less. 3, 50 or less. 4, 25 or less?": ["4"]},
    {"What rule is used to maintain a good space cushion between you and the vehicle in front of you. 1, Two-second rule. 2, Three-second rule. 3, Four-second rule. 4, One-second rule?": ["1"]},
    {"What must you do when another driver passes you on the left. 1, Pull over and stop. 2, Slow down slightly and keep to the left. 3, Slow down slightly and keep to the right. 4, Increase your speed and keep to the right?": ["3"]},
    {"If your rear wheels start to skid, you must do what. 1, Turn the steering wheel in the opposite direction of the skid. 2, Turn the steering wheel toward the left. 3, Turn the steering wheel toward the right. 4, Turn the steering wheel in the direction of the skid?": ["4"]},
    {"What method is used to turn around on a narrow, two-way street. 1, A three-point turn. 2, A single-point turn. 3, A four-point turn. 4, A two-point turn?": ["1"]},
    {"When must you not pass a vehicle on the right. 1, You are driving on a one-way road with two lanes of traffic. 2, The vehicle ahead is making a right turn. 3, Oncoming vehicles are not making a left turn. 4, The vehicle ahead is going straight?": ["2"]},
    {"What is the term when a vehicle's tires may begin to ride on the water lying on top of the road pavement when traveling at high speeds in heavy rain. 1, Waterplaining. 2, Weaving. 3, Tailgating. 4, Hydroplaning?": ["4"]},
    {"When must you not pass a vehicle from the left. 1, Your lane has a broken yellow center line. 2, Your lane has a solid yellow center line. 3, Your lane has a broken white line. 4, You are far from a curve?": ["2"]},
    {"What type of signs are yellow, diamond-shaped with black lettering or symbols. 1, Warning Signs. 2, Service Signs. 3, Regulatory Signs. 4, Destination Signs?": ["1"]},
    {"Your headlights must be on low-beam at night when you are within how many feet of an approaching vehicle. 1, 200 Feet. 2, 400 Feet. 3, 300 Feet. 4, 500 Feet?": ["4"]},
]


def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest, etc).
    The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID
    to prevent someone else from configuring a skill that sends requests
    to this function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """Called when the session starts."""
    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])


def on_launch(launch_request, session):
    """Called when the user launches the skill without specifying what they want."""
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill."""
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # handle yes/no intent after the user has been prompted
    if session.get('attributes', {}).get('user_prompted_to_continue'):
        del session['attributes']['user_prompted_to_continue']
        if intent_name == 'AMAZON.NoIntent':
            return handle_finish_session_request(intent, session)
        elif intent_name == "AMAZON.YesIntent":
            return handle_repeat_request(intent, session)

    # Dispatch to your skill's intent handlers
    if intent_name == "QuizIntent":
        return play_game(intent, session)
    elif intent_name == "WhatIsNewIntent":
        return handle_what_is_new_request(intent, session)
    elif intent_name == "MoreInfoIntent":
        return handle_more_info_request(intent, session)
    elif intent_name == "AnswerIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "ContinueIntent":
        return handle_continue_game_request(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.StartOverIntent":
        return play_game(intent, session)
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior -------------


def get_welcome_response():
    """If we wanted to initialize the session to have some attributes we could add those here."""
    text = "Welcome to the My DMV Alexa Skill. I can update you on new information regarding:  " \
           "Inspections, Registrations, and License Renewals.  " \
           "I can also quiz you for the written permit test.  " \
           "To find out new information you can say, what's new.  " \
           "Or to quiz yourself for the permit test say, quiz me.  " \
           "What would you like to do?  "

    spoken_question = None
    should_end_session = False
    
    speech_output = text
    attributes = {"speech_output": speech_output,
                  "reprompt_text": speech_output,
                  "spoken_question": spoken_question
                  }

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, spoken_question, should_end_session))

def handle_what_is_new_request(intent, session):
    text = "Your inspection for passenger plate, A B C 1 2 3, expired July 1.  " \
           "Your boat registration for, N Y 1 2 3 4 5, will expire on August 1.  " \
           "Your driver's license will expire next month, you are eligible to renew it online.  " \
           "If you would like more information regarding online license renewals, say more info.  " \
           "If not say stop or exit.  "

    spoken_question = None
    should_end_session = False

    speech_output = text
    attributes = {"speech_output": speech_output,
                  "reprompt_text": speech_output,
                  "spoken_question": spoken_question}

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, spoken_question, should_end_session))

def handle_more_info_request(intent, session):
    text = "To renew your license online follow these steps:  " \
           "Step 1, pass an eye test by an approved provider, like a pharmacy. Or have a professional complete a paper report.  " \
           "Step 2, follow the online renewal steps on the DMV website.  " \
           "Step 3, download and print a temporary license, in PDF format to use until your new license arrives.  " \
           "If you would like more in depth information, please visit the DMV website. Have a wonderful day!  "

    spoken_question = None
    should_end_session = True

    speech_output = text
    attributes = {"speech_output": speech_output,
                  "reprompt_text": speech_output,
                  "spoken_question": spoken_question}

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, spoken_question, should_end_session))

def play_game(intent, session):
    intro = ("Welcome to {}'s Practice Permit Test. ".format(SKILL_NAME) +
             "I will ask you {} questions. ".format(GAME_LENGTH) +
             "Try to get as many right as you can. Just say the number of the answer. Let's begin. ")
    should_end_session = False
    game_questions = populate_game_questions()
    starting_index = 0

    spoken_question = QUESTIONS[game_questions[starting_index]].keys()[0]

    speech_output = intro + spoken_question
    attributes = {"speech_output": speech_output,
                  "reprompt_text": spoken_question,
                  "current_questions_index": starting_index,
                  "questions": game_questions,
                  "score": 0,
                  "correct_answers": QUESTIONS[game_questions[starting_index]].values()[0]
                  }

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, spoken_question, should_end_session))

def handle_continue_game_request(intent, session):
    should_end_session = False
    game_questions = populate_game_questions()
    starting_index = 0

    spoken_question = QUESTIONS[game_questions[starting_index]].keys()[0]

    speech_output = spoken_question
    attributes = {"speech_output": speech_output,
                  "reprompt_text": spoken_question,
                  "current_questions_index": starting_index,
                  "questions": game_questions,
                  "score": 0,
                  "correct_answers": QUESTIONS[game_questions[starting_index]].values()[0]
                  }

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, spoken_question, should_end_session))


def populate_game_questions():
    game_questions = []
    index_list = []
    index = len(QUESTIONS)

    if GAME_LENGTH > index:
        raise ValueError("Invalid Game Length")

    for i in range(0, index):
        index_list.append(i)

    # Pick GAME_LENGTH random questions from the list to ask the user,
    # make sure there are no repeats
    for j in range(0, GAME_LENGTH):
        rand = int(math.floor(random.random() * index))
        index -= 1

        temp = index_list[index]
        index_list[index] = index_list[rand]
        index_list[rand] = temp
        game_questions.append(index_list[index])

    return game_questions


def handle_answer_request(intent, session):
    attributes = {}
    should_end_session = False
    answer = intent['slots'].get('Answer', {}).get('value')
    user_gave_up = intent['name']

    if 'attributes' in session.keys() and 'questions' not in session['attributes'].keys():
        # If the user responded with an answer but there is no game
        # in progress ask the user if they want to start a new game.
        # Set a flag to track that we've prompted the user.
        attributes['user_prompted_to_continue'] = True
        speech_output = "There is no quiz in progress. " \
                        "Do you want to start a new quiz?"
        reprompt_text = speech_output
        return build_response(attributes, build_speechlet_response(SKILL_NAME,
                              speech_output, reprompt_text, should_end_session))
    elif not answer and user_gave_up == "DontKnowIntent":
        # If the user provided answer isn't a number > 0 and < ANSWER_COUNT,
        # return an error message to the user. Remember to guide the user
        # into providing correct values.
        reprompt = session['attributes']['speech_output']
        speech_output = "I couldn't understand your answer, please try again " + reprompt
        return build_response(
            session['attributes'],
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))
    else:
        game_questions = session['attributes']['questions']
        current_score = session['attributes']['score']
        current_questions_index = session['attributes']['current_questions_index']
        correct_answers = session['attributes']['correct_answers']

        speech_output_analysis = None
        if answer and answer.lower() in map(string.lower, correct_answers):
            current_score += 1
            speech_output_analysis = "correct. "
        else:
            if user_gave_up != "DontKnowIntent":
                speech_output_analysis = "wrong. "
            speech_output_analysis = (speech_output_analysis +
                                      "The correct answer is " +
                                      correct_answers[0])

        # if current_questions_index is 4, we've reached 5 questions
        # (zero-indexed) and can exit the game session
        if current_questions_index == GAME_LENGTH - 1:
            speech_output = "" if intent['name'] == "DontKnowIntent" else "That answer is "
            speech_output = (speech_output + speech_output_analysis +
                             "You got {} out of {} correct. ".format(current_score, GAME_LENGTH) +
                             "To keep playing say continue. Or to exit say stop. ")
            reprompt_text = None
            should_end_session = False
            return build_response(
                session['attributes'],
                build_speechlet_response(
                    SKILL_NAME, speech_output, reprompt_text, should_end_session
                ))
        else:
            current_questions_index += 1
            spoken_question = QUESTIONS[game_questions[current_questions_index]].keys()[0]
            reprompt_text = spoken_question

            speech_output = "" if user_gave_up == "DontKnowIntent" else "That answer is "
            speech_output = (speech_output + speech_output_analysis +
                             "Your score is " +
                             str(current_score) + '. ' + reprompt_text)
            attributes = {"speech_output": speech_output,
                          "reprompt_text": reprompt_text,
                          "current_questions_index": current_questions_index,
                          "questions": game_questions,
                          "score": current_score,
                          "correct_answers": QUESTIONS[game_questions[current_questions_index]].values()[0]  # noqa
                          }

            return build_response(attributes,
                                  build_speechlet_response(SKILL_NAME, speech_output, reprompt_text,
                                                           should_end_session))


def handle_repeat_request(intent, session):
    """
    Repeat the previous speech_output and reprompt_text from the session['attributes'].
    If available, else start a new game session.
    """
    if 'attributes' not in session or 'speech_output' not in session['attributes']:
        return get_welcome_response()
    else:
        attributes = session['attributes']
        speech_output = attributes['speech_output']
        reprompt_text = attributes['reprompt_text']
        should_end_session = False
        return build_response(
            attributes,
            build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)
        )


def handle_get_help_request(intent, session):
    attributes = {}
    speech_output = ("You can say what's new to hear up to date information regarding the status of your inspections, registrations, and license renewals. " \
                     "Or you can say quiz me to test yourself for the written permit test. Rounds will consist of five questions and you can continue playing for as long as you would like. " \
                     "You can stop at any time. What can I help you with?")
    reprompt_text = speech_output
    should_end_session = False
    return build_response(
        attributes,
        build_speechlet_response(SKILL_NAME, speech_output, reprompt_text, should_end_session)
    )


def handle_finish_session_request(intent, session):
    """End the session with a message if the user wants to quit the game."""
    attributes = session['attributes']
    reprompt_text = None
    speech_output = "Thank you for using the {} Alexa Skill! Have a wonderful day!".format(SKILL_NAME)
    should_end_session = True
    return build_response(
        attributes,
        build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)
    )


def is_answer_slot_valid(intent):
    if 'Answer' in intent['slots'].keys() and 'value' in intent['slots']['Answer'].keys():
        return True
    else:
        return False


# --------------- Helpers that build all of the responses -----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }
