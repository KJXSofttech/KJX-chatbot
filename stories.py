import torch
import json
from flask import jsonify, request
from nltk_utils import tokenize, stem, bag_of_words

def get_chat_response(model, all_words, tags, professors_data):
    try:
        user_message = request.json.get("message", "")
        current_tag = request.json.get("current_tag", "start_conversation")
        response = []
        options = []

        if current_tag == "start_conversation":
            response = [
                "Hello! Welcome to AskToMentor! I'm here to help you find the perfect mentor.",
                "What kind of assistance are you looking for today?"
            ]
            options = [
                {"text": "Academic Help", "value": "academic"},
                {"text": "Career Guidance", "value": "career"},
                {"text": "Personal Development", "value": "personal"}
            ]
            response_tag = "select_category"

        elif current_tag == "select_category":
            if user_message.lower() == "academic":
                response = ["Great! You've selected Academic Help. What subject are you interested in?"]
                options = [
                    {"text": "Mathematics", "value": "mathematics"},
                    {"text": "Science", "value": "science"},
                    {"text": "Literature", "value": "literature"},
                    {"text": "History", "value": "history"},
                    {"text": "Computer Science", "value": "computer_science"},
                    {"text": "Other", "value": "other_subject"}
                ]
                response_tag = "select_academic_subject"
            elif user_message.lower() == "career":
                response = ["Excellent choice! For Career Guidance, what specific area are you interested in?"]
                options = [
                    {"text": "Interview Preparation", "value": "interview_prep"},
                    {"text": "Career Planning", "value": "career_planning"},
                    {"text": "Resume Building", "value": "resume_building"},
                    {"text": "Networking Skills", "value": "networking_skills"},
                    {"text": "Other", "value": "other_career"}
                ]
                response_tag = "select_career_area"
            elif user_message.lower() == "personal":
                response = ["Great! For Personal Development, what area would you like to focus on?"]
                options = [
                    {"text": "Time Management", "value": "time_management"},
                    {"text": "Stress Management", "value": "stress_management"},
                    {"text": "Goal Setting", "value": "goal_setting"},
                    {"text": "Confidence Building", "value": "confidence_building"},
                    {"text": "Communication Skills", "value": "communication_skills"},
                    {"text": "Other", "value": "other_personal"}
                ]
                response_tag = "select_personal_area"
            else:
                response = ["I'm sorry, I didn't understand your selection. Please choose one of the options provided."]
                options = [
                    {"text": "Academic Help", "value": "academic"},
                    {"text": "Career Guidance", "value": "career"},
                    {"text": "Personal Development", "value": "personal"}
                ]
                response_tag = "select_category"

        elif current_tag == "select_academic_subject":
            if user_message.lower() == "other_subject":
                response = ["Please type the subject you need help with:"]
                response_tag = "manual_subject_entry"
            else:
                matched_professors = [prof for prof in professors_data if prof['Subject'].lower() == user_message.lower()]
                if matched_professors:
                    response = [f"Great! Here are some mentors available for {user_message}:"]
                    for prof in matched_professors[:2]:  # Show only 2 professors
                        response.append(f"{prof['Name']}, {prof['Experience']} of experience, based in {prof['Geography']}")
                    if len(matched_professors) > 2:
                        options.append({"text": "Show more mentors", "value": "show_more_mentors"})
                    response.append("Would you like to be matched with one of these mentors?")
                    options.append({"text": "Yes, match me!", "value": "match_mentor"})
                    options.append({"text": "No, I have more questions", "value": "more_questions"})
                    response_tag = "mentor_matching"
                else:
                    response = [f"I'm sorry, we couldn't find any mentors for {user_message} at the moment. Would you like to try a different subject?"]
                    options = [
                        {"text": "Yes, show me subjects again", "value": "academic"},
                        {"text": "No, I have more questions", "value": "more_questions"}
                    ]
                    response_tag = "select_category"

        elif current_tag == "select_career_area" or current_tag == "select_personal_area":
            if user_message.lower() in ["other_career", "other_personal"]:
                response = ["Please specify the area you need help with:"]
                response_tag = "manual_subject_entry"
            else:
                career_personal_professors = [prof for prof in professors_data if prof['Profession'] in [
                    "Career Counselor", "Career Coach", "Career Planner", "Career Advisor", 
                    "Personal Development Coach", "Life Coach"
                ]]
                
                if career_personal_professors:
                    response = [f"Great! You've selected {user_message}. Here are some mentors who can help you:"]
                    for prof in career_personal_professors[:2]:  # Show only 2 professors
                        response.append(f"{prof['Name']}, {prof['Profession']}, {prof['Experience']} of experience, based in {prof['Geography']}")
                    if len(career_personal_professors) > 2:
                        options.append({"text": "Show more mentors", "value": "show_more_mentors"})
                    response.append("Would you like to be matched with one of these mentors?")
                    options.append({"text": "Yes, match me!", "value": "match_mentor"})
                    options.append({"text": "No, I have more questions", "value": "more_questions"})
                    response_tag = "mentor_matching"
                else:
                    response = ["I'm sorry, we couldn't find any mentors for this area at the moment. Would you like to explore other options?"]
                    options = [
                        {"text": "Yes, show me other options", "value": "select_category"},
                        {"text": "No, I have more questions", "value": "more_questions"}
                    ]
                    response_tag = "select_category"

        elif current_tag == "manual_subject_entry":
            matched_professors = [prof for prof in professors_data if prof['Subject'].lower() == user_message.lower()]
            if matched_professors:
                response = [f"Great! Here are some mentors available for {user_message}:"]
                for prof in matched_professors[:2]:  # Show only 2 professors
                    response.append(f"{prof['Name']}, {prof['Experience']} of experience, based in {prof['Geography']}")
                if len(matched_professors) > 2:
                    options.append({"text": "Show more mentors", "value": "show_more_mentors"})
                response.append("Would you like to be matched with one of these mentors?")
                options.append({"text": "Yes, match me!", "value": "match_mentor"})
                options.append({"text": "No, I have more questions", "value": "more_questions"})
                response_tag = "mentor_matching"
            else:
                response = [f"I'm sorry, we couldn't find any mentors for {user_message}. Would you like to try a different subject?"]
                options = [
                    {"text": "Yes, show me subjects again", "value": "academic"},
                    {"text": "No, I have more questions", "value": "more_questions"}
                ]
                response_tag = "select_category"

        elif current_tag == "mentor_matching":
            if user_message.lower() == "match_mentor":
                response = ["Excellent! I'll start the process to match you with a mentor.",
                            "To help me find the best match, could you tell me your preferred mentoring style?"]
                options = [
                    {"text": "Hands-on guidance", "value": "hands_on"},
                    {"text": "General advice and direction", "value": "general_advice"},
                    {"text": "Mix of both", "value": "mixed_style"}
                ]
                response_tag = "mentoring_style"
            elif user_message.lower() == "more_questions":
                response = ["Sure, I'm here to help! I am here to help you, ask me what you want to know about our mentoring program?"]
                response_tag = "open_questions"
            elif user_message.lower() == "show_more_mentors":
                # Handle showing more mentors here
                response = ["Here are more mentors for you:"]
                if current_tag == "select_academic_subject" or current_tag == "manual_subject_entry":
                    matched_professors = [prof for prof in professors_data if prof['Subject'].lower() == user_message.lower()]
                else:
                    matched_professors = [prof for prof in professors_data if prof['Profession'] in [
                        "Career Counselor", "Career Coach", "Career Planner", "Career Advisor", 
                        "Personal Development Coach", "Life Coach"
                    ]]
                for prof in matched_professors[:4]:  # Show next 2 professors
                    response.append(f"{prof['Name']}, {prof['Experience']} of experience, based in {prof['Geography']}")
                if len(matched_professors) > 4:
                    options.append({"text": "Show more mentors", "value": "show_more_mentors"})
                response.append("Would you like to be matched with one of these mentors?")
                options.append({"text": "Yes, match me!", "value": "match_mentor"})
                options.append({"text": "No, I have more questions", "value": "more_questions"})
                response_tag = "mentor_matching"
            else:
                response = ["I'm sorry, I didn't understand your selection. Please choose one of the options provided."]
                options = [
                    {"text": "Yes, match me!", "value": "match_mentor"},
                    {"text": "No, I have more questions", "value": "more_questions"}
                ]
                response_tag = "mentor_matching"

        elif current_tag == "mentoring_style":
            response = ["Thank you for providing your preferred mentoring style. A suitable mentor will contact you shortly to discuss your needs in more detail."]
            options = [
                {"text": "Close Chat", "value": "close_chat"},
                {"text": "Ask More Questions", "value": "ask_more_questions"}
            ]
            response_tag = "end_conversation"

        else:
            # If the tag is not handled above, use the neural network to predict the response
            sentence = tokenize(user_message)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).float()

            output = model(X)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            # Get the corresponding intent and responses
            with open('intents.json', 'r') as json_data:
                intents = json.load(json_data)

            for intent in intents['intents']:
                if tag == intent['tag']:
                    response = intent['responses']
                    break

            response_tag = tag

        return jsonify({"response": response, "tag": response_tag, "options": options})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
