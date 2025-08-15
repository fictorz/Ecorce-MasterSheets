# from flask import Flask, request, jsonify, render_template, send_file, session
# import stripe
# import os  # Import the os module
# import library.lawyerup.question_flow as question_flow
# import os

import secrets

# stripe.api_key = app.config['STRIPE_SECRET_KEY']

class AppEngine:
    def __init__(self): #, stripe_api_key):
        self.temp_storage = {}
        #stripe_api_key
    
    def new_checkout(self, request):
                
        # Get input data from the frontend (adjust as needed)
        data = request.get_json()
        input_text1 = data.get('inputText1')
        input_text2 = data.get('inputText2')  # Add more as needed

        legal_name1 = data.get('legalName1')
        legal_name2 = data.get('legalName2')  # Add more as needed

        token = secrets.token_hex(16)  # 32-character hex string

        # Store in memory (can also write to Redis, file, or db)
        received_inputs = f"Received: name {legal_name1}, {input_text1} and name {legal_name2}, {input_text2} "
        print(received_inputs)

        print("Token = " + token)
        self.temp_storage[token] = (legal_name1, input_text1, legal_name2, input_text2)

        return token

    def get_data_from_token(self, token):
        data = self.temp_storage.get(token)
        print("Token = " + token)
        if not data:
            return "Invalid or expired token", 404
        
        return data