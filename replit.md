# Krishi Mitra AI - Agricultural Assistant Application

## Overview

Krishi Mitra AI is a comprehensive agricultural assistant application designed for Indian farmers. The application provides AI-powered farming advice, crop recommendations, weather information, agricultural news, disease diagnosis through image analysis, and information about government schemes. Built with Streamlit for the web interface, it integrates multiple external services to deliver a unified farming support platform with multilingual capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with wide layout configuration
- **State Management**: Session-based state management for tracking user interactions, chat history, language preferences, and voice queries
- **User Interface Components**:
  - Multi-section navigation (Ask AI, Weather, Crop Advisory, News, Schemes)
  - Chat interface with persistent history
  - Voice input capability with audio file processing
  - Image upload and analysis for disease detection
  - Responsive layout with sidebar navigation

### Backend Architecture
- **Modular Design**: Utility-based architecture with specialized helper modules:
  - `gemini_helper.py`: AI-powered query processing and image analysis
  - `weather_helper.py`: Weather data retrieval and processing
  - `crop_advisory.py`: Rule-based crop recommendation engine
  - `news_helper.py`: Agricultural news aggregation with fallback mechanism
  
- **AI Integration**: Google Gemini API (gemini-2.5-flash model) serves as the core AI engine with:
  - Comprehensive agricultural knowledge base
  - Multilingual support (English, Malayalam, Hindi, Marathi)
  - Context-aware responses for Indian farming conditions
  - Image analysis capabilities for crop disease detection

- **Recommendation System**: Rule-based crop advisory system using:
  - Season-based filtering (Kharif, Rabi, Zaid, All Season)
  - Soil type compatibility (Clay, Loamy, Sandy, Red Soil, Alluvial)
  - Regional/state-specific crop database
  - Water requirement and duration metrics

### Data Storage
- **Static Data**: JSON-based storage for government schemes (`schemes.json`)
- **Scheme Database Structure**: Contains comprehensive information including:
  - Scheme details and eligibility criteria
  - Benefits and application procedures
  - State-specific applicability
  - Contact information and deadlines
- **Session State**: In-memory storage for chat history and user preferences (no persistent database)
- **Crop Database**: In-code dictionary structure with crop characteristics and growing requirements

### Multilingual Support
- **Language Options**: English, Malayalam, Hindi, Marathi
- **Implementation**: Language code mapping with automatic detection and response generation in target language
- **Voice Input**: Speech recognition with language-specific processing using Google Speech Recognition API

### Voice Processing
- **Speech Recognition**: Uses `speech_recognition` library with Google's speech-to-text service
- **Audio Handling**: Temporary file processing for uploaded audio files
- **Error Handling**: Comprehensive exception handling for audio processing failures

## External Dependencies

### APIs and Services
1. **Google Gemini API** (`google.genai`)
   - Purpose: AI-powered agricultural query responses and image analysis
   - Model: gemini-2.5-flash
   - Authentication: API key via environment variable `GEMINI_API_KEY`
   - Features: Text generation, image analysis for disease detection

2. **OpenWeatherMap API**
   - Purpose: Real-time weather data retrieval
   - Endpoint: `api.openweathermap.org/data/2.5/weather`
   - Authentication: API key via environment variable `OPENWEATHER_API_KEY`
   - Data: Temperature, humidity, rainfall, wind speed, visibility, sunrise/sunset times

3. **NewsAPI** (Optional)
   - Purpose: Fetching latest agriculture-related news
   - Authentication: API key via environment variable `NEWS_API_KEY`
   - Fallback: Hardcoded curated news when API unavailable
   - Query: Agriculture, farming, crops, farmers India-related news

4. **Google Speech Recognition API**
   - Purpose: Voice-to-text conversion for voice queries
   - Library: `speech_recognition`
   - Language Support: Multiple Indian languages via language codes

### Python Libraries
- **streamlit**: Web application framework
- **google-genai**: Google Gemini AI client
- **requests**: HTTP client for external API calls
- **speech_recognition**: Voice input processing
- **base64, io, tempfile**: File and data handling utilities
- **datetime, json**: Data processing and formatting

### Configuration Requirements
- Environment variables for API keys (GEMINI_API_KEY, OPENWEATHER_API_KEY, NEWS_API_KEY)
- Default fallback values for missing configurations
- Timeout handling (10 seconds) for external API calls
- Error handling with graceful degradation (fallback news, error messages)