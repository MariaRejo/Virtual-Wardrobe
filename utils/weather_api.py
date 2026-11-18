import requests

def get_current_weather(city="Chennai"):
    # Simple Logic for Demo
    # Unaku viva-la "Hot" nu varanum na 'return "Hot"' nu podu
    # Real weather venum na API use pannalam.
    
    try:
        # Dummy logic: Chennai is always Hot for demo ;)
        return "Hot - Sunny ☀️"
    except:
        return "Normal"