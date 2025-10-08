def get_crop_recommendation(season, soil_type, state="Kerala"):
    """
    Rule-based crop recommendation system
    """
    
    # Define crop database with characteristics
    crops_db = {
        "Rice": {
            "seasons": ["Kharif (Monsoon)", "Rabi (Winter)"],
            "soil_types": ["Clay", "Loamy", "Alluvial"],
            "states": ["Kerala", "All"],
            "water_req": "High",
            "duration": "120-150 days"
        },
        "Coconut": {
            "seasons": ["All Season"],
            "soil_types": ["Sandy", "Loamy", "Red Soil"],
            "states": ["Kerala", "All"],
            "water_req": "Medium",
            "duration": "Perennial"
        },
        "Pepper": {
            "seasons": ["Kharif (Monsoon)"],
            "soil_types": ["Red Soil", "Loamy"],
            "states": ["Kerala", "All"],
            "water_req": "Medium",
            "duration": "Perennial"
        },
        "Banana": {
            "seasons": ["All Season"],
            "soil_types": ["Loamy", "Alluvial", "Red Soil"],
            "states": ["Kerala", "All"],
            "water_req": "High",
            "duration": "12-15 months"
        },
        "Cardamom": {
            "seasons": ["Kharif (Monsoon)"],
            "soil_types": ["Red Soil", "Loamy"],
            "states": ["Kerala"],
            "water_req": "High",
            "duration": "Perennial"
        },
        "Rubber": {
            "seasons": ["All Season"],
            "soil_types": ["Red Soil", "Loamy"],
            "states": ["Kerala"],
            "water_req": "High",
            "duration": "Perennial"
        },
        "Tapioca": {
            "seasons": ["Kharif (Monsoon)", "Zaid (Summer)"],
            "soil_types": ["Red Soil", "Sandy", "Loamy"],
            "states": ["Kerala", "All"],
            "water_req": "Low",
            "duration": "8-10 months"
        },
        "Ginger": {
            "seasons": ["Kharif (Monsoon)"],
            "soil_types": ["Loamy", "Red Soil"],
            "states": ["Kerala", "All"],
            "water_req": "Medium",
            "duration": "8-10 months"
        },
        "Turmeric": {
            "seasons": ["Kharif (Monsoon)"],
            "soil_types": ["Loamy", "Red Soil", "Clay"],
            "states": ["Kerala", "All"],
            "water_req": "Medium",
            "duration": "7-10 months"
        },
        "Arecanut": {
            "seasons": ["All Season"],
            "soil_types": ["Loamy", "Red Soil"],
            "states": ["Kerala"],
            "water_req": "High",
            "duration": "Perennial"
        },
        "Cashew": {
            "seasons": ["All Season"],
            "soil_types": ["Red Soil", "Sandy"],
            "states": ["Kerala", "All"],
            "water_req": "Low",
            "duration": "Perennial"
        },
        "Cocoa": {
            "seasons": ["All Season"],
            "soil_types": ["Loamy", "Red Soil"],
            "states": ["Kerala"],
            "water_req": "Medium",
            "duration": "Perennial"
        }
    }
    
    # Additional crops for different seasons
    if season == "Rabi (Winter)":
        additional_crops = {
            "Wheat": {
                "seasons": ["Rabi (Winter)"],
                "soil_types": ["Loamy", "Alluvial", "Clay"],
                "states": ["All"],
                "water_req": "Medium",
                "duration": "120-150 days"
            },
            "Barley": {
                "seasons": ["Rabi (Winter)"],
                "soil_types": ["Loamy", "Sandy"],
                "states": ["All"],
                "water_req": "Low",
                "duration": "120-140 days"
            },
            "Mustard": {
                "seasons": ["Rabi (Winter)"],
                "soil_types": ["Loamy", "Sandy"],
                "states": ["All"],
                "water_req": "Low",
                "duration": "90-120 days"
            }
        }
        crops_db.update(additional_crops)
    
    if season == "Zaid (Summer)":
        summer_crops = {
            "Watermelon": {
                "seasons": ["Zaid (Summer)"],
                "soil_types": ["Sandy", "Loamy"],
                "states": ["All"],
                "water_req": "High",
                "duration": "90-100 days"
            },
            "Muskmelon": {
                "seasons": ["Zaid (Summer)"],
                "soil_types": ["Sandy", "Loamy"],
                "states": ["All"],
                "water_req": "Medium",
                "duration": "90-110 days"
            },
            "Cucumber": {
                "seasons": ["Zaid (Summer)"],
                "soil_types": ["Loamy", "Sandy"],
                "states": ["All"],
                "water_req": "High",
                "duration": "50-70 days"
            }
        }
        crops_db.update(summer_crops)
    
    # Find suitable crops
    primary_crops = []
    secondary_crops = []
    
    for crop_name, crop_info in crops_db.items():
        # Check season compatibility
        season_match = (season in crop_info["seasons"] or 
                       "All Season" in crop_info["seasons"])
        
        # Check soil compatibility  
        soil_match = soil_type in crop_info["soil_types"]
        
        # Check state compatibility
        state_match = (state in crop_info["states"] or 
                      "All" in crop_info["states"])
        
        if season_match and soil_match and state_match:
            crop_rec = {
                "name": crop_name,
                "reason": f"Suitable for {season.split('(')[0].strip()} season in {soil_type.lower()} soil",
                "water_requirement": crop_info["water_req"],
                "duration": crop_info["duration"]
            }
            primary_crops.append(crop_rec)
        elif season_match and state_match:  # Partially suitable
            crop_rec = {
                "name": crop_name,
                "reason": f"May work with soil management for {season.split('(')[0].strip()} season",
                "water_requirement": crop_info["water_req"], 
                "duration": crop_info["duration"]
            }
            secondary_crops.append(crop_rec)
    
    # Generate farming tips based on season and soil
    tips = generate_farming_tips(season, soil_type, state)
    
    return {
        "primary_crops": primary_crops[:5],  # Top 5 recommendations
        "secondary_crops": secondary_crops[:3],  # Top 3 alternatives
        "tips": tips
    }

