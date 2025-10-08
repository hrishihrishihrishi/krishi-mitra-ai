import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file (if it exists)
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "default_key"))

def ask_gemini(query, language="en"):
    """
    Ask Gemini AI a farming-related question with multilingual support
    """
    try:
        # Language codes mapping
        lang_map = {
            "en": "English",
            "ml": "Malayalam", 
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        target_language = lang_map.get(language, "English")
        
        # Create a comprehensive farming assistant prompt
        system_prompt = f"""
        You are Krishi Mitra AI, an expert agricultural assistant for Indian farmers. 
        You have deep knowledge of:
        - Indian crops, seasons (Kharif, Rabi, Zaid)
        - Soil types common in India
        - Pest and disease management
        - Government schemes and subsidies
        - Weather-based farming advice
        - Sustainable farming practices
        - Market prices and trends
        - Fertilizer and seed recommendations
        
        Always provide:
        1. Practical, actionable advice
        2. Context-specific recommendations for Indian conditions
        3. Cost-effective solutions
        4. Traditional knowledge combined with modern techniques
        
        Respond in {target_language}. If the user asks in a different language, detect it and respond in that language.
        Keep responses informative yet concise (200-300 words max).
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=query)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        
        return response.text or "I apologize, but I couldn't process your query at the moment. Please try again."
        
    except Exception as e:
        return f"Error: Unable to get AI response. Please check your internet connection and try again. ({str(e)})"

def analyze_image_for_disease(image_path, language="en"):
    """
    Analyze crop image for disease detection using Gemini Vision
    """
    try:
        lang_map = {
            "en": "English",
            "ml": "Malayalam", 
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        target_language = lang_map.get(language, "English")
        
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        system_prompt = f"""
        You are an expert plant pathologist specializing in crop diseases common in India.
        Analyze this image and provide:
        1. Crop identification if possible
        2. Disease/pest identification
        3. Severity level (Mild/Moderate/Severe)
        4. Immediate treatment recommendations
        5. Prevention measures
        6. Organic/chemical treatment options
        
        Focus on diseases common in Indian agriculture.
        Respond in {target_language}.
        If you cannot identify any disease, suggest general plant health tips.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                system_prompt
            ],
        )
        
        return response.text or "Unable to analyze the image. Please ensure the image is clear and shows the affected plant parts."
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def translate_text(text, target_language):
    """
    Translate text to target language using Gemini
    """
    try:
        lang_map = {
            "en": "English",
            "ml": "Malayalam", 
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        target_lang = lang_map.get(target_language, "English")
        
        prompt = f"Translate the following text to {target_lang}. Keep agricultural terms accurate:\n\n{text}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return response.text or text
        
    except Exception as e:
        return text  # Return original text if translation fails
