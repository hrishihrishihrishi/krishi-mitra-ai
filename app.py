import streamlit as st
import os
from utils.gemini_helper import ask_gemini, analyze_image_for_disease
from utils.weather_helper import get_weather_data
from utils.crop_advisory import get_crop_recommendation
from utils.news_helper import get_agriculture_news
import json
from datetime import datetime
import base64

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

# Header
st.markdown("""
<div style="background-color: #4CAF50; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; text-align: center; margin: 0;">🌾 Krishi Mitra AI — Your Smart Farming Companion</h1>
    <p style="color: white; text-align: center; margin: 10px 0 0 0; font-size: 18px;">
        👨‍🌾 Ramesh – Palakkad, Kerala
    </p>
</div>
""", unsafe_allow_html=True)

# Language selector
languages = {"English": "en", "Malayalam": "ml", "Hindi": "hi", "Marathi": "mr"}
st.session_state.language = st.selectbox(
    "🌐 Select Language / भाषा चुनें / ഭാഷ തിരഞ്ഞെടുക്കുക / भाषा निवडा",
    options=list(languages.keys()),
    index=0
)

# Sidebar navigation
st.sidebar.title("Navigation")
sections = ["💬 Ask AI", "🌦️ Weather Info", "📢 Schemes", "🌾 Crop Advisory", "📰 News Feed"]

for section in sections:
    if st.sidebar.button(section, key=section):
        st.session_state.current_section = section.split(" ", 1)[1]  # Remove emoji for comparison

# Main content area
if st.session_state.current_section == "Ask AI":
    st.header("💬 AI Farming Assistant")
    
    # Chat interface
    st.subheader("Ask your farming questions")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**Krishi Mitra:** {chat['answer']}")
            st.divider()
    
    # Input methods
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        user_query = st.text_input("Type your farming question here...", key="chat_input")
    
    with col2:
        if st.button("🎤 Voice Input"):
            st.info("Voice input feature will be available soon!")
    
    with col3:
        if st.button("📤 Send"):
            if user_query:
                with st.spinner("Getting AI response..."):
                    try:
                        response = ask_gemini(user_query, languages[st.session_state.language])
                        st.session_state.chat_history.append({
                            "question": user_query,
                            "answer": response
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error getting AI response: {str(e)}")
    
    # Image upload for disease detection
    st.subheader("🔍 Crop Disease Detection")
    uploaded_file = st.file_uploader("Upload crop image for disease analysis", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        
        if st.button("Analyze Disease"):
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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🌾 Krishi Mitra AI - Empowering Farmers with Technology</p>
    <p>For support, contact: krishimitra@support.gov.in</p>
</div>
""", unsafe_allow_html=True)
