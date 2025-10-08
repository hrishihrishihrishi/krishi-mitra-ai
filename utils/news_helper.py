import requests
import json
from datetime import datetime, timedelta

def get_agriculture_news():
    """
    Fetch agriculture-related news (using NewsAPI or fallback to hardcoded)
    """
    try:
        # Try to fetch from NewsAPI if available
        news_items = fetch_news_from_api()
        
        if not news_items:
            # Fallback to curated agriculture news
            news_items = get_fallback_news()
        
        return news_items
    
    except Exception as e:
        # Return fallback news in case of any error
        return get_fallback_news()

def fetch_news_from_api():
    """
    Fetch news from NewsAPI (if API key is available)
    """
    try:
        api_key = os.getenv("NEWS_API_KEY", "")
        
        if not api_key or api_key == "default_key":
            return None
        
        base_url = "https://newsapi.org/v2/everything"
        
        params = {
            'q': 'agriculture OR farming OR crops OR farmers India',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': api_key
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            news_items = []
            
            for article in data['articles'][:8]:  # Get top 8 articles
                news_item = {
                    'title': article['title'],
                    'description': article['description'] or 'No description available',
                    'source': article['source']['name'],
                    'published_at': article['publishedAt'],
                    'url': article['url']
                }
                news_items.append(news_item)
            
            return news_items
        
        return None
    
    except Exception:
        return None

def get_fallback_news():
    """
    Fallback agriculture news when API is not available
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    news_items = [
        {
            'title': 'Digital Agriculture Initiatives Boost Farmer Incomes Across India',
            'description': 'Government launches new digital platforms to connect farmers directly with markets, eliminating middlemen and increasing profits by 30%.',
            'source': 'Ministry of Agriculture',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'Monsoon 2024: IMD Predicts Normal Rainfall for Kerala',
            'description': 'Indian Meteorological Department forecasts favorable monsoon conditions for Kerala, benefiting rice and spice cultivation.',
            'source': 'India Meteorological Department',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'New High-Yield Rice Varieties Released for Coastal States',
            'description': 'ICAR develops salt-tolerant rice varieties specifically for coastal regions, promising 20% higher yields.',
            'source': 'Indian Council of Agricultural Research',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'PM-KISAN Benefits Reach 12 Crore Farmers',
            'description': 'Direct benefit transfer scheme successfully provides financial support to millions of small and marginal farmers.',
            'source': 'Press Information Bureau',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'Organic Farming: Kerala Leads in Sustainable Agriculture',
            'description': 'Kerala state government announces incentives for organic farming, aiming to become fully organic by 2025.',
            'source': 'Kerala Agricultural Department',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'Drone Technology Revolutionizes Crop Monitoring',
            'description': 'Farmers increasingly adopt drone technology for pest surveillance and precision agriculture applications.',
            'source': 'Agriculture Technology Today',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'Coconut Prices Show Upward Trend in South Indian Markets',
            'description': 'Increased demand for coconut products drives prices up, benefiting coconut farmers in Kerala and Karnataka.',
            'source': 'Coconut Development Board',
            'published_at': current_date,
            'url': '#'
        },
        {
            'title': 'Climate-Smart Agriculture Practices Gain Momentum',
            'description': 'Farmers adopt climate-resilient techniques to combat changing weather patterns and ensure sustainable production.',
            'source': 'National Sample Survey Office',
            'published_at': current_date,
            'url': '#'
        }
    ]
    
    return news_items

def get_market_prices():
    """
    Get current market prices for major agricultural commodities
    """
    # This would typically fetch from an API like eNAM or commodity exchange
    # For now, returning sample data structure
    
    market_data = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'prices': {
            'Rice (Per Quintal)': {
                'price': '₹2,850',
                'change': '+2.5%',
                'trend': 'up'
            },
            'Coconut (Per 1000 nuts)': {
                'price': '₹18,500',
                'change': '+5.2%', 
                'trend': 'up'
            },
            'Pepper (Per Kg)': {
                'price': '₹485',
                'change': '-1.8%',
                'trend': 'down'
            },
            'Cardamom (Per Kg)': {
                'price': '₹1,250',
                'change': '+3.1%',
                'trend': 'up'
            },
            'Ginger (Per Quintal)': {
                'price': '₹8,200',
                'change': '+0.5%',
                'trend': 'stable'
            },
            'Turmeric (Per Quintal)': {
                'price': '₹7,800',
                'change': '+1.2%',
                'trend': 'up'
            }
        }
    }
    
    return market_data

def get_weather_alerts():
    """
    Get weather-based farming alerts
    """
    alerts = []
    
    # This would typically integrate with weather services
    # Sample alerts based on common scenarios
    
    sample_alerts = [
        {
            'type': 'info',
            'title': 'Favorable Conditions',
            'message': 'Current weather conditions are ideal for rice transplanting in Kerala.',
            'priority': 'low'
        },
        {
            'type': 'warning', 
            'title': 'Heavy Rain Alert',
            'message': 'Heavy rainfall expected in next 48 hours. Secure harvested crops and ensure drainage.',
            'priority': 'high'
        },
        {
            'type': 'advisory',
            'title': 'Pest Management',
            'message': 'High humidity conditions favor fungal diseases. Monitor crops closely.',
            'priority': 'medium'
        }
    ]
    
    return sample_alerts