def generate_farming_tips(season, soil_type, state):
    """
    Generate contextual farming tips
    """
    tips = []
    
    # Season-specific tips
    if "Monsoon" in season:
        tips.extend([
            "Ensure proper drainage to prevent waterlogging",
            "Monitor for fungal diseases due to high humidity",
            "Plant at the right time to utilize monsoon rains effectively"
        ])
    elif "Winter" in season:
        tips.extend([
            "Protect crops from frost in colder regions",
            "Irrigation requirements are generally lower",
            "Good time for harvesting kharif crops"
        ])
    elif "Summer" in season:
        tips.extend([
            "Ensure adequate irrigation systems",
            "Use mulching to conserve soil moisture",
            "Consider drought-resistant varieties"
        ])
    
    # Soil-specific tips
    soil_tips = {
        "Clay": [
            "Improve drainage by adding organic matter",
            "Avoid working the soil when it's too wet",
            "Clay soils retain nutrients well but may need better aeration"
        ],
        "Sandy": [
            "Add organic matter to improve water retention",
            "More frequent but lighter irrigation needed",
            "Regular fertilization required as nutrients leach quickly"
        ],
        "Loamy": [
            "Ideal soil type for most crops",
            "Maintain organic matter levels with compost",
            "Well-balanced nutrition and water retention"
        ],
        "Red Soil": [
            "May need lime to reduce acidity",
            "Add phosphorus-rich fertilizers",
            "Good for perennial crops like coconut and cashew"
        ],
        "Black Soil": [
            "Excellent for cotton and sugarcane",
            "Rich in nutrients but may have drainage issues",
            "Deep plowing recommended"
        ],
        "Alluvial": [
            "Very fertile and suitable for cereals",
            "Regular flooding areas - plan accordingly",
            "Rich in potash but may need phosphorus"
        ]
    }
    
    if soil_type in soil_tips:
        tips.extend(soil_tips[soil_type])
    
    # State-specific tips for Kerala
    if state == "Kerala":
        tips.extend([
            "Take advantage of two monsoon seasons",
            "Intercropping with spices can increase income",
            "Consider organic farming for premium prices"
        ])
    
    return tips[:8]  # Return top 8 tips

def get_seasonal_calendar(state="Kerala"):
    """
    Get crop calendar for the specified state
    """
    calendar = {
        "Kharif (June-October)": [
            "Rice (June-July planting)",
            "Ginger (April-June planting)",
            "Turmeric (April-June planting)",
            "Pepper (June-July planting)"
        ],
        "Rabi (November-March)": [
            "Rice (November-December planting)",
            "Vegetables (October-December planting)",
            "Pulses (October-November planting)"
        ],
        "Summer (April-June)": [
            "Tapioca (March-May planting)",
            "Vegetables (February-April planting)",
            "Watermelon (February-March planting)"
        ],
        "Perennial Crops": [
            "Coconut (Year-round)",
            "Rubber (Year-round)",
            "Arecanut (Year-round)",
            "Cashew (Year-round)"
        ]
    }
    
    return calendar
