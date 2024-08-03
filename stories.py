import json
from flask import jsonify, request

def save_user_data(data):
    try:
        with open('user_data.json', 'a') as f:
            json.dump(data, f)
            f.write("\n")
    except Exception as e:
        print(f"Error saving user data: {e}")

def get_chat_response(all_words, tags, professors_data):
    try:
        user_message = request.json.get("message", "").lower()
        current_tag = request.json.get("current_tag", "start_conversation")
        response = []
        options = []

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
                options = [
                    {"text": "Machine Learning and Data Science", "value": "ml_data_science"},
                    {"text": "AI", "value": "ai"},
                    {"text": "UI/UX Development", "value": "ui_ux"},
                    {"text": "Data Visualization", "value": "data_visualization"},
                    {"text": "IoT & Cloud Services", "value": "iot_cloud"},
                    {"text": "DevOps", "value": "devops"},
                    {"text": "Custom Software Development", "value": "custom_software"},
                    {"text": "E-commerce Development", "value": "e_commerce"}
                ]
                response_tag = "select_service_category"
            elif user_message == "explore_industries":
                response = ["We have experience in various industries. Please choose an industry to learn more:"]
                options = [
                    {"text": "Banking & Finance", "value": "banking_finance"},
                    {"text": "Healthcare", "value": "healthcare"},
                    {"text": "Government", "value": "government"},
                    {"text": "Travel & Hospitality", "value": "travel_hospitality"},
                    {"text": "Automotive", "value": "automotive"},
                    {"text": "Media & Entertainment", "value": "media_entertainment"},
                    {"text": "Real Estate", "value": "real_estate"},
                    {"text": "Investment", "value": "investment"},
                    {"text": "E-learning", "value": "e_learning"},
                    {"text": "Transportation", "value": "transportation"},
                    {"text": "E-commerce", "value": "e_commerce_industry"},
                    {"text": "Technical Services", "value": "technical_services"}
                ]
                response_tag = "select_industry_category"
            elif user_message == "know_why":
                response = [
                    "Here’s why KJX Softtech stands out:",
                    "- **Fast Service:** We are committed to completing projects as quickly and accurately as possible.",
                    "- **Pocket-friendly:** We offer the greatest service at a reasonable price.",
                    "- **Global Enterprise Development:** Our focus is on advancing your business on a worldwide scale.",
                    "Would you like to explore our services, industries, or contact us for more details?"
                ]
                options = [
                    {"text": "Learn about our services", "value": "learn_services"},
                    {"text": "Explore the industries we serve", "value": "explore_industries"},
                    {"text": "Contact us", "value": "contact_us"}
                ]
                response_tag = "know_why"

        elif current_tag == "select_service_category":
            if user_message == "ml_data_science":
                response = [
                    "Our Machine Learning and Data Science services include:",
                    "- Predictive Analytics",
                    "- Data Modeling",
                    "- Algorithm Development",
                    "Would you like to know more about a specific service?"
                ]
                options = [
                    {"text": "Predictive Analytics", "value": "predictive_analytics"},
                    {"text": "Data Modeling", "value": "data_modeling"},
                    {"text": "Algorithm Development", "value": "algorithm_development"}
                ]
                response_tag = "ml_data_science_services"
            elif user_message == "ai":
                response = [
                    "Our AI services include:",
                    "Select specific service you want to know about:"
                ]
                options = [
                    {"text": "Custom AI Solutions", "value": "custom_ai_solutions"},
                    {"text": "Machine Learning Model Development", "value": "ml_model_development"},
                    {"text": "AI Consulting", "value": "ai_consulting"},
                    {"text": "Chatbot Development", "value": "chatbot_development"}
                ]
                response_tag = "ai_services"
            elif user_message == "ui_ux":
                response = [
                    "Our UI/UX Development services include:",
                    "Select specific UI/UX service you want to know about"
                ]
                options = [
                    {"text": "User Interface Design", "value": "ui_design"},
                    {"text": "User Experience Research", "value": "ux_research"},
                    {"text": "Prototyping and Wireframing", "value": "prototyping_wireframing"}
                ]
                response_tag = "ui_ux_services"
            elif user_message == "data_visualization":
                response = [
                    "Our Data Visualization services include:",
                    "Would you like to know more about a specific Data Visualization service?"
                ]
                options = [
                    {"text": "Dashboard Development", "value": "dashboard_development"},
                    {"text": "Data Storytelling", "value": "data_storytelling"},
                    {"text": "Visualization Consulting", "value": "visualization_consulting"}
                ]
                response_tag = "data_visualization_services"
            elif user_message == "iot_cloud":
                response = [
                    "Our IoT & Cloud Services include:",
                ]
                options = [
                    {"text": "Cloud Integration", "value": "cloud_integration"},
                    {"text": "IoT Device Management", "value": "iot_device_management"},
                    {"text": "Cloud Security", "value": "cloud_security"}
                ]
                response_tag = "iot_cloud_services"
            elif user_message == "devops":
                response = [
                    "Our DevOps services include:",
                    "Would you like to know more about a specific DevOps service?"
                ]
                options = [
                    {"text": "CI/CD", "value": "ci_cd"},
                    {"text": "Infrastructure as Code (IaC)", "value": "infrastructure_as_code"},
                    {"text": "Monitoring and Logging", "value": "monitoring_logging"}
                ]
                response_tag = "devops_services"
            elif user_message == "custom_software":
                response = [
                    "Our Custom Software Development services include:",
                    "Would you like to know more about a specific Custom Software Development?"
                ]
                options = [
                    {"text": "Software Consulting", "value": "software_consulting"},
                    {"text": "Enterprise Application Development", "value": "enterprise_app_development"},
                    {"text": "Maintenance and Support", "value": "maintenance_support"}
                ]
                response_tag = "custom_software_services"
            elif user_message == "e_commerce":
                response = [
                    "Our E-commerce Development services include:",
                    "Would you like to know more about a specific E-commerce Development?"
                ]
                options = [
                    {"text": "E-commerce Website Development", "value": "ecommerce_website_development"},
                    {"text": "Payment Gateway Integration", "value": "payment_gateway_integration"},
                    {"text": "E-commerce Consulting", "value": "ecommerce_consulting"}
                ]
                response_tag = "e_commerce_services"

        elif current_tag == "select_industry_category":
            if user_message == "banking_finance":
                response = [
                    "In the Banking & Finance industry, we provide solutions such as:",
                    "Would you like to know more about our work in Banking & Finance?"
                ]
                options = [
                    {"text": "Financial Analytics", "value": "financial_analytics"},
                    {"text": "Risk Management Systems", "value": "risk_management"},
                    {"text": "Blockchain Solutions", "value": "blockchain_solutions"}
                ]
                response_tag = "banking_finance_services"
            elif user_message == "healthcare":
                response = [
                    "In the Healthcare industry, we provide solutions such as:",
                ]
                options = [
                    {"text": "Health Data Analytics", "value": "health_data_analytics"},
                    {"text": "Hospital Management Systems", "value": "hospital_management"},
                    {"text": "Telemedicine Solutions", "value": "telemedicine_solutions"},
                    {"text": "AI-based Diagnostic Tools", "value": "ai_diagnostic_tools"}
                ]
                response_tag = "healthcare_services"
            elif user_message == "government":
                response = [
                    "In the Government sector, we provide solutions such as:",
                ]
                options = [
                    {"text": "E-governance Solutions", "value": "e_governance"},
                    {"text": "Data Analytics for Policy Making", "value": "policy_data_analytics"},
                    {"text": "Citizen Engagement Platforms", "value": "citizen_engagement"}
                ]
                response_tag = "government_services"
            elif user_message == "travel_hospitality":
                response = [
                    "In the Travel & Hospitality industry, we provide solutions such as:"
                ]
                options = [
                    {"text": "Booking and Reservation Systems", "value": "booking_reservation"},
                    {"text": "Customer Experience Management", "value": "customer_experience"},
                    {"text": "Travel Data Analytics", "value": "travel_data_analytics"}
                ]
                response_tag = "travel_hospitality_services"
            elif user_message == "automotive":
                response = [
                    "In the Automotive industry, we provide solutions such as:",
                    "Would you like to know more about our work in Automotive?"
                ]
                options = [
                    {"text": "Vehicle Telematics", "value": "vehicle_telematics"},
                    {"text": "Predictive Maintenance", "value": "predictive_maintenance"},
                    {"text": "Autonomous Driving Solutions", "value": "autonomous_driving"}
                ]
                response_tag = "automotive_services"
            elif user_message == "media_entertainment":
                response = [
                    "In the Media & Entertainment industry, we provide solutions such as:",
                ]
                options = [
                    {"text": "Content Management Systems", "value": "content_management"},
                    {"text": "Audience Analytics", "value": "audience_analytics"},
                    {"text": "Digital Rights Management", "value": "digital_rights"}
                ]
                response_tag = "media_entertainment_services"
            elif user_message == "real_estate":
                response = [
                    "In the Real Estate industry, we provide solutions such as:",
                ]
                options = [
                    {"text": "Property Management Systems", "value": "property_management"},
                    {"text": "Real Estate Analytics", "value": "real_estate_analytics"},
                    {"text": "Virtual Tours and Visualization", "value": "virtual_tours"}
                ]
                response_tag = "real_estate_services"
            elif user_message == "investment":
                response = [
                    "In the Investment sector, we provide solutions such as:",
                ]
                options = [
                    {"text": "Portfolio Management Systems", "value": "portfolio_management"},
                    {"text": "Investment Analytics", "value": "investment_analytics"},
                    {"text": "Risk Assessment Tools", "value": "risk_assessment"}
                ]
                response_tag = "investment_services"
            elif user_message == "e_learning":
                response = [
                    "In the E-learning industry, we provide solutions such as:",
                ]
                options = [
                    {"text": "Learning Management Systems", "value": "lms"},
                    {"text": "E-learning Content Development", "value": "elearning_content"},
                    {"text": "Virtual Classroom Solutions", "value": "virtual_classroom"}
                ]
                response_tag = "e_learning_services"
            elif user_message == "transportation":
                response = [
                    "In the Transportation industry, we provide solutions such as:",
                ]
                options = [
                    {"text": "Fleet Management Systems", "value": "fleet_management"},
                    {"text": "Transportation Analytics", "value": "transportation_analytics"},
                    {"text": "Route Optimization", "value": "route_optimization"}
                ]
                response_tag = "transportation_services"
            elif user_message == "e_commerce_industry":
                response = [
                    "In the E-commerce industry, we provide solutions such as:",
                ]
                options = [
                    {"text": "E-commerce Platform Development", "value": "ecommerce_platform"},
                    {"text": "Online Payment Solutions", "value": "online_payment"},
                    {"text": "Customer Analytics", "value": "customer_analytics"}
                ]
                response_tag = "e_commerce_industry_services"
            elif user_message == "technical_services":
                response = [
                    "In the Technical Services sector, we provide solutions such as:",
                ]
                options = [
                    {"text": "IT Support and Maintenance", "value": "it_support"},
                    {"text": "Technical Consulting", "value": "technical_consulting"},
                    {"text": "System Integration", "value": "system_integration"}
                ]
                response_tag = "technical_services"

        elif current_tag == "ml_data_science_services":
            if user_message == "predictive_analytics":
                response = [
                    "Predictive Analytics helps you forecast future trends based on historical data. Would you like to know more or need help with Predictive Analytics?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "data_modeling":
                response = [
                    "Data Modeling involves creating a visual representation of the data structure. Would you like to know more or need help with Data Modeling?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "algorithm_development":
                response = [
                    "Algorithm Development involves designing algorithms to solve specific problems. Would you like to know more or need help with Algorithm Development?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "ai_services":
            if user_message == "custom_ai_solutions":
                response = [
                    "Custom AI Solutions are tailored to meet your specific business needs. Would you like to know more or need help with Custom AI Solutions?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "ml_model_development":
                response = [
                    "Machine Learning Model Development involves creating models that learn from data. Would you like to know more or need help with Machine Learning Model Development?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "ai_consulting":
                response = [
                    "AI Consulting helps you integrate AI into your business strategy. Would you like to know more or need help with AI Consulting?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "chatbot_development":
                response = [
                    "Chatbot Development involves creating intelligent chatbots for customer interaction. Would you like to know more or need help with Chatbot Development?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "ui_ux_services":
            if user_message == "ui_design":
                response = [
                    "User Interface Design focuses on the look and feel of your application. Would you like to know more or need help with User Interface Design?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "ux_research":
                response = [
                    "User Experience Research involves understanding user behavior to improve usability. Would you like to know more or need help with User Experience Research?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "prototyping_wireframing":
                response = [
                    "Prototyping and Wireframing help in visualizing the application before development. Would you like to know more or need help with Prototyping and Wireframing?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "data_visualization_services":
            if user_message == "dashboard_development":
                response = [
                    "Dashboard Development involves creating interactive dashboards to visualize data. Would you like to know more or need help with Dashboard Development?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "data_storytelling":
                response = [
                    "Data Storytelling involves presenting data in a way that tells a story. Would you like to know more or need help with Data Storytelling?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "visualization_consulting":
                response = [
                    "Visualization Consulting helps you choose the right visualization techniques for your data. Would you like to know more or need help with Visualization Consulting?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "iot_cloud_services":
            if user_message == "cloud_integration":
                response = [
                    "Cloud Integration involves connecting various cloud services. Would you like to know more or need help with Cloud Integration?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "iot_device_management":
                response = [
                    "IoT Device Management involves managing and monitoring IoT devices. Would you like to know more or need help with IoT Device Management?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "cloud_security":
                response = [
                    "Cloud Security involves protecting data and applications in the cloud. Would you like to know more or need help with Cloud Security?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "devops_services":
            if user_message == "ci_cd":
                response = [
                    "CI/CD involves continuous integration and continuous delivery of code. Would you like to know more or need help with CI/CD?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "infrastructure_as_code":
                response = [
                    "Infrastructure as Code (IaC) involves managing infrastructure through code. Would you like to know more or need help with Infrastructure as Code?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "monitoring_logging":
                response = [
                    "Monitoring and Logging involves tracking application performance and logging events. Would you like to know more or need help with Monitoring and Logging?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "custom_software_services":
            if user_message == "software_consulting":
                response = [
                    "Software Consulting involves advising on software solutions. Would you like to know more or need help with Software Consulting?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "enterprise_app_development":
                response = [
                    "Enterprise Application Development involves creating applications for businesses. Would you like to know more or need help with Enterprise Application Development?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "maintenance_support":
                response = [
                    "Maintenance and Support involves providing ongoing support for software. Would you like to know more or need help with Maintenance and Support?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "e_commerce_services":
            if user_message == "ecommerce_website_development":
                response = [
                    "E-commerce Website Development involves creating online stores. Would you like to know more or need help with E-commerce Website Development?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "payment_gateway_integration":
                response = [
                    "Payment Gateway Integration involves connecting payment gateways to your website. Would you like to know more or need help with Payment Gateway Integration?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"
            elif user_message == "ecommerce_consulting":
                response = [
                    "E-commerce Consulting involves advising on e-commerce strategies. Would you like to know more or need help with E-commerce Consulting?"
                ]
                options = [
                    {"text": "Yes", "value": "ask_problem_statement"},
                    {"text": "No", "value": "thank_you"}
                ]
                response_tag = "ask_problem_statement"

        elif current_tag == "thank_you":
            response = [
                "Thank you so much! You can check our website for more details."
            ]
            response_tag = "end_conversation"
            options = []

        elif current_tag == "ask_problem_statement":
            response = [
                "Can you describe what help do you want from us? Please provide your problem statement."
            ]
            response_tag = "get_contact_details"
            options = []

        elif current_tag == "get_contact_details":
            problem_statement = request.json.get("message", "")
            response = [
                "Please provide your name."
            ]
            response_tag = "collect_name"
            options = []
            save_user_data({"problem_statement": problem_statement})

        elif current_tag == "collect_name":
            name = request.json.get("message", "")
            response = [
                "Please provide your email."
            ]
            response_tag = "collect_email"
            options = []
            save_user_data({"name": name})

        elif current_tag == "collect_email":
            email = request.json.get("message", "")
            response = [
                "Please provide your phone number."
            ]
            response_tag = "collect_phone"
            options = []
            save_user_data({"email": email})

        elif current_tag == "collect_phone":
            phone = request.json.get("message", "")
            save_user_data({"phone": phone})
            response = [
                "Thank you for providing your details. Our team will reach out to you shortly."
            ]
            response_tag = "end_conversation"
            options = []

        return jsonify({"response": response, "tag": response_tag, "options": options})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
