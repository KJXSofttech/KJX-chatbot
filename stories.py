import json
import re
from flask import request
import certifi
from pymongo import MongoClient
import urllib.parse

# MongoDB connection setup
username = urllib.parse.quote_plus("kjxsofttechpvtltd")
password = urllib.parse.quote_plus("KJXSOFTTECH123")
connection_string = f"mongodb+srv://{username}:{password}@kjxwebsite.3mup0.mongodb.net/?retryWrites=true&w=majority&appName=kjxwebsite&tls=true&tlsAllowInvalidCertificates=true"

client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client['KJXWebsite']  # Use your actual database name
collection = db['Users data']  # Use your actual collection name

def save_user_data(data):
    try:
        result = collection.insert_one(data)
        print("User data saved successfully to MongoDB")
        return str(result.inserted_id)  # Convert ObjectId to string
    except Exception as e:
        print(f"Error saving user data to MongoDB: {e}")
        return None
    
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_phone(phone):
    phone_regex = r'^\+?1?\d{9,15}$'
    return re.match(phone_regex, phone) is not None

def get_chat_response():
    try:
        user_message = request.json.get("message", "").lower()
        current_tag = request.json.get("current_tag", "start_conversation")
        user_data = request.json.get("user_data", {})  # Fetch user_data from request if it exists

        print(f"Received user_data: {user_data}")  # Debug log

        response = []
        options = []
        response_tag = None

        categories = {
            "ml_data_science": {
                "name": "Machine Learning and Data Science",
                "subcategories": {
                    "predictive_analytics": "Predictive Analytics uses historical data to forecast future trends.",
                    "data_modeling": "Data Modeling creates visual representations of data structures.",
                    "algorithm_development": "Algorithm Development involves creating custom algorithms to solve specific problems."
                }
            },
            "ai": {
                "name": "AI",
                "subcategories": {
                    "custom_ai_solutions": "Custom AI Solutions are tailored to meet specific business needs.",
                    "ml_model_development": "Machine Learning Model Development creates models that learn from data.",
                    "ai_consulting": "AI Consulting helps integrate AI into your business strategy.",
                    "chatbot_development": "Chatbot Development creates intelligent conversational interfaces."
                }
            },
            "ui_ux": {
                "name": "UI/UX Development",
                "subcategories": {
                    "ui_design": "User Interface Design focuses on the look and feel of your application.",
                    "ux_research": "User Experience Research involves understanding user behavior to improve usability.",
                    "prototyping_wireframing": "Prototyping and Wireframing help visualize the application before development."
                }
            },
            "data_visualization": {
                "name": "Data Visualization",
                "subcategories": {
                    "dashboard_development": "Dashboard Development creates interactive data dashboards.",
                    "data_storytelling": "Data Storytelling presents data in a narrative format.",
                    "visualization_consulting": "Visualization Consulting helps choose the right visualization techniques."
                }
            },
            "iot_cloud": {
                "name": "IoT & Cloud Services",
                "subcategories": {
                    "cloud_integration": "Cloud Integration connects various cloud services.",
                    "iot_device_management": "IoT Device Management involves managing and monitoring IoT devices.",
                    "cloud_security": "Cloud Security protects data and applications in the cloud."
                }
            },
            "devops": {
                "name": "DevOps",
                "subcategories": {
                    "ci_cd": "CI/CD (Continuous Integration/Continuous Delivery) automates software delivery processes.",
                    "infrastructure_as_code": "Infrastructure as Code (IaC) manages infrastructure through code.",
                    "monitoring_logging": "Monitoring and Logging tracks application performance and logs events."
                }
            },
            "custom_software": {
                "name": "Custom Software Development",
                "subcategories": {
                    "software_consulting": "Software Consulting provides expert advice on software solutions.",
                    "enterprise_app_development": "Enterprise Application Development creates custom applications for businesses.",
                    "maintenance_support": "Maintenance and Support provides ongoing software maintenance."
                }
            },
            "e_commerce": {
                "name": "E-commerce Development",
                "subcategories": {
                    "ecommerce_website_development": "E-commerce Website Development creates online stores.",
                    "payment_gateway_integration": "Payment Gateway Integration connects payment systems to your website.",
                    "ecommerce_consulting": "E-commerce Consulting provides expert advice on e-commerce strategies."
                }
            }
        }

        industries = {
            "banking_finance": "Banking & Finance solutions include Financial Analytics, Risk Management Systems, and Blockchain Solutions.",
            "healthcare": "Healthcare solutions include Health Data Analytics, Hospital Management Systems, Telemedicine Solutions, and AI-based Diagnostic Tools.",
            "government": "Government sector solutions include E-governance Solutions, Data Analytics for Policy Making, and Citizen Engagement Platforms.",
            "travel_hospitality": "Travel & Hospitality solutions include Booking and Reservation Systems, Customer Experience Management, and Travel Data Analytics.",
            "automotive": "Automotive industry solutions include Vehicle Telematics, Predictive Maintenance, and Autonomous Driving Solutions.",
            "media_entertainment": "Media & Entertainment solutions include Content Management Systems, Audience Analytics, and Digital Rights Management.",
            "real_estate": "Real Estate solutions include Property Management Systems, Real Estate Analytics, and Virtual Tours and Visualization.",
            "investment": "Investment sector solutions include Portfolio Management Systems, Investment Analytics, and Risk Assessment Tools.",
            "e_learning": "E-learning solutions include Learning Management Systems, E-learning Content Development, and Virtual Classroom Solutions.",
            "transportation": "Transportation solutions include Fleet Management Systems, Transportation Analytics, and Route Optimization.",
            "e_commerce_industry": "E-commerce industry solutions include E-commerce Platform Development, Online Payment Solutions, and Customer Analytics.",
            "technical_services": "Technical Services include IT Support and Maintenance, Technical Consulting, and System Integration."
        }

        if current_tag == "start_conversation":
            response = [
                "Welcome to KJX Softtech! How can we assist you today? Here are some options to get started:",
            ]
            options = [
                {"text": "Learn about our services", "value": "learn_services"},
                {"text": "Explore the industries we serve", "value": "explore_industries"},
                {"text": "Know why to choose us", "value": "know_why"}
            ]
            response_tag = "select_category"

        elif current_tag == "select_category":
            if user_message == "learn_services":
                response = ["We offer a wide range of services to cater to your needs. Please choose a category to learn more:"]
                options = [{"text": cat_info["name"], "value": cat} for cat, cat_info in categories.items()]
                response_tag = "select_service_category"
            elif user_message == "explore_industries":
                response = ["We have experience in various industries. Please choose an industry to learn more:"]
                options = [{"text": industry.replace('_', ' ').title(), "value": industry} for industry in industries.keys()]
                response_tag = "select_industry_category"
            elif user_message == "know_why":
                response = [
                    "Here's why KJX Softtech stands out:",
                    "- **Fast Service:** We are committed to completing projects as quickly and accurately as possible.",
                    "- **Pocket-friendly:** We offer the greatest service at a reasonable price.",
                    "- **Global Enterprise Development:** Our focus is on advancing your business on a worldwide scale.",
                    "Would you like to contact us for more details?"
                ]
                options = [
                    {"text": "Yes", "value": "yes"},
                    {"text": "No", "value": "no"}
                ]
                response_tag = "contact_us"

        elif current_tag == "select_service_category":
            if user_message in categories:
                response = [f"In {categories[user_message]['name']}, we offer the following services:"]
                options = [{"text": subcat.replace('_', ' ').title(), "value": f"{user_message}_{subcat}"} for subcat in categories[user_message]['subcategories'].keys()]
                response_tag = "select_service_subcategory"
            else:
                response = ["I'm sorry, I didn't understand that. Could you please choose from the options provided?"]
                response_tag = current_tag

        elif current_tag == "select_service_subcategory":
            for category, cat_info in categories.items():
                for subcategory in cat_info['subcategories'].keys():
                    if user_message.lower() == f"{category}_{subcategory}":
                        response = [
                            f"{subcategory.replace('_', ' ').title()}: {cat_info['subcategories'][subcategory]}",
                            "Would you like to know more or need help with this service?"
                        ]
                        options = [
                            {"text": "Yes", "value": "yes"},
                            {"text": "No", "value": "no"}
                        ]
                        response_tag = f"{category}_{subcategory}_services"
                        return {
                            "response": response,
                            "tag": response_tag,
                            "options": options,
                            "user_data": user_data
                        }
            
            response = ["I'm sorry, I didn't understand that. Could you please choose from the options provided?"]
            response_tag = "select_service_category"

        elif current_tag == "select_industry_category":
            if user_message in industries:
                response = [
                    f"{user_message.replace('_', ' ').title()}: {industries[user_message]}",
                    "Would you like to know more or need help with solutions for this industry?"
                ]
                options = [
                    {"text": "Yes", "value": "yes"},
                    {"text": "No", "value": "no"}
                ]
                response_tag = f"{user_message}_industry"
            else:
                response = ["I'm sorry, I didn't understand that. Could you please choose from the options provided?"]
                response_tag = current_tag

        elif current_tag.endswith("_services") or current_tag.endswith("_industry") or current_tag == "contact_us":
            if user_message == "yes":
                response = ["Great! Please provide your email."]
                response_tag = "collect_email"
                options = []
            elif user_message == "no":
                response = ["Thank you for your interest. Is there anything else I can help you with?"]
                options = [
                    {"text": "Yes", "value": "start_conversation"},
                    {"text": "No", "value": "end_conversation"}
                ]
                response_tag = "offer_more_help"

        elif current_tag == "collect_email":
            email = request.json.get("message", "")
            if is_valid_email(email):
                user_data['email'] = email
                print(f"Email added: {user_data}")  # Debug log
                response = ["Thank you. Now, please provide your phone number."]
                response_tag = "collect_phone"
            else:
                response = ["The email address you provided is not valid. Please enter a valid email address."]
                response_tag = "collect_email"
            options = []

        elif current_tag == "collect_phone":
            phone = request.json.get("message", "")
            if is_valid_phone(phone):
                user_data['phone'] = phone
                print(f"Phone added: {user_data}")  # Debug log
                response = ["Great. Could you please tell me your name?"]
                response_tag = "collect_name"
            else:
                response = ["The phone number you provided is not valid. Please enter a valid phone number."]
                response_tag = "collect_phone"
            options = []

        elif current_tag == "collect_name":
            name = request.json.get("message", "")
            user_data['name'] = name
            print(f"Name added: {user_data}")  # Debug log
            response = ["Thank you, " + name + ". Can you describe what help you want from us? Please provide your problem statement."]
            response_tag = "collect_problem_statement"
            options = []

        elif current_tag == "collect_problem_statement":
            problem_statement = request.json.get("message", "")
            user_data['problem_statement'] = problem_statement
            print(f"Problem statement added: {user_data}")  # Debug log
            
            # Check only for missing fields
            required_fields = ['name', 'email', 'phone', 'problem_statement']
            missing_fields = [field for field in required_fields if field not in user_data]
            
            if missing_fields:
                response = [f"Some information is missing. Please provide: {', '.join(missing_fields)}"]
                response_tag = f"collect_{'_'.join(missing_fields)}"
            else:
                result_id = save_user_data(user_data)  # Save all user data to MongoDB
                if result_id:
                    response = [f"Thank you for providing your details. Our team will reach out to you shortly. Your reference ID is {result_id}."]
                else:
                    response = ["There was an issue saving your data, please try again later."]
                response_tag = "end_conversation"
            
            options = []

        # Ensure response_tag is set for all pathways
        if not response_tag:
            response_tag = "unknown_tag"

        print(f"Sending user_data: {user_data}")  # Debug log
        return {
            "response": response,
            "tag": response_tag,
            "options": options,
            "user_data": user_data
        }

    except Exception as e:
        print(f"Error in get_chat_response: {e}")  # Debug log
        return {"error": f"An error occurred: {str(e)}"}