import requests
from django.conf import settings

def send_donation_sms(phone_number, donor_name, donation_for):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'Fnet',
        "recipient[]": phone_number,
        "message": f"Dear {donor_name}, thank you so much for your kind donation towards the funeral of {donation_for}. Your support during this difficult time means a lot to the family. God richly bless you.",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None


def send_donation_thanksgiving_sms(phone_number, donor_name):
    endpoint = "https://api.mnotify.com/api/sms/quick"
    apiKey = settings.MNOTIFY_API_KEY
    payload = {
        "key": apiKey,
        "sender": 'Fnet',
        "recipient[]": phone_number,
        "message": f"Dear {donor_name}, thank you so much for your generous support during our time of loss. Your kind donation and presence brought us comfort and strength. We deeply appreciate your thoughtfulness. God richly bless you.",
        "is_schedule": False,
        "schedule_date": ''
    }
    

    url = endpoint + '?key=' + apiKey
    
   
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None
