import json
import re
from flask import jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_phone(phone):
    phone_regex = r'^\+?1?\d{9,15}$'
    return re.match(phone_regex, phone) is not None

def send_email(data):
    sender_email = "devamkathane.me@sbjit.edu.in"
    password = "nooneisyours42"
    receiver_email = sender_email  # Sending to self

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "New User Data from Chatbot"

    body = f"""
    New user data received:
    
    Name: {data.get('name', 'N/A')}
    Email: {data.get('email', 'N/A')}
    Phone: {data.get('phone', 'N/A')}
    Problem Statement: {data.get('problem_statement', 'N/A')}
    """

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_chat_response():
    try:
        user_message = request.json.get("message", "").lower()
        current_tag = request.json.get("current_tag", "start_conversation")
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
                        return jsonify({"response": response, "tag": response_tag, "options": options})
            
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
                send_email({"email": email})
                response = ["Thank you. Now, please provide your phone number."]
                response_tag = "collect_phone"
            else:
                response = ["The email address you provided is not valid. Please enter a valid email address."]
                response_tag = "collect_email"
            options = []

        elif current_tag == "collect_phone":
            phone = request.json.get("message", "")
            if is_valid_phone(phone):
                send_email({"phone": phone})
                response = ["Great. Could you please tell me your name?"]
                response_tag = "collect_name"
            else:
                response = ["The phone number you provided is not valid. Please enter a valid phone number."]
                response_tag = "collect_phone"
            options = []

        elif current_tag == "collect_name":
            name = request.json.get("message", "")
            send_email({"name": name})
            response = ["Thank you, " + name + ". Can you describe what help you want from us? Please provide your problem statement."]
            response_tag = "collect_problem_statement"
            options = []

        elif current_tag == "collect_problem_statement":
            problem_statement = request.json.get("message", "")
            send_email({"problem_statement": problem_statement})
            response = ["Thank you for providing your details. Our team will reach out to you shortly."]
            response_tag = "end_conversation"
            options = []

        elif current_tag == "end_conversation":
            response = ["Is there anything else I can help you with?"]
            options = [
                {"text": "Yes", "value": "start_conversation"},
                {"text": "No", "value": "close_chat"}
            ]
            response_tag = "offer_more_help"

        # Ensure response_tag is set for all pathways
        if not response_tag:
            response_tag = "unknown_tag"

        return jsonify({"response": response, "tag": response_tag, "options": options})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

# The rest of your code (if any) goes here
