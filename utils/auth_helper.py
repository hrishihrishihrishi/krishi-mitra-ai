import streamlit as st
import json
import os
from datetime import datetime
import hashlib

def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def register_user(name, location, mobile, password):
    """Register a new user"""
    users = load_users()
    
    if mobile in users:
        return False, "Mobile number already registered"
    
    users[mobile] = {
        'name': name,
        'location': location,
        'mobile': mobile,
        'password': hash_password(password),
        'registered_at': datetime.now().isoformat(),
        'crops': [],
        'reminders': []
    }
    
    save_users(users)
    return True, "Registration successful"

def login_user(mobile, password):
    """Login user"""
    users = load_users()
    
    if mobile not in users:
        return False, "Mobile number not found"
    
    if users[mobile]['password'] != hash_password(password):
        return False, "Incorrect password"
    
    return True, users[mobile]

def get_user_data(mobile):
    """Get user data by mobile number"""
    users = load_users()
    return users.get(mobile, None)

def update_user_data(mobile, data):
    """Update user data"""
    users = load_users()
    if mobile in users:
        users[mobile].update(data)
        save_users(users)
        return True
    return False
