import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

from utils.gemini_helper import ask_gemini, analyze_image_for_disease
from utils.weather_helper import get_weather_data
from utils.crop_advisory import get_crop_recommendation
from utils.news_helper import get_agriculture_news
from utils.auth_helper import register_user, login_user, get_user_data
from utils.market_prices import get_market_prices, get_market_insights, get_best_selling_time
from utils.farming_calendar import get_crop_calendar, add_crop_to_user, get_upcoming_tasks, add_reminder
import json
from datetime import datetime, timedelta
import base64
import speech_recognition as sr
import tempfile
import io
from audio_recorder_streamlit import audio_recorder

# Page configuration
st.set_page_config(
    page_title="🌾 Krishi Mitra AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Ask AI"

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'language' not in st.session_state:
    st.session_state.language = "English"

#if 'voice_query' not in st.session_state:
    #st.session_state.voice_query = ""

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_mobile' not in st.session_state:
    st.session_state.user_mobile = None

if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# def process_voice_input(audio_file, language_code):
#     """Process voice input and convert to text"""
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.AudioFile(audio_file) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data, language=language_code)
#             return text
#     except sr.UnknownValueError:
#         return "Could not understand audio"
#     except sr.RequestError as e:
#         return f"Could not request results; {e}"
#     except Exception as e:
#         return f"Error: {str(e)}"

# Header
if st.session_state.authenticated and st.session_state.user_data:
    user_info = f"👨‍🌾 {st.session_state.user_data['name']} – {st.session_state.user_data['location']}"
else:
    user_info = "👨‍🌾 Guest User"

st.markdown(f"""
<div style="background-color: #4CAF50; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">🌾 Krishi Mitra AI — Your Smart Farming Companion</h1>
    <p style="color: white; text-align: center; margin: 10px 0 0 0; font-size: 18px;">
        {user_info}
    </p>
</div>
""", unsafe_allow_html=True)

# Language selector
languages = {"English": "en", "Malayalam": "ml", "Hindi": "hi", "Marathi": "mr"}

# UI translations
ui_translations = {
    "English": {
        "select_language": "🌐 Select Language",
        "navigation": "Navigation",
        "ask_ai": "💬 Ask AI",
        "weather_info": "🌦️ Weather Info",
        "schemes": "📢 Schemes",
        "crop_advisory": "🌾 Crop Advisory",
        "news_feed": "📰 News Feed",
        "market_prices": "📈 Market Prices",
        "farming_calendar": "📅 My Calendar",
        "login": "🔐 Login/Signup",
        "farming_assistant": "AI Farming Assistant",
        "ask_questions": "Ask your farming questions",
        "type_question": "Type your farming question here...",
        "send": "📤 Send",
        "voice_input": "🎤 Voice Input - Speak Directly",
        "record_voice": "Click to record your question",
        "upload_audio": "Upload audio file (WAV format)",
        "process_voice": "🎤 Process Voice Input",
        "disease_detection": "🔍 Crop Disease Detection",
        "upload_image": "Upload crop image for disease analysis",
        "analyze": "Analyze Disease",
        "logout": "Logout",
        "weather_header": "🌦️ Weather Information",
        "temperature": "🌡️ Temperature",
        "humidity": "💧 Humidity",
        "rainfall": "🌧️ Rainfall",
        "wind_speed": "💨 Wind Speed",
        "current_conditions": "Current Conditions",
        "weather": "Weather",
        "feels_like": "Feels like",
        "farming_advisory": "🧑‍🌾 Farming Advisory",
        "high_humidity": "⚠️ High humidity detected. Monitor crops for fungal diseases.",
        "high_temp": "🌡️ High temperature. Ensure adequate irrigation.",
        "good_rainfall": "🌧️ Good rainfall. Perfect for rice cultivation.",
        "schemes_header": "📢 Government Schemes",
        "available_schemes": "Available Schemes for Kerala",
        "description": "Description",
        "eligibility": "Eligibility",
        "benefits": "Benefits",
        "how_to_apply": "How to Apply",
        "deadline": "Deadline",
        "contact": "Contact",
        "crop_advisory_header": "🌾 Crop Advisory System",
        "select_season": "Select Current Season",
        "select_soil": "Select Soil Type",
        "get_recommendations": "Get Crop Recommendations",
        "recommended_crops": "🌱 Recommended Crops",
        "alternative_crops": "Alternative Crops",
        "farming_tips": "🧑‍🌾 Farming Tips",
        "news_header": "📰 Agriculture News Feed",
        "source": "Source",
        "read_more": "Read More",
        "market_header": "📈 Market Prices",
        "live_prices": "📊 Live Market Prices",
        "last_updated": "Last Updated",
        "market_insights": "💡 Market Insights",
        "best_time_sell": "⏰ Best Time to Sell",
        "select_crop": "Select Crop",
        "best_months": "Best Months",
        "reason": "Reason",
        "advice": "Advice",
        "login_header": "🔐 Login / Signup",
        "login_tab": "Login",
        "signup_tab": "Sign Up",
        "login_to_account": "Login to Your Account",
        "mobile_number": "Mobile Number",
        "password": "Password",
        "login_button": "Login",
        "create_account": "Create New Account",
        "full_name": "Full Name",
        "location": "Location (Village, District, State)",
        "confirm_password": "Confirm Password",
        "signup_button": "Sign Up",
        "calendar_header": "📅 My Farming Calendar",
        "my_crops": "🌾 My Crops",
        "add_new_crop": "🌱 Add New Crop",
        "upcoming_tasks": "📋 Upcoming Tasks (Next 7 Days)",
        "planting_date": "Planting Date",
        "expected_harvest": "Expected Harvest",
        "total_duration": "Total Duration",
        "growth_stages": "Growth Stages",
        "activities": "Activities",
        "fertilizer_schedule": "Fertilizer Schedule",
        "area_acres": "Area (in acres)",
        "add_crop_button": "Add Crop",
        "add_reminder": "➕ Add Custom Reminder",
        "reminder_title": "Reminder Title",
        "reminder_date": "Reminder Date",
        "description_optional": "Description (optional)",
        "add_reminder_button": "Add Reminder",
        "affects": "Affects",
        "market_label": "Market"
    },
    "Hindi": {
        "select_language": "🌐 भाषा चुनें",
        "navigation": "नेविगेशन",
        "ask_ai": "💬 AI से पूछें",
        "weather_info": "🌦️ मौसम की जानकारी",
        "schemes": "📢 योजनाएं",
        "crop_advisory": "🌾 फसल सलाह",
        "news_feed": "📰 समाचार",
        "market_prices": "📈 बाजार मूल्य",
        "farming_calendar": "📅 मेरा कैलेंडर",
        "login": "🔐 लॉगिन/साइनअप",
        "farming_assistant": "कृषि सहायक AI",
        "ask_questions": "अपने कृषि संबंधी प्रश्न पूछें",
        "type_question": "यहाँ अपना प्रश्न लिखें...",
        "send": "📤 भेजें",
        "voice_input": "🎤 वॉइस इनपुट - सीधे बोलें",
        "record_voice": "अपना सवाल रिकॉर्ड करने के लिए क्लिक करें",
        "upload_audio": "ऑडियो फ़ाइल अपलोड करें (WAV प्रारूप)",
        "process_voice": "🎤 वॉइस प्रोसेस करें",
        "disease_detection": "🔍 फसल रोग का पता लगाना",
        "upload_image": "रोग विश्लेषण के लिए फसल की तस्वीर अपलोड करें",
        "analyze": "विश्लेषण करें",
        "logout": "लॉगआउट",
        "weather_header": "🌦️ मौसम की जानकारी",
        "temperature": "🌡️ तापमान",
        "humidity": "💧 आर्द्रता",
        "rainfall": "🌧️ वर्षा",
        "wind_speed": "💨 हवा की गति",
        "current_conditions": "वर्तमान स्थिति",
        "weather": "मौसम",
        "feels_like": "महसूस होता है",
        "farming_advisory": "🧑‍🌾 कृषि सलाह",
        "high_humidity": "⚠️ उच्च आर्द्रता का पता चला। फंगल रोगों के लिए फसलों की निगरानी करें।",
        "high_temp": "🌡️ उच्च तापमान। पर्याप्त सिंचाई सुनिश्चित करें।",
        "good_rainfall": "🌧️ अच्छी वर्षा। धान की खेती के लिए उपयुक्त।",
        "schemes_header": "📢 सरकारी योजनाएं",
        "available_schemes": "केरल के लिए उपलब्ध योजनाएं",
        "description": "विवरण",
        "eligibility": "पात्रता",
        "benefits": "लाभ",
        "how_to_apply": "आवेदन कैसे करें",
        "deadline": "अंतिम तिथि",
        "contact": "संपर्क",
        "crop_advisory_header": "🌾 फसल सलाह प्रणाली",
        "select_season": "वर्तमान मौसम चुनें",
        "select_soil": "मिट्टी का प्रकार चुनें",
        "get_recommendations": "फसल सिफारिशें प्राप्त करें",
        "recommended_crops": "🌱 अनुशंसित फसलें",
        "alternative_crops": "वैकल्पिक फसलें",
        "farming_tips": "🧑‍🌾 कृषि युक्तियाँ",
        "news_header": "📰 कृषि समाचार फ़ीड",
        "source": "स्रोत",
        "read_more": "और पढ़ें",
        "market_header": "📈 बाजार मूल्य",
        "live_prices": "📊 लाइव बाजार मूल्य",
        "last_updated": "अंतिम अपडेट",
        "market_insights": "💡 बाजार अंतर्दृष्टि",
        "best_time_sell": "⏰ बेचने का सबसे अच्छा समय",
        "select_crop": "फसल चुनें",
        "best_months": "सबसे अच्छे महीने",
        "reason": "कारण",
        "advice": "सलाह",
        "login_header": "🔐 लॉगिन / साइनअप",
        "login_tab": "लॉगिन",
        "signup_tab": "साइन अप",
        "login_to_account": "अपने खाते में लॉगिन करें",
        "mobile_number": "मोबाइल नंबर",
        "password": "पासवर्ड",
        "login_button": "लॉगिन",
        "create_account": "नया खाता बनाएं",
        "full_name": "पूरा नाम",
        "location": "स्थान (गांव, जिला, राज्य)",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "signup_button": "साइन अप",
        "calendar_header": "📅 मेरा कृषि कैलेंडर",
        "my_crops": "🌾 मेरी फसलें",
        "add_new_crop": "🌱 नई फसल जोड़ें",
        "upcoming_tasks": "📋 आगामी कार्य (अगले 7 दिन)",
        "planting_date": "रोपण तिथि",
        "expected_harvest": "अपेक्षित फसल",
        "total_duration": "कुल अवधि",
        "growth_stages": "वृद्धि चरण",
        "activities": "गतिविधियाँ",
        "fertilizer_schedule": "उर्वरक अनुसूची",
        "area_acres": "क्षेत्रफल (एकड़ में)",
        "add_crop_button": "फसल जोड़ें",
        "add_reminder": "➕ कस्टम रिमाइंडर जोड़ें",
        "reminder_title": "रिमाइंडर शीर्षक",
        "reminder_date": "रिमाइंडर तिथि",
        "description_optional": "विवरण (वैकल्पिक)",
        "add_reminder_button": "रिमाइंडर जोड़ें",
        "affects": "प्रभावित करता है",
        "market_label": "बाजार"
    },
    "Malayalam": {
        "select_language": "🌐 ഭാഷ തിരഞ്ഞെടുക്കുക",
        "navigation": "നാവിഗേഷൻ",
        "ask_ai": "💬 AI യോട് ചോദിക്കുക",
        "weather_info": "🌦️ കാലാവസ്ഥാ വിവരം",
        "schemes": "📢 പദ്ധതികൾ",
        "crop_advisory": "🌾 വിള ഉപദേശം",
        "news_feed": "📰 വാർത്തകൾ",
        "market_prices": "📈 വിപണി വില",
        "farming_calendar": "📅 എന്റെ കലണ്ടർ",
        "login": "🔐 ലോഗിൻ/സൈൻഅപ്പ്",
        "farming_assistant": "കൃഷി സഹായി AI",
        "ask_questions": "നിങ്ങളുടെ കൃഷി ചോദ്യങ്ങൾ ചോദിക്കുക",
        "type_question": "ഇവിടെ നിങ്ങളുടെ ചോദ്യം ടൈപ്പ് ചെയ്യുക...",
        "send": "📤 അയയ്ക്കുക",
        "voice_input": "🎤 വോയ്സ് ഇൻപുട്ട് - നേരിട്ട് സംസാരിക്കുക",
        "record_voice": "നിങ്ങളുടെ ചോദ്യം റെക്കോർഡ് ചെയ്യാൻ ക്ലിക്ക് ചെയ്യുക",
        "upload_audio": "ഓഡിയോ ഫയൽ അപ്‌ലോഡ് ചെയ്യുക (WAV ഫോർമാറ്റ്)",
        "process_voice": "🎤 വോയ്സ് പ്രോസസ് ചെയ്യുക",
        "disease_detection": "🔍 വിള രോഗ കണ്ടെത്തൽ",
        "upload_image": "രോഗ വിശകലനത്തിനായി വിള ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "analyze": "വിശകലനം ചെയ്യുക",
        "logout": "ലോഗൗട്ട്",
        "weather_header": "🌦️ കാലാവസ്ഥാ വിവരം",
        "temperature": "🌡️ ഊഷ്മാവ്",
        "humidity": "💧 ഈർപ്പം",
        "rainfall": "🌧️ മഴ",
        "wind_speed": "💨 കാറ്റിന്റെ വേഗത",
        "current_conditions": "നിലവിലെ അവസ്ഥ",
        "weather": "കാലാവസ്ഥ",
        "feels_like": "അനുഭവപ്പെടുന്നത്",
        "farming_advisory": "🧑‍🌾 കൃഷി ഉപദേശം",
        "high_humidity": "⚠️ ഉയർന്ന ഈർപ്പം കണ്ടെത്തി. ഫംഗൽ രോഗങ്ങൾക്കായി വിളകൾ നിരീക്ഷിക്കുക.",
        "high_temp": "🌡️ ഉയർന്ന താപനില. മതിയായ ജലസേചനം ഉറപ്പാക്കുക.",
        "good_rainfall": "🌧️ നല്ല മഴ. നെല്ല് കൃഷിക്ക് അനുയോജ്യം.",
        "schemes_header": "📢 സർക്കാർ പദ്ധതികൾ",
        "available_schemes": "കേരളത്തിനായി ലഭ്യമായ പദ്ധതികൾ",
        "description": "വിവരണം",
        "eligibility": "യോഗ്യത",
        "benefits": "ആനുകൂല്യങ്ങൾ",
        "how_to_apply": "എങ്ങനെ അപേക്ഷിക്കാം",
        "deadline": "അവസാന തീയതി",
        "contact": "ബന്ധപ്പെടുക",
        "crop_advisory_header": "🌾 വിള ഉപദേശ സംവിധാനം",
        "select_season": "നിലവിലെ സീസൺ തിരഞ്ഞെടുക്കുക",
        "select_soil": "മണ്ണിന്റെ തരം തിരഞ്ഞെടുക്കുക",
        "get_recommendations": "വിള ശുപാർശകൾ നേടുക",
        "recommended_crops": "🌱 ശുപാർശ ചെയ്ത വിളകൾ",
        "alternative_crops": "ബദൽ വിളകൾ",
        "farming_tips": "🧑‍🌾 കൃഷി നുറുങ്ങുകൾ",
        "news_header": "📰 കാർഷിക വാർത്താ ഫീഡ്",
        "source": "ഉറവിടം",
        "read_more": "കൂടുതൽ വായിക്കുക",
        "market_header": "📈 മാർക്കറ്റ് വിലകൾ",
        "live_prices": "📊 തത്സമയ വിപണി വിലകൾ",
        "last_updated": "അവസാനം അപ്ഡേറ്റ് ചെയ്തത്",
        "market_insights": "💡 വിപണി സ്ഥിതിവിവരങ്ങൾ",
        "best_time_sell": "⏰ വിൽക്കാനുള്ള മികച്ച സമയം",
        "select_crop": "വിള തിരഞ്ഞെടുക്കുക",
        "best_months": "മികച്ച മാസങ്ങൾ",
        "reason": "കാരണം",
        "advice": "ഉപദേശം",
        "login_header": "🔐 ലോഗിൻ / സൈൻഅപ്പ്",
        "login_tab": "ലോഗിൻ",
        "signup_tab": "സൈൻ അപ്പ്",
        "login_to_account": "നിങ്ങളുടെ അക്കൗണ്ടിലേക്ക് ലോഗിൻ ചെയ്യുക",
        "mobile_number": "മൊബൈൽ നമ്പർ",
        "password": "പാസ്‌വേഡ്",
        "login_button": "ലോഗിൻ",
        "create_account": "പുതിയ അക്കൗണ്ട് സൃഷ്ടിക്കുക",
        "full_name": "പൂർണ്ണ നാമം",
        "location": "സ്ഥലം (ഗ്രാമം, ജില്ല, സംസ്ഥാനം)",
        "confirm_password": "പാസ്‌വേഡ് സ്ഥിരീകരിക്കുക",
        "signup_button": "സൈൻ അപ്പ്",
        "calendar_header": "📅 എന്റെ കാർഷിക കലണ്ടർ",
        "my_crops": "🌾 എന്റെ വിളകൾ",
        "add_new_crop": "🌱 പുതിയ വിള ചേർക്കുക",
        "upcoming_tasks": "📋 വരാനിരിക്കുന്ന ചുമതലകൾ (അടുത്ത 7 ദിവസം)",
        "planting_date": "നടീൽ തീയതി",
        "expected_harvest": "പ്രതീക്ഷിക്കുന്ന വിളവെടുപ്പ്",
        "total_duration": "മൊത്തം ദൈർഘ്യം",
        "growth_stages": "വളർച്ചാ ഘട്ടങ്ങൾ",
        "activities": "പ്രവർത്തനങ്ങൾ",
        "fertilizer_schedule": "വളം ഷെഡ്യൂൾ",
        "area_acres": "വിസ്തീർണ്ണം (ഏക്കറിൽ)",
        "add_crop_button": "വിള ചേർക്കുക",
        "add_reminder": "➕ കസ്റ്റം റിമൈൻഡർ ചേർക്കുക",
        "reminder_title": "റിമൈൻഡർ ശീർഷകം",
        "reminder_date": "റിമൈൻഡർ തീയതി",
        "description_optional": "വിവരണം (ഓപ്ഷണൽ)",
        "add_reminder_button": "റിമൈൻഡർ ചേർക്കുക",
        "affects": "ബാധിക്കുന്നത്",
        "market_label": "വിപണി"
    },
    "Marathi": {
        "select_language": "🌐 भाषा निवडा",
        "navigation": "नेव्हिगेशन",
        "ask_ai": "💬 AI ला विचारा",
        "weather_info": "🌦️ हवामान माहिती",
        "schemes": "📢 योजना",
        "crop_advisory": "🌾 पीक सल्ला",
        "news_feed": "📰 बातम्या",
        "market_prices": "📈 बाजार किंमत",
        "farming_calendar": "📅 माझे कॅलेंडर",
        "login": "🔐 लॉगिन/साइनअप",
        "farming_assistant": "शेती सहाय्यक AI",
        "ask_questions": "तुमचे शेती प्रश्न विचारा",
        "type_question": "येथे तुमचा प्रश्न टाइप करा...",
        "send": "📤 पाठवा",
        "voice_input": "🎤 व्हॉइस इनपुट - थेट बोला",
        "record_voice": "तुमचा प्रश्न रेकॉर्ड करण्यासाठी क्लिक करा",
        "upload_audio": "ऑडिओ फाइल अपलोड करा (WAV स्वरूप)",
        "process_voice": "🎤 व्हॉइस प्रोसेस करा",
        "disease_detection": "🔍 पीक रोग शोध",
        "upload_image": "रोग विश्लेषणासाठी पीक प्रतिमा अपलोड करा",
        "analyze": "विश्लेषण करा",
        "logout": "लॉगआउट",
        "weather_header": "🌦️ हवामान माहिती",
        "temperature": "🌡️ तापमान",
        "humidity": "💧 आर्द्रता",
        "rainfall": "🌧️ पाऊस",
        "wind_speed": "💨 वाऱ्याचा वेग",
        "current_conditions": "सध्याची परिस्थिती",
        "weather": "हवामान",
        "feels_like": "जाणवते",
        "farming_advisory": "🧑‍🌾 शेती सल्ला",
        "high_humidity": "⚠️ उच्च आर्द्रता आढळली. बुरशीजन्य रोगांसाठी पिकांचे निरीक्षण करा.",
        "high_temp": "🌡️ उच्च तापमान. पुरेसे सिंचन सुनिश्चित करा.",
        "good_rainfall": "🌧️ चांगला पाऊस. तांदूळ लागवडीसाठी योग्य.",
        "schemes_header": "📢 सरकारी योजना",
        "available_schemes": "केरळसाठी उपलब्ध योजना",
        "description": "वर्णन",
        "eligibility": "पात्रता",
        "benefits": "फायदे",
        "how_to_apply": "अर्ज कसा करावा",
        "deadline": "अंतिम तारीख",
        "contact": "संपर्क",
        "crop_advisory_header": "🌾 पीक सल्ला प्रणाली",
        "select_season": "सध्याचा हंगाम निवडा",
        "select_soil": "मातीचा प्रकार निवडा",
        "get_recommendations": "पीक शिफारसी मिळवा",
        "recommended_crops": "🌱 शिफारस केलेली पिके",
        "alternative_crops": "पर्यायी पिके",
        "farming_tips": "🧑‍🌾 शेती टिपा",
        "news_header": "📰 कृषी बातम्या फीड",
        "source": "स्रोत",
        "read_more": "अधिक वाचा",
        "market_header": "📈 बाजार किंमत",
        "live_prices": "📊 थेट बाजार किंमत",
        "last_updated": "शेवटचे अपडेट",
        "market_insights": "💡 बाजार अंतर्दृष्टी",
        "best_time_sell": "⏰ विक्रीसाठी सर्वोत्तम वेळ",
        "select_crop": "पीक निवडा",
        "best_months": "सर्वोत्तम महिने",
        "reason": "कारण",
        "advice": "सल्ला",
        "login_header": "🔐 लॉगिन / साइनअप",
        "login_tab": "लॉगिन",
        "signup_tab": "साइन अप",
        "login_to_account": "तुमच्या खात्यात लॉगिन करा",
        "mobile_number": "मोबाइल नंबर",
        "password": "पासवर्ड",
        "login_button": "लॉगिन",
        "create_account": "नवीन खाते तयार करा",
        "full_name": "पूर्ण नाव",
        "location": "स्थान (गाव, जिल्हा, राज्य)",
        "confirm_password": "पासवर्ड पुष्टी करा",
        "signup_button": "साइन अप",
        "calendar_header": "📅 माझे शेती कॅलेंडर",
        "my_crops": "🌾 माझी पिके",
        "add_new_crop": "🌱 नवीन पीक जोडा",
        "upcoming_tasks": "📋 आगामी कार्ये (पुढील 7 दिवस)",
        "planting_date": "लागवड तारीख",
        "expected_harvest": "अपेक्षित कापणी",
        "total_duration": "एकूण कालावधी",
        "growth_stages": "वाढीचे टप्पे",
        "activities": "क्रियाकलाप",
        "fertilizer_schedule": "खत वेळापत्रक",
        "area_acres": "क्षेत्रफळ (एकरमध्ये)",
        "add_crop_button": "पीक जोडा",
        "add_reminder": "➕ सानुकूल रिमाइंडर जोडा",
        "reminder_title": "रिमाइंडर शीर्षक",
        "reminder_date": "रिमाइंडर तारीख",
        "description_optional": "वर्णन (पर्यायी)",
        "add_reminder_button": "रिमाइंडर जोडा",
        "affects": "प्रभावित करते",
        "market_label": "बाजार"
    }
}

current_lang = st.selectbox(
    ui_translations[st.session_state.language]["select_language"] + " / Select Language / भाषा चुनें / ഭാഷ തിരഞ്ഞെടുക്കുക / भाषा निवडा",
    options=list(languages.keys()),
    index=list(languages.keys()).index(st.session_state.language)
)

if current_lang != st.session_state.language:
    st.session_state.language = current_lang
    st.rerun()

# Get current language translations
t = ui_translations[st.session_state.language]

# Sidebar navigation
st.sidebar.title(t["navigation"])

# Login/Logout button
if st.session_state.authenticated:
    if st.sidebar.button(f"👤 {st.session_state.user_data['name']} - {t['logout']}", key="logout_btn"):
        st.session_state.authenticated = False
        st.session_state.user_mobile = None
        st.session_state.user_data = None
        st.session_state.current_section = "Ask AI"
        st.rerun()
else:
    if st.sidebar.button(t["login"], key="login_btn"):
        st.session_state.current_section = "Login"

st.sidebar.divider()

# Main sections
sections = [
    (t["ask_ai"], "Ask AI"),
    (t["weather_info"], "Weather Info"),
    (t["schemes"], "Schemes"),
    (t["crop_advisory"], "Crop Advisory"),
    (t["news_feed"], "News Feed"),
    (t["market_prices"], "Market Prices"),
]

