from datetime import datetime, timedelta
import json
import os

def get_crop_calendar(crop_name, planting_date=None):
    """Get farming calendar for a specific crop"""
    
    crop_schedules = {
        'Rice (Paddy)': {
            'duration_days': 120,
            'stages': [
                {'name': 'Land Preparation', 'days': 7, 'activities': ['Ploughing', 'Leveling', 'Bund repair']},
                {'name': 'Nursery Preparation', 'days': 25, 'activities': ['Seed treatment', 'Nursery bed preparation', 'Sowing']},
                {'name': 'Transplanting', 'days': 5, 'activities': ['Field preparation', 'Transplant seedlings', 'Gap filling']},
                {'name': 'Vegetative Stage', 'days': 40, 'activities': ['Irrigation', 'Weeding', 'First fertilizer dose']},
                {'name': 'Reproductive Stage', 'days': 30, 'activities': ['Second fertilizer dose', 'Pest monitoring', 'Disease control']},
                {'name': 'Maturity & Harvest', 'days': 13, 'activities': ['Stop irrigation', 'Harvesting', 'Threshing']}
            ],
            'fertilizer_schedule': [
                {'days': 15, 'fertilizer': 'Urea - 25 kg/acre', 'stage': 'After transplanting'},
                {'days': 40, 'fertilizer': 'Urea - 25 kg/acre', 'stage': 'Tillering stage'},
                {'days': 60, 'fertilizer': 'Urea - 15 kg/acre', 'stage': 'Panicle initiation'}
            ]
        },
        'Coconut': {
            'duration_days': 365,
            'stages': [
                {'name': 'Year-round Care', 'days': 365, 'activities': ['Regular watering', 'Manuring', 'Pest control']}
            ],
            'fertilizer_schedule': [
                {'days': 90, 'fertilizer': 'Organic manure - 25 kg/palm', 'stage': 'Pre-monsoon'},
                {'days': 180, 'fertilizer': 'NPK - 1.3 kg/palm', 'stage': 'Monsoon'},
                {'days': 270, 'fertilizer': 'Organic manure - 25 kg/palm', 'stage': 'Post-monsoon'}
            ]
        },
        'Pepper': {
            'duration_days': 240,
            'stages': [
                {'name': 'Planting', 'days': 15, 'activities': ['Pit preparation', 'Planting cuttings', 'Mulching']},
                {'name': 'Establishment', 'days': 60, 'activities': ['Regular watering', 'Training vines', 'Mulching']},
                {'name': 'Vegetative Growth', 'days': 90, 'activities': ['Fertilizer application', 'Pruning', 'Pest control']},
                {'name': 'Flowering & Fruiting', 'days': 75, 'activities': ['Increased irrigation', 'Nutrient spray', 'Disease control']}
            ],
            'fertilizer_schedule': [
                {'days': 45, 'fertilizer': 'Organic manure - 10 kg/vine', 'stage': 'After planting'},
                {'days': 120, 'fertilizer': 'NPK - 100:60:140 g/vine', 'stage': 'Growth stage'},
                {'days': 180, 'fertilizer': 'NPK - 100:60:140 g/vine', 'stage': 'Flowering stage'}
            ]
        },
        'Banana': {
            'duration_days': 365,
            'stages': [
                {'name': 'Planting', 'days': 15, 'activities': ['Pit preparation', 'Sucker selection', 'Planting']},
                {'name': 'Vegetative Phase', 'days': 120, 'activities': ['Irrigation', 'Mulching', 'Earthing up']},
                {'name': 'Flowering Phase', 'days': 90, 'activities': ['Bunch care', 'Propping', 'Denavelling']},
                {'name': 'Fruiting & Harvest', 'days': 140, 'activities': ['Bunch covering', 'Harvesting', 'Post-harvest']}
            ],
            'fertilizer_schedule': [
                {'days': 30, 'fertilizer': 'FYM - 10 kg/plant', 'stage': 'After planting'},
                {'days': 60, 'fertilizer': 'NPK - 200:100:300 g/plant', 'stage': 'Vegetative'},
                {'days': 120, 'fertilizer': 'NPK - 200:100:300 g/plant', 'stage': 'Pre-flowering'}
            ]
        }
    }
    
    if crop_name not in crop_schedules:
        crop_name = 'Rice (Paddy)'  # Default
    
    schedule = crop_schedules[crop_name]
    
    if planting_date is None:
        planting_date = datetime.now()
    elif isinstance(planting_date, str):
        planting_date = datetime.fromisoformat(planting_date)
    
    # Generate timeline
    timeline = []
    current_date = planting_date
    
    for stage in schedule['stages']:
        end_date = current_date + timedelta(days=stage['days'])
        timeline.append({
            'stage': stage['name'],
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'duration_days': stage['days'],
            'activities': stage['activities']
        })
        current_date = end_date
    
    # Generate fertilizer schedule
    fertilizer_timeline = []
    for fert in schedule['fertilizer_schedule']:
        fert_date = planting_date + timedelta(days=fert['days'])
        fertilizer_timeline.append({
            'date': fert_date.strftime('%Y-%m-%d'),
            'fertilizer': fert['fertilizer'],
            'stage': fert['stage']
        })
    
    return {
        'crop': crop_name,
        'planting_date': planting_date.strftime('%Y-%m-%d'),
        'harvest_date': (planting_date + timedelta(days=schedule['duration_days'])).strftime('%Y-%m-%d'),
        'total_duration': schedule['duration_days'],
        'timeline': timeline,
        'fertilizer_schedule': fertilizer_timeline
    }

