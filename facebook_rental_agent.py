import os
import json
import random
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FacebookRentalAgent:
    def __init__(self, model_name: str = "tinyllama:latest"):
        """Initialize the Facebook Rental Agent for Isla Vista apartment posts using Ollama."""
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model_name = model_name
        self.apartment_details = {
            "location": "Isla Vista, CA",
            "address": "6777 Del Playa Dr, Isla Vista, CA 93117",
            "bedrooms": 4,
            "bathrooms": 2,
            "sqft": "1,493",
            "room_availability": {
                "triple_room": "1 available immediately",
                "double_room": "1 available immediately"
            },
            "pricing": {
                "rent": "$1,500",
                "deposit": "$1,500",
                "first_month": "$1,500",
                "last_month": "$1,500",
                "total_due_at_signing": "$4,500"
            },
            "target_audience": ["UCSB students", "SBCC students"],
            "features": [
                "Walking distance to UCSB campus",
                "Close to SBCC",
                "Beachfront location",
                "Great location on the beach",
                "Shared back patio with sea views",
                "High-end stainless steel appliances",
                "On-site laundry facilities",
                "Proximity to local park",
                "Secure 5-unit complex",
                "Elegant coastal living",
                "Virtual tour available"
            ],
            "amenities": [
                "Utilities included",
                "WiFi included",
                "Furnished",
                "Beach access",
                "Walking distance to UCSB and SBCC",
                "Washer/Dryer in unit",
                "Dishwasher",
                "Balcony with ocean view"
            ],
            "posting_frequency": "daily",
            "tone": "friendly, professional, student-focused",
            "contact": {
                "phone": "(805) 555-0123",
                "email": "leasing@playalifeiv.com",
                "virtual_tour": "https://playalifeiv.com/virtual-tour"
            }
        }
        
        # Post templates and themes
        self.post_themes = [
            "campus_proximity",
            "beach_lifestyle", 
            "student_community",
            "affordability",
            "convenience",
            "move_in_ready",
            "neighborhood_highlights"
        ]
        
        self.post_templates = {
            "campus_proximity": [
                "{address} – {campus} Students Welcome!\nSlide through to tour this prime location gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nGreat location on the beach, walk to {campus}\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "{campus} STUDENTS! Your dream apartment is here!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nWalking distance to {campus} campus\nGreat location on the beach\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Roll out of bed and walk to {campus}!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nNo more long commutes - everything is walkable!\nGreat location on the beach\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "{campus} LIFE just got better!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nSteps away from campus + beach vibes = perfect student life!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "{campus} STUDENTS: Your perfect spot is here!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nPrime location: Beach + {campus} walking distance\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ],
            "beach_lifestyle": [
                "{address} – Oceanfront Unit Available!\nSlide through to tour this oceanfront gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nGreat location on the beach with stunning sea views\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "OCEANFRONT LIVING for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nWake up to ocean views every day!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Surf, study, repeat at {address}!\n{bedrooms} bed / {bathrooms} bath oceanfront unit\n1 Triple room OR 1 Double room available immediately!\nBeach access + {campus} proximity = student paradise!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Beach vibes meet {campus} life!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nPerfect for students who want the ultimate coastal experience!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Sunset views from your {campus} apartment!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nOceanfront living with easy campus access!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ],
            "student_community": [
                "{address} – Student Community Living!\nSlide through to tour this student-friendly gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nJoin the {campus} community in great beach location\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Join the {campus} community at {address}!\n{bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nConnect with fellow students in this vibrant beach community!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "{campus} STUDENT LIFE at its finest!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nJoin the best student community in Isla Vista!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "{campus} FRIENDSHIP starts here!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nBuild lasting connections in this student-friendly beach community!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "{campus} COMMUNITY VIBES!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nExperience the best of student life in this beachfront community!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ],
            "affordability": [
                "{address} – Affordable Student Housing!\nSlide through to tour this budget-friendly gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nStudent-friendly pricing in great beach location\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "BUDGET-FRIENDLY {campus} living!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nQuality housing that won't break the bank!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Perfect balance: Location + Affordability!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nGreat value for {campus} students in prime beach location!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Student budget approved! {address}\n{bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nAffordable luxury for {campus} students!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Best value for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nPremium location at student-friendly prices!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ],
            "convenience": [
                "{address} – Convenient Student Living!\nSlide through to tour this convenient location gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nEverything within walking distance, great beach location\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Everything within walking distance!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\n{campus}, beach, shops, food - all nearby!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Convenience meets {campus} life!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nWalk to everything you need!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "No car needed! Everything is walkable!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\n{campus}, beach, restaurants, shopping - all steps away!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Ultimate convenience for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nLocation that makes student life easy!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ],
            "move_in_ready": [
                "{address} – Move-In Ready!\nSlide through to tour this ready-to-go gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nAvailable now in great beach location\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Move-in ready for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nNo waiting - your new home is ready now!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Ready for immediate move-in!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nPerfect for {campus} students who need housing now!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Available immediately for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nNo delays - move in when you're ready!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Instant availability for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nYour new home is waiting for you!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ],
            "neighborhood_highlights": [
                "{address} – Isla Vista Living!\nSlide through to tour this IV gem {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nHeart of student life in great beach location\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Experience the best of Isla Vista!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nThe ultimate {campus} student experience!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "IV LIFE at its finest!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nPrime location in the heart of student life!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "Premium Isla Vista location!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nThe best spot for {campus} students in IV!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!",
                "IV living redefined for {campus} students!\n{address} - {bedrooms} bed / {bathrooms} bath\n1 Triple room OR 1 Double room available immediately!\nExperience the magic of Isla Vista!\nRent: {rent}/month\nDue at signing: {deposit} deposit + {first_month} first month + {last_month} last month = {total_due_at_signing} total\nVirtual tour: {virtual_tour}\nDM to apply or set up a tour!"
            ]
        }

    def _call_ollama(self, prompt: str) -> str:
        """Make a call to Ollama API."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 150,
                        "num_predict": 100
                    }
                },
                timeout=15  # Much shorter timeout for small model
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                print(f"Ollama API error: {response.status_code}")
                return ""
                
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return ""

    def _check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def generate_daily_post(self) -> Dict[str, Any]:
        """Generate a daily Facebook post for apartment rental."""
        # Select a random theme for today
        theme = random.choice(self.post_themes)
        
        # Prioritize UCSB students (70% chance), SBCC secondary (30% chance)
        campus = random.choices(["UCSB", "SBCC"], weights=[0.7, 0.3])[0]
        
        # 50% chance to use main templates, 50% chance to use fallback templates
        use_main_templates = random.choice([True, False])
        
        if use_main_templates:
            # Use main templates with formatting
            template = random.choice(self.post_templates[theme])
            
            # Format template with apartment details
            formatted_template = template.format(
                address=self.apartment_details["address"],
                bedrooms=self.apartment_details["bedrooms"],
                bathrooms=self.apartment_details["bathrooms"],
                campus=campus,
                virtual_tour=self.apartment_details["contact"]["virtual_tour"],
                rent=self.apartment_details["pricing"]["rent"],
                deposit=self.apartment_details["pricing"]["deposit"],
                first_month=self.apartment_details["pricing"]["first_month"],
                last_month=self.apartment_details["pricing"]["last_month"],
                total_due_at_signing=self.apartment_details["pricing"]["total_due_at_signing"]
            )
            
            post_content = formatted_template
            model_used = "template"
            
        else:
            # Use fallback templates for variety
            fallback_templates = {
                "campus_proximity": [
                    f"{campus} students! Your perfect spot is here!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nWalking distance to {campus} campus\nGreat location on the beach\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Roll out of bed and walk to {campus}!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nNo more long commutes - everything is walkable!\nGreat location on the beach\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"{campus} LIFE just got better!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nSteps away from campus + beach vibes = perfect student life!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ],
                "beach_lifestyle": [
                    f"OCEANFRONT LIVING for {campus} students!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nWake up to ocean views every day!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Surf, study, repeat at {self.apartment_details['address']}!\n{self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath oceanfront unit\n1 Triple room OR 1 Double room available immediately!\nBeach access + {campus} proximity = student paradise!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Beach vibes meet {campus} life!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nPerfect for students who want the ultimate coastal experience!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ],
                "student_community": [
                    f"Join the {campus} community at {self.apartment_details['address']}!\n{self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nConnect with fellow students in this vibrant beach community!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"{campus} STUDENT LIFE at its finest!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nJoin the best student community in Isla Vista!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"{campus} FRIENDSHIP starts here!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nBuild lasting connections in this student-friendly beach community!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ],
                "affordability": [
                    f"BUDGET-FRIENDLY {campus} living!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nQuality housing that won't break the bank!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Perfect balance: Location + Affordability!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nGreat value for {campus} students in prime beach location!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Student budget approved! {self.apartment_details['address']}\n{self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nAffordable luxury for {campus} students!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ],
                "convenience": [
                    f"Everything within walking distance!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\n{campus}, beach, shops, food - all nearby!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Convenience meets {campus} life!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nWalk to everything you need!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"No car needed! Everything is walkable!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\n{campus}, beach, restaurants, shopping - all steps away!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ],
                "move_in_ready": [
                    f"Move-in ready for {campus} students!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nNo waiting - your new home is ready now!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Ready for immediate move-in!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nPerfect for {campus} students who need housing now!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Available immediately for {campus} students!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nNo delays - move in when you're ready!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ],
                "neighborhood_highlights": [
                    f"Experience the best of Isla Vista!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nThe ultimate {campus} student experience!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"IV LIFE at its finest!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nPrime location in the heart of student life!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!",
                    f"Premium Isla Vista location!\n{self.apartment_details['address']} - {self.apartment_details['bedrooms']} bed / {self.apartment_details['bathrooms']} bath\n1 Triple room OR 1 Double room available immediately!\nThe best spot for {campus} students in IV!\nRent: {self.apartment_details['pricing']['rent']}/month\nDue at signing: {self.apartment_details['pricing']['deposit']} deposit + {self.apartment_details['pricing']['first_month']} first month + {self.apartment_details['pricing']['last_month']} last month = {self.apartment_details['pricing']['total_due_at_signing']} total\nVirtual tour: {self.apartment_details['contact']['virtual_tour']}\nDM to apply or set up a tour!"
                ]
            }
            
            template = random.choice(fallback_templates.get(theme, fallback_templates["campus_proximity"]))
            post_content = template
            model_used = "fallback"
        
        # Create the full post (no hashtags or creative styling)
        full_post = post_content
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "theme": theme,
            "target_campus": campus,
            "content": post_content,
            "hashtags": "",
            "full_post": full_post,
            "character_count": len(full_post),
            "model_used": model_used,
            "creative_style": "clean"
        }

    def schedule_weekly_posts(self) -> List[Dict[str, Any]]:
        """Generate a week's worth of posts."""
        posts = []
        for i in range(7):
            # Simulate different days
            post_date = datetime.now() + timedelta(days=i)
            post = self.generate_daily_post()
            post["date"] = post_date.strftime("%Y-%m-%d")
            posts.append(post)
        return posts

    def save_post_to_file(self, post: Dict[str, Any], filename: str = None):
        """Save the generated post to a file."""
        if not filename:
            filename = f"facebook_post_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(post, f, indent=2)
        
        print(f"Post saved to {filename}")

    def list_available_models(self) -> List[str]:
        """List available Ollama models."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model['name'] for model in models]
            return []
        except:
            return []



def preview_post(post: Dict[str, Any]):
    """Display a formatted preview of the Facebook post."""
    print("\n" + "="*60)
    print("📱 FACEBOOK POST PREVIEW")
    print("="*60)
    
    # Post metadata
    print(f"📅 Date: {post['date']}")
    print(f"🎯 Target Audience: {post['target_campus']} students")
    print(f"📌 Theme: {post['theme'].replace('_', ' ').title()}")
    print(f"🤖 Generated by: {post.get('model_used', 'unknown')}")
    print(f"🎨 Creative Style: {post.get('creative_style', 'standard').replace('_', ' ').title()}")
    print(f"📊 Character count: {post['character_count']}")
    
    if 'note' in post:
        print(f"⚠️  Note: {post['note']}")
    
    print("\n" + "-"*60)
    print("📝 POST CONTENT:")
    print("-"*60)
    print(post['content'])
    print("-"*60)
    
    # Facebook preview simulation
    print("\n📱 HOW IT WOULD LOOK ON FACEBOOK:")
    print("─" * 40)
    print(f"🏠 Your Name • {post['date']}")
    print("─" * 40)
    print(post['content'])
    print("─" * 40)
    print("👍 Like • 💬 Comment • 🔄 Share")
    print("="*60)

def test_post_generation(agent: FacebookRentalAgent, num_posts: int = 3):
    """Test and preview multiple posts."""
    print(f"\n🧪 TESTING POST GENERATION ({num_posts} posts)")
    print("="*60)
    
    for i in range(num_posts):
        print(f"\n🔄 Generating test post {i+1}/{num_posts}...")
        post = agent.generate_daily_post()
        preview_post(post)
        
        if i < num_posts - 1:
            input("\n⏸️  Press Enter to generate next post...")

def main():
    """Main function to run the Facebook Rental Agent."""
    print("🏠 Facebook Rental Agent for Isla Vista (Ollama Edition)")
    print("=" * 60)
    
    # Check Ollama connection
    agent = FacebookRentalAgent()
    
    if not agent._check_ollama_connection():
        print("❌ Ollama is not running or not accessible!")
        print("💡 Please start Ollama first:")
        print("   1. Install Ollama: https://ollama.ai/")
        print("   2. Start Ollama: ollama serve")
        print("   3. Pull a model: ollama pull llama2")
        print("   4. Run this script again")
        return
    
    # Show available models
    models = agent.list_available_models()
    if models:
        print(f"✅ Ollama connected! Available models: {', '.join(models)}")
    else:
        print("⚠️  Ollama connected but no models found. Pull a model with: ollama pull llama2")
    
    # Main menu
    while True:
        print("\n" + "="*60)
        print("🎯 MAIN MENU")
        print("="*60)
        print("1. 📝 Generate today's post")
        print("2. 🧪 Test multiple posts")
        print("3. 📅 Generate weekly posts")
        print("4. 🎲 Generate random theme post")
        print("5. 📊 Show post statistics")
        print("6. 🚪 Exit")
        print("="*60)
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            # Generate today's post
            print(f"\n📝 Generating today's Facebook post using {agent.model_name}...")
            today_post = agent.generate_daily_post()
            preview_post(today_post)
            
            # Save option
            save_choice = input("\n💾 Save this post to file? (y/n): ").lower()
            if save_choice == 'y':
                agent.save_post_to_file(today_post)
            
        elif choice == "2":
            # Test multiple posts
            try:
                num_posts = int(input("How many test posts to generate? (1-10): "))
                num_posts = max(1, min(10, num_posts))
                test_post_generation(agent, num_posts)
            except ValueError:
                test_post_generation(agent, 3)
                
        elif choice == "3":
            # Generate weekly posts
            print("\n📅 Generating weekly posts...")
            weekly_posts = agent.schedule_weekly_posts()
            
            for i, post in enumerate(weekly_posts, 1):
                print(f"\n--- Day {i} ({post['date']}) ---")
                preview_post(post)
                
                if i < len(weekly_posts):
                    input("\n⏸️  Press Enter for next post...")
            
            # Save weekly posts
            save_choice = input("\n💾 Save all weekly posts to file? (y/n): ").lower()
            if save_choice == 'y':
                filename = f"weekly_posts_{datetime.now().strftime('%Y%m%d')}.json"
                with open(filename, "w") as f:
                    json.dump(weekly_posts, f, indent=2)
                print(f"✅ Weekly posts saved to {filename}")
                
        elif choice == "4":
            # Generate random theme post
            theme = random.choice(agent.post_themes)
            print(f"\n🎲 Generating post with theme: {theme.replace('_', ' ').title()}")
            post = agent.generate_daily_post()
            preview_post(post)
            
        elif choice == "5":
            # Show post statistics
            print("\n📊 POST GENERATION STATISTICS")
            print("="*40)
            print(f"Available themes: {len(agent.post_themes)}")
            print(f"Target campuses: {len(agent.apartment_details['target_audience'])}")
            print(f"Apartment features: {len(agent.apartment_details['features'])}")
            print(f"Model being used: {agent.model_name}")
            print(f"Ollama URL: {agent.ollama_url}")
            
        elif choice == "6":
            print("\n👋 Thanks for using the Facebook Rental Agent!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-6.")
        
        if choice in ["1", "2", "3", "4"]:
            input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()