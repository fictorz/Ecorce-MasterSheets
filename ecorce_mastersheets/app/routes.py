from flask import Blueprint, request, jsonify, render_template, send_file #, current_app 
from app.main_stripe import AppEngine
import os

bp = Blueprint('main', __name__)
ae = AppEngine()

# Move to main_stripe
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY") # current_app.config['STRIPE_SECRET_KEY']

# To filter and export
# from flask import Flask, request, jsonify, render_template, send_file, session

import library.lawyerup.question_flow as question_flow

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")  # default fallback

# --- Frontend Rendering ---
@bp.route("/")
def index():
    return render_template("index.html", stripe_pk=os.getenv("STRIPE_PUBLISHABLE_KEY"))

@bp.route('/download', methods=['POST'], endpoint="download_contract")
def download_contract():
    try:
        # Retrieve data from the session
        token = request.form['token']
        data = ae.get_data_from_token(token)

        (legal_name1, input_text1, legal_name2, input_text2) = data

        received_inputs = f"Processed: name {legal_name1}, {input_text1} and name {legal_name2}, {input_text2} "
        print(received_inputs)
        pdf_buffer = question_flow.lawyerup_process(legal_name1, input_text1, legal_name2, input_text2, False)

        # send_file handles the file transfer and sets appropriate headers.
        return send_file(
            pdf_buffer,
            as_attachment=True,  # Forces the browser to download, instead of displaying
            download_name='ContratDeResolution.pdf'  #  Optional: Set a custom filename
        )

    except Exception as e:
        print(f"Error in download_contract: {e}")  # Log the error for debugging
        return "An error occurred during download", 500  # Return a 500 error
    
# --- Payment Processing ---
@bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Get input data from the frontend (adjust as needed)
        data = request.get_json()
        # input_text1 = data.get('inputText1')
        # input_text2 = data.get('inputText2')  # Add more as needed

        token = ae.new_checkout(request)

        # --- Custom Logic (Placeholder) ---
        # processed_result = f"Processed: {input_text1} and {input_text2}"
        price_in_cents = 0  # Example 1000 = $10.00

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',  # Change if needed
                        'product_data': {
                            'name': 'My Product', # Customize
                        },
                        'unit_amount': price_in_cents,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{BASE_URL}/success?session_id={token}', #Change to deployed URL
            cancel_url=f'{BASE_URL}/cancel',  # Change to deployed URL
        )
        return jsonify({'id': checkout_session.id})

    except Exception as e:
        return jsonify(error=str(e)), 400

# --- Success/Cancel Routes (Simple) ---
@bp.route("/success")
def success():
    session_id = request.args.get('session_id')
    if not session_id:
        return "No session ID found", 400

    return render_template("success.html", token=session_id)

@bp.route("/cancel")
def cancel():
  return render_template("cancel.html")