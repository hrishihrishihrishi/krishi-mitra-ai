import streamlit as st
import os
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

if 'voice_query' not in st.session_state:
    st.session_state.voice_query = ""

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_mobile' not in st.session_state:
    st.session_state.user_mobile = None

if 'user_data' not in st.session_state:
    st.session_state.user_data = None

def process_voice_input(audio_file, language_code):
    """Process voice input and convert to text"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language_code)
            return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Error: {str(e)}"

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
        "voice_input": "🎤 Voice Input",
        "upload_audio": "Upload audio file (WAV format)",
        "process_voice": "🎤 Process Voice Input",
        "disease_detection": "🔍 Crop Disease Detection",
        "upload_image": "Upload crop image for disease analysis",
        "analyze": "Analyze Disease",
        "logout": "Logout"
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
        "voice_input": "🎤 वॉइस इनपुट",
        "upload_audio": "ऑडियो फ़ाइल अपलोड करें (WAV प्रारूप)",
        "process_voice": "🎤 वॉइस प्रोसेस करें",
        "disease_detection": "🔍 फसल रोग का पता लगाना",
        "upload_image": "रोग विश्लेषण के लिए फसल की तस्वीर अपलोड करें",
        "analyze": "विश्लेषण करें",
        "logout": "लॉगआउट"
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
        "voice_input": "🎤 വോയ്സ് ഇൻപുട്ട്",
        "upload_audio": "ഓഡിയോ ഫയൽ അപ്‌ലോഡ് ചെയ്യുക (WAV ഫോർമാറ്റ്)",
        "process_voice": "🎤 വോയ്സ് പ്രോസസ് ചെയ്യുക",
        "disease_detection": "🔍 വിള രോഗ കണ്ടെത്തൽ",
        "upload_image": "രോഗ വിശകലനത്തിനായി വിള ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "analyze": "വിശകലനം ചെയ്യുക",
        "logout": "ലോഗൗട്ട്"
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
        "voice_input": "🎤 व्हॉइस इनपुट",
        "upload_audio": "ऑडिओ फाइल अपलोड करा (WAV स्वरूप)",
        "process_voice": "🎤 व्हॉइस प्रोसेस करा",
        "disease_detection": "🔍 पीक रोग शोध",
        "upload_image": "रोग विश्लेषणासाठी पीक प्रतिमा अपलोड करा",
        "analyze": "विश्लेषण करा",
        "logout": "लॉगआउट"
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
    
    # Voice input section
    st.subheader(t["voice_input"])
    audio_file = st.file_uploader(t["upload_audio"], type=['wav'], key="audio_upload")
    
    if audio_file is not None:
        if st.button(t["process_voice"]):
            with st.spinner("Processing voice input..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                        tmp_file.write(audio_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    voice_text = process_voice_input(tmp_file_path, speech_lang_codes[st.session_state.language])
                    st.session_state.voice_query = voice_text
                    st.success(f"Recognized: {voice_text}")
                    
                    os.unlink(tmp_file_path)
                except Exception as e:
                    st.error(f"Error processing voice: {str(e)}")
    
    # Text input or use voice query
    user_query = st.text_input(
        t["type_question"], 
        value=st.session_state.voice_query,
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
    st.header("🌦️ Weather Information")
    
    location = "Palakkad,Kerala,IN"
    
    try:
        weather_data = get_weather_data(location)
        
        if weather_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🌡️ Temperature",
                    value=f"{weather_data['temperature']}°C",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="💧 Humidity",
                    value=f"{weather_data['humidity']}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label="🌧️ Rainfall",
                    value=f"{weather_data.get('rainfall', 0)} mm",
                    delta=None
                )
            
            with col4:
                st.metric(
                    label="💨 Wind Speed",
                    value=f"{weather_data.get('wind_speed', 0)} km/h",
                    delta=None
                )
            
            st.subheader("Current Conditions")
            st.write(f"**Weather:** {weather_data['description']}")
            st.write(f"**Feels like:** {weather_data.get('feels_like', weather_data['temperature'])}°C")
            
            # Weather advisory
            st.subheader("🧑‍🌾 Farming Advisory")
            if weather_data['humidity'] > 80:
                st.warning("⚠️ High humidity detected. Monitor crops for fungal diseases.")
            if weather_data['temperature'] > 35:
                st.warning("🌡️ High temperature. Ensure adequate irrigation.")
            if weather_data.get('rainfall', 0) > 10:
                st.info("🌧️ Good rainfall. Perfect for rice cultivation.")
        else:
            st.error("Unable to fetch weather data. Please check your internet connection.")
            
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")

elif st.session_state.current_section == "Schemes":
    st.header("📢 Government Schemes")
    
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            schemes_data = json.load(f)
        
        # Filter schemes for Kerala
        kerala_schemes = [scheme for scheme in schemes_data['schemes'] 
                         if 'Kerala' in scheme.get('applicable_states', []) or 'All States' in scheme.get('applicable_states', [])]
        
        st.subheader(f"Available Schemes for Kerala ({len(kerala_schemes)} schemes)")
        
        for scheme in kerala_schemes:
            with st.expander(f"🎯 {scheme['title']}"):
                st.write(f"**Description:** {scheme['description']}")
                st.write(f"**Eligibility:** {scheme['eligibility']}")
                st.write(f"**Benefits:** {scheme['benefits']}")
                st.write(f"**How to Apply:** {scheme['how_to_apply']}")
                
                if scheme.get('deadline'):
                    st.write(f"**Deadline:** {scheme['deadline']}")
                
                if scheme.get('contact_info'):
                    st.write(f"**Contact:** {scheme['contact_info']}")
    
    except FileNotFoundError:
        st.error("Schemes database not found. Please contact administrator.")
    except Exception as e:
        st.error(f"Error loading schemes: {str(e)}")

elif st.session_state.current_section == "Crop Advisory":
    st.header("🌾 Crop Advisory System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        season = st.selectbox(
            "Select Current Season",
            ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"]
        )
    
    with col2:
        soil_type = st.selectbox(
            "Select Soil Type",
            ["Loamy", "Clay", "Sandy", "Red Soil", "Black Soil", "Alluvial"]
        )
    
    if st.button("Get Crop Recommendations"):
        recommendations = get_crop_recommendation(season, soil_type, "Kerala")
        
        st.subheader("🌱 Recommended Crops")
        
        for crop in recommendations['primary_crops']:
            st.success(f"🌾 **{crop['name']}** - {crop['reason']}")
        
        if recommendations['secondary_crops']:
            st.subheader("Alternative Crops")
            for crop in recommendations['secondary_crops']:
                st.info(f"🌿 **{crop['name']}** - {crop['reason']}")
        
        # Additional tips
        st.subheader("🧑‍🌾 Farming Tips")
        for tip in recommendations['tips']:
            st.write(f"• {tip}")

elif st.session_state.current_section == "News Feed":
    st.header("📰 Agriculture News Feed")
    
    try:
        news_items = get_agriculture_news()
        
        if news_items:
            for news in news_items:
                with st.container():
                    st.subheader(news['title'])
                    st.write(news['description'])
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Source:** {news['source']}")
                    with col2:
                        if news.get('url'):
                            st.markdown(f"[Read More]({news['url']})")
                    
                    st.divider()
        else:
            st.info("No news items available at the moment. Please check back later.")
            
    except Exception as e:
        st.error(f"Error loading news: {str(e)}")

elif st.session_state.current_section == "Login":
    st.header("🔐 Login / Signup")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to Your Account")
        mobile = st.text_input("Mobile Number", key="login_mobile", max_chars=10)
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
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
        st.subheader("Create New Account")
        name = st.text_input("Full Name", key="signup_name")
        location = st.text_input("Location (Village, District, State)", key="signup_location")
        mobile_signup = st.text_input("Mobile Number", key="signup_mobile", max_chars=10)
        password_signup = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Sign Up"):
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
    st.header("📈 Market Prices")
    
    try:
        market_data = get_market_prices("Kerala")
        
        st.subheader(f"📊 Live Market Prices - {market_data['state']}")
        st.caption(f"Last Updated: {market_data['last_updated']}")
        
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
                st.caption(f"Market: {crop_data['market']}")
        
        st.divider()
        
        # Market Insights
        st.subheader("💡 Market Insights")
        insights = get_market_insights("Kerala")
        
        for insight in insights:
            impact_color = "green" if insight['impact'] == 'positive' else ("red" if insight['impact'] == 'negative' else "blue")
            st.markdown(f"**{insight['title']}**")
            st.markdown(f"<p style='color: {impact_color};'>{insight['description']}</p>", unsafe_allow_html=True)
            st.caption(f"Affects: {', '.join(insight['crops'])}")
            st.divider()
        
        # Best Selling Time
        st.subheader("⏰ Best Time to Sell")
        selected_crop = st.selectbox("Select Crop", list(market_data['prices'].keys()))
        
        if selected_crop:
            selling_advice = get_best_selling_time(selected_crop)
            st.info(f"**Best Months:** {selling_advice['best_months']}")
            st.write(f"**Reason:** {selling_advice['reason']}")
            st.success(f"**Advice:** {selling_advice['advice']}")
            
    except Exception as e:
        st.error(f"Error loading market prices: {str(e)}")

elif st.session_state.current_section == "Farming Calendar":
    if not st.session_state.authenticated:
        st.warning("Please login to access your farming calendar")
        st.stop()
    
    st.header("📅 My Farming Calendar")
    
    # Tabs for different features
    tab1, tab2, tab3 = st.tabs(["My Crops", "Add New Crop", "Upcoming Tasks"])
    
    with tab1:
        st.subheader("🌾 My Crops")
        user_crops = st.session_state.user_data.get('crops', [])
        
        if user_crops:
            for crop in user_crops:
                with st.expander(f"🌱 {crop['name']} - {crop['area_acres']} acres"):
                    calendar = get_crop_calendar(crop['name'], crop['planting_date'])
                    
                    st.write(f"**Planting Date:** {crop['planting_date']}")
                    st.write(f"**Expected Harvest:** {calendar['harvest_date']}")
                    st.write(f"**Total Duration:** {calendar['total_duration']} days")
                    
                    st.subheader("Growth Stages")
                    for stage in calendar['timeline']:
                        st.write(f"**{stage['stage']}** ({stage['start_date']} to {stage['end_date']})")
                        st.write(f"Activities: {', '.join(stage['activities'])}")
                        st.divider()
                    
                    st.subheader("Fertilizer Schedule")
                    for fert in calendar['fertilizer_schedule']:
                        st.info(f"**{fert['date']}** - {fert['fertilizer']} ({fert['stage']})")
        else:
            st.info("No crops added yet. Add your first crop in the 'Add New Crop' tab!")
    
    with tab2:
        st.subheader("🌱 Add New Crop")
        
        crop_name = st.selectbox(
            "Select Crop",
            ["Rice (Paddy)", "Coconut", "Pepper", "Banana", "Cardamom", "Ginger", "Turmeric"]
        )
        
        planting_date = st.date_input("Planting Date", value=datetime.now())
        area_acres = st.number_input("Area (in acres)", min_value=0.1, max_value=100.0, value=1.0, step=0.5)
        
        if st.button("Add Crop"):
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
        st.subheader("📋 Upcoming Tasks (Next 7 Days)")
        
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
        st.subheader("➕ Add Custom Reminder")
        reminder_title = st.text_input("Reminder Title")
        reminder_date = st.date_input("Reminder Date")
        reminder_desc = st.text_area("Description (optional)")
        
        if st.button("Add Reminder"):
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