def get_user_reminders(mobile):
    """Get reminders for a user"""
    from utils.auth_helper import get_user_data
    
    user_data = get_user_data(mobile)
    if not user_data:
        return []
    
    return user_data.get('reminders', [])

def add_reminder(mobile, reminder_data):
    """Add a reminder for user"""
    from utils.auth_helper import get_user_data, update_user_data
    
    user_data = get_user_data(mobile)
    if not user_data:
        return False
    
    reminders = user_data.get('reminders', [])
    reminders.append({
        'id': len(reminders) + 1,
        'created_at': datetime.now().isoformat(),
        **reminder_data
    })
    
    update_user_data(mobile, {'reminders': reminders})
    return True

def get_upcoming_tasks(mobile, days=7):
    """Get upcoming farming tasks for user"""
    from utils.auth_helper import get_user_data
    
    user_data = get_user_data(mobile)
    if not user_data:
        return []
    
    upcoming_tasks = []
    today = datetime.now()
    
    # Check reminders
    for reminder in user_data.get('reminders', []):
        reminder_date = datetime.fromisoformat(reminder['date'])
        days_until = (reminder_date - today).days
        
        if 0 <= days_until <= days:
            upcoming_tasks.append({
                'type': 'reminder',
                'date': reminder['date'],
                'days_until': days_until,
                'title': reminder['title'],
                'description': reminder.get('description', '')
            })
    
    # Check crop calendars
    for crop in user_data.get('crops', []):
        calendar = get_crop_calendar(crop['name'], crop['planting_date'])
        
        # Check fertilizer schedule
        for fert in calendar['fertilizer_schedule']:
            fert_date = datetime.fromisoformat(fert['date'])
            days_until = (fert_date - today).days
            
            if 0 <= days_until <= days:
                upcoming_tasks.append({
                    'type': 'fertilizer',
                    'date': fert['date'],
                    'days_until': days_until,
                    'title': f"{crop['name']} - Fertilizer Application",
                    'description': fert['fertilizer']
                })
        
        # Check stage transitions
        for stage in calendar['timeline']:
            stage_date = datetime.fromisoformat(stage['end_date'])
            days_until = (stage_date - today).days
            
            if 0 <= days_until <= days:
                upcoming_tasks.append({
                    'type': 'stage',
                    'date': stage['end_date'],
                    'days_until': days_until,
                    'title': f"{crop['name']} - {stage['stage']} Complete",
                    'description': ', '.join(stage['activities'])
                })
    
    # Sort by date
    upcoming_tasks.sort(key=lambda x: x['days_until'])
    
    return upcoming_tasks

def add_crop_to_user(mobile, crop_name, planting_date, area_acres):
    """Add a crop to user's farming calendar"""
    from utils.auth_helper import get_user_data, update_user_data
    
    user_data = get_user_data(mobile)
    if not user_data:
        return False
    
    crops = user_data.get('crops', [])
    crops.append({
        'name': crop_name,
        'planting_date': planting_date,
        'area_acres': area_acres,
        'added_at': datetime.now().isoformat()
    })
    
    update_user_data(mobile, {'crops': crops})
    return True