# Add authenticated-only sections
if st.session_state.authenticated:
    sections.append((t["farming_calendar"], "Farming Calendar"))

for display_name, section_key in sections:
    if st.sidebar.button(display_name, key=section_key):
        st.session_state.current_section = section_key

# Main content area
if st.session_state.current_section == "Ask AI":
    st.header(t["farming_assistant"])
    
    # Chat interface
    st.subheader(t["ask_questions"])
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**Krishi Mitra:** {chat['answer']}")
            st.divider()
    
    # Language code mapping for speech recognition
    speech_lang_codes = {
        "English": "en-IN",
        "Malayalam": "ml-IN",
        "Hindi": "hi-IN",
        "Marathi": "mr-IN"
    }
    
    # # Voice input section
    # st.subheader(t["voice_input"])
    # st.caption(t["record_voice"])
    # audio_bytes = audio_recorder(
    #     text="",
    #     recording_color="#e74c3c",
    #     neutral_color="#3498db",
    #     icon_name="microphone",
    #     icon_size="3x",
    # )
    
    # if audio_bytes:
    #     with st.spinner("Processing voice input..."):
    #         try:
    #             with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
    #                 tmp_file.write(audio_bytes)
    #                 tmp_file_path = tmp_file.name
                
    #             voice_text = process_voice_input(tmp_file_path, speech_lang_codes[st.session_state.language])
    #             st.session_state.voice_query = voice_text
    #             st.success(f"Recognized: {voice_text}")
                
    #             os.unlink(tmp_file_path)
    #         except Exception as e:
    #             st.error(f"Error processing voice: {str(e)}")
    
    # Text input or use voice query
    voice_text_value = st.session_state.get("voice_query", "")
    user_query = st.text_input(
    t["type_question"],
    value=voice_text_value,
    key="chat_input"
)
    
    if st.button(t["send"]):
        if user_query:
            with st.spinner("Getting AI response..."):
                try:
                    response = ask_gemini(user_query, languages[st.session_state.language])
                    st.session_state.chat_history.append({
                        "question": user_query,
                        "answer": response
                    })
                    st.session_state.voice_query = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"Error getting AI response: {str(e)}")
    
    # Image upload for disease detection
    st.subheader(t["disease_detection"])
    uploaded_file = st.file_uploader(t["upload_image"], type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        
        if st.button(t["analyze"]):
            with st.spinner("Analyzing image..."):
                try:
                    # Save uploaded file temporarily
                    with open("temp_image.jpg", "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    analysis = analyze_image_for_disease("temp_image.jpg", languages[st.session_state.language])
                    st.success("Analysis Complete!")
                    st.write(analysis)
                    
                    # Clean up temp file
                    if os.path.exists("temp_image.jpg"):
                        os.remove("temp_image.jpg")
                        
                except Exception as e:
                    st.error(f"Error analyzing image: {str(e)}")

elif st.session_state.current_section == "Weather Info":
    st.header(t["weather_header"])
    
    location = "Palakkad,Kerala,IN"
    
    try:
        weather_data = get_weather_data(location)
        
        if weather_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label=t["temperature"],
                    value=f"{weather_data['temperature']}°C",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label=t["humidity"],
                    value=f"{weather_data['humidity']}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label=t["rainfall"],
                    value=f"{weather_data.get('rainfall', 0)} mm",
                    delta=None
                )
            
            with col4:
                st.metric(
                    label=t["wind_speed"],
                    value=f"{weather_data.get('wind_speed', 0)} km/h",
                    delta=None
                )
            
            st.subheader(t["current_conditions"])
            st.write(f"**{t['weather']}:** {weather_data['description']}")
            st.write(f"**{t['feels_like']}:** {weather_data.get('feels_like', weather_data['temperature'])}°C")
            
            # Weather advisory
            st.subheader(t["farming_advisory"])
            if weather_data['humidity'] > 80:
                st.warning(t["high_humidity"])
            if weather_data['temperature'] > 35:
                st.warning(t["high_temp"])
            if weather_data.get('rainfall', 0) > 10:
                st.info(t["good_rainfall"])
        else:
            st.error("Unable to fetch weather data. Please check your internet connection.")
            
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")

elif st.session_state.current_section == "Schemes":
    st.header(t["schemes_header"])
    
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            schemes_data = json.load(f)
        
        # Filter schemes for Kerala
        kerala_schemes = [scheme for scheme in schemes_data['schemes'] 
                         if 'Kerala' in scheme.get('applicable_states', []) or 'All States' in scheme.get('applicable_states', [])]
        
        st.subheader(f"{t['available_schemes']} ({len(kerala_schemes)} schemes)")
        
        for scheme in kerala_schemes:
            with st.expander(f"🎯 {scheme['title']}"):
                st.write(f"**{t['description']}:** {scheme['description']}")
                st.write(f"**{t['eligibility']}:** {scheme['eligibility']}")
                st.write(f"**{t['benefits']}:** {scheme['benefits']}")
                st.write(f"**{t['how_to_apply']}:** {scheme['how_to_apply']}")
                
                if scheme.get('deadline'):
                    st.write(f"**{t['deadline']}:** {scheme['deadline']}")
                
                if scheme.get('contact_info'):
                    st.write(f"**{t['contact']}:** {scheme['contact_info']}")
    
    except FileNotFoundError:
        st.error("Schemes database not found. Please contact administrator.")
    except Exception as e:
        st.error(f"Error loading schemes: {str(e)}")

elif st.session_state.current_section == "Crop Advisory":
    st.header(t["crop_advisory_header"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        season = st.selectbox(
            t["select_season"],
            ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"]
        )
    
    with col2:
        soil_type = st.selectbox(
            t["select_soil"],
            ["Loamy", "Clay", "Sandy", "Red Soil", "Black Soil", "Alluvial"]
        )
    
    if st.button(t["get_recommendations"]):
        recommendations = get_crop_recommendation(season, soil_type, "Kerala")
        
        st.subheader(t["recommended_crops"])
        
        for crop in recommendations['primary_crops']:
            st.success(f"🌾 **{crop['name']}** - {crop['reason']}")
        
        if recommendations['secondary_crops']:
            st.subheader(t["alternative_crops"])
            for crop in recommendations['secondary_crops']:
                st.info(f"🌿 **{crop['name']}** - {crop['reason']}")
        
        # Additional tips
        st.subheader(t["farming_tips"])
        for tip in recommendations['tips']:
            st.write(f"• {tip}")

elif st.session_state.current_section == "News Feed":
    st.header(t["news_header"])
    
    try:
        news_items = get_agriculture_news()
        
        if news_items:
            for news in news_items:
                with st.container():
                    st.subheader(news['title'])
                    st.write(news['description'])
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{t['source']}:** {news['source']}")
                    with col2:
                        if news.get('url'):
                            st.markdown(f"[{t['read_more']}]({news['url']})")
                    
                    st.divider()
        else:
            st.info("No news items available at the moment. Please check back later.")
            
    except Exception as e:
        st.error(f"Error loading news: {str(e)}")

elif st.session_state.current_section == "Login":
    st.header(t["login_header"])
    
    tab1, tab2 = st.tabs([t["login_tab"], t["signup_tab"]])
    
    with tab1:
        st.subheader(t["login_to_account"])
        mobile = st.text_input(t["mobile_number"], key="login_mobile", max_chars=10)
        password = st.text_input(t["password"], type="password", key="login_password")
        
        if st.button(t["login_button"]):
            if mobile and password:
                success, result = login_user(mobile, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_mobile = mobile
                    st.session_state.user_data = result
                    st.success("Login successful!")
                    st.session_state.current_section = "Farming Calendar"
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("Please enter mobile number and password")
    
    with tab2:
        st.subheader(t["create_account"])
        name = st.text_input(t["full_name"], key="signup_name")
        location = st.text_input(t["location"], key="signup_location")
        mobile_signup = st.text_input(t["mobile_number"], key="signup_mobile", max_chars=10)
        password_signup = st.text_input(t["password"], type="password", key="signup_password")
        confirm_password = st.text_input(t["confirm_password"], type="password", key="signup_confirm")
        
        if st.button(t["signup_button"]):
            if name and location and mobile_signup and password_signup:
                if password_signup == confirm_password:
                    success, message = register_user(name, location, mobile_signup, password_signup)
                    if success:
                        st.success(message + " Please login now.")
                    else:
                        st.error(message)
                else:
                    st.error("Passwords do not match")
            else:
                st.warning("Please fill all fields")

elif st.session_state.current_section == "Market Prices":
    st.header(t["market_header"])
    
    try:
        market_data = get_market_prices("Kerala")
        
        st.subheader(f"{t['live_prices']} - {market_data['state']}")
        st.caption(f"{t['last_updated']}: {market_data['last_updated']}")
        
        # Display prices in cards
        cols = st.columns(3)
        for idx, (crop_name, crop_data) in enumerate(market_data['prices'].items()):
            with cols[idx % 3]:
                trend_emoji = "📈" if crop_data['trend'] == 'up' else ("📉" if crop_data['trend'] == 'down' else "➡️")
                
                st.metric(
                    label=f"{trend_emoji} {crop_name}",
                    value=f"₹{crop_data['modal_price']} / {crop_data['unit']}",
                    delta=crop_data['change']
                )
                st.caption(f"{t['market_label']}: {crop_data['market']}")
        
        st.divider()
        
        # Market Insights
        st.subheader(t["market_insights"])
        insights = get_market_insights("Kerala")
        
        for insight in insights:
            impact_color = "green" if insight['impact'] == 'positive' else ("red" if insight['impact'] == 'negative' else "blue")
            st.markdown(f"**{insight['title']}**")
            st.markdown(f"<p style='color: {impact_color};'>{insight['description']}</p>", unsafe_allow_html=True)
            st.caption(f"{t['affects']}: {', '.join(insight['crops'])}")
            st.divider()
        
        # Best Selling Time
        st.subheader(t["best_time_sell"])
        selected_crop = st.selectbox(t["select_crop"], list(market_data['prices'].keys()))
        
        if selected_crop:
            selling_advice = get_best_selling_time(selected_crop)
            st.info(f"**{t['best_months']}:** {selling_advice['best_months']}")
            st.write(f"**{t['reason']}:** {selling_advice['reason']}")
            st.success(f"**{t['advice']}:** {selling_advice['advice']}")
            
    except Exception as e:
        st.error(f"Error loading market prices: {str(e)}")

elif st.session_state.current_section == "Farming Calendar":
    if not st.session_state.authenticated:
        st.warning("Please login to access your farming calendar")
        st.stop()
    
    st.header(t["calendar_header"])
    
    # Tabs for different features
    tab1, tab2, tab3 = st.tabs([t["my_crops"], t["add_new_crop"], t["upcoming_tasks"]])
    
    with tab1:
        st.subheader(t["my_crops"])
        user_crops = st.session_state.user_data.get('crops', [])
        
        if user_crops:
            for crop in user_crops:
                with st.expander(f"🌱 {crop['name']} - {crop['area_acres']} acres"):
                    calendar = get_crop_calendar(crop['name'], crop['planting_date'])
                    
                    st.write(f"**{t['planting_date']}:** {crop['planting_date']}")
                    st.write(f"**{t['expected_harvest']}:** {calendar['harvest_date']}")
                    st.write(f"**{t['total_duration']}:** {calendar['total_duration']} days")
                    
                    st.subheader(t["growth_stages"])
                    for stage in calendar['timeline']:
                        st.write(f"**{stage['stage']}** ({stage['start_date']} to {stage['end_date']})")
                        st.write(f"{t['activities']}: {', '.join(stage['activities'])}")
                        st.divider()
                    
                    st.subheader(t["fertilizer_schedule"])
                    for fert in calendar['fertilizer_schedule']:
                        st.info(f"**{fert['date']}** - {fert['fertilizer']} ({fert['stage']})")
        else:
            st.info("No crops added yet. Add your first crop in the 'Add New Crop' tab!")
    
    with tab2:
        st.subheader(t["add_new_crop"])
        
        crop_name = st.selectbox(
            t["select_crop"],
            ["Rice (Paddy)", "Coconut", "Pepper", "Banana", "Cardamom", "Ginger", "Turmeric"]
        )
        
        planting_date = st.date_input(t["planting_date"], value=datetime.now())
        area_acres = st.number_input(t["area_acres"], min_value=0.1, max_value=100.0, value=1.0, step=0.5)
        
        if st.button(t["add_crop_button"]):
            success = add_crop_to_user(
                st.session_state.user_mobile,
                crop_name,
                planting_date.isoformat(),
                area_acres
            )
            if success:
                st.session_state.user_data = get_user_data(st.session_state.user_mobile)
                st.success(f"{crop_name} added successfully!")
                st.rerun()
            else:
                st.error("Failed to add crop")
    
    with tab3:
        st.subheader(t["upcoming_tasks"])
        
        upcoming = get_upcoming_tasks(st.session_state.user_mobile, days=7)
        
        if upcoming:
            for task in upcoming:
                days_text = "Today" if task['days_until'] == 0 else f"In {task['days_until']} days"
                
                if task['type'] == 'fertilizer':
                    st.warning(f"**{task['title']}** - {days_text}")
                elif task['type'] == 'stage':
                    st.info(f"**{task['title']}** - {days_text}")
                else:
                    st.success(f"**{task['title']}** - {days_text}")
                
                st.write(task['description'])
                st.caption(f"Date: {task['date']}")
                st.divider()
        else:
            st.info("No upcoming tasks in the next 7 days")
        
        # Add custom reminder
        st.subheader(t["add_reminder"])
        reminder_title = st.text_input(t["reminder_title"])
        reminder_date = st.date_input(t["reminder_date"])
        reminder_desc = st.text_area(t["description_optional"])
        
        if st.button(t["add_reminder_button"]):
            if reminder_title:
                success = add_reminder(
                    st.session_state.user_mobile,
                    {
                        'title': reminder_title,
                        'date': reminder_date.isoformat(),
                        'description': reminder_desc
                    }
                )
                if success:
                    st.session_state.user_data = get_user_data(st.session_state.user_mobile)
                    st.success("Reminder added!")
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🌾 Krishi Mitra AI - Empowering Farmers with Technology</p>
    <p>For support, contact: krishimitra@support.gov.in</p>
</div>
""", unsafe_allow_html=True)
