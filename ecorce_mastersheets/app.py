from flask import Flask, request, jsonify, render_template, send_file, session
import stripe
import os  # Import the os module
import library.lawyerup.question_flow as question_flow

import os

import tempfile

import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()





# Load environment variables from .env (recommended) or set directly
#  (less secure for production, but fine for quick prototyping).
# Create a .env file in your project root:

from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # ton fichier HTML placé dans templates/

@app.route("/process", methods=["POST"])
def process():
    # Récupération des champs
    uploaded_file = request.files.get("file")
    display_name = request.form.get("display_name", "")
    mode = request.form.get("mode", "code")  # "code" ou "question"
    content = request.form.get("content", "")

    # Sauvegarde du fichier si présent
    saved_path = None
    if uploaded_file and uploaded_file.filename:
        safe_filename = uploaded_file.filename  # à sécuriser si besoin (werkzeug.utils.secure_filename)
        saved_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        uploaded_file.save(saved_path)

    # Ici, tu peux ajouter ton traitement :
    # - utiliser `display_name` pour nommer/loguer
    # - `mode` pour savoir comment interpréter `content`
    # - `saved_path` pour lire le fichier sur disque
    # - `content` comme texte/code fourni par l'utilisateur

    print(f"Mode: {mode}")
    print(f"Nom affiché: {display_name}")
    print(f"Fichier sauvegardé: {saved_path}")
    print(f"Contenu: {content[:80]}{'...' if len(content) > 80 else ''}")

    # Redirection après traitement (ou rendre un template avec le résultat)
    return redirect(url_for("index"))

# Temporary in-memory or file-based storage
temp_storage = {}

# # --- Frontend Rendering ---
# @app.route("/")
# def index():
#     return render_template("index.html", stripe_pk=os.getenv("STRIPE_PUBLISHABLE_KEY"))

# @app.route('/download_contract')
# def download_contract():
@app.route('/download', methods=['POST'])
def download_contract():
    try:
        # Retrieve data from the session
        token = request.form['token']
        data = temp_storage.get(token)
        print("Token = " + token)
        if not data:
            return "Invalid or expired token", 404

        input_text1, input_text2 = data

        pdf_buffer = question_flow.lawyerup_process(input_text1,
            input_text2, False)
        
        # contract_data = session.pop('contract_data', None)  # Get and remove
        # if contract_data is None:
        #     return "No contract data found", 404

        # pdf_buffer = question_flow.lawyerup_process(contract_data['input_text1'],
        #     contract_data['input_text2'], False)
        
        
        # data = request.get_json()
        # input_text1 = data.get('inputText1')
        # input_text2 = data.get('inputText2')  # Add more as needed
    

        # print("Contract")
        # session_id = request.args.get('session_id') #Get session id
        # if session_id:
        #     checkout_session = stripe.checkout.Session.retrieve(session_id) #Retrieve the data
        #     python_pdf = checkout_session.metadata.get('python_pdf') # Get custom string
        #     print("Contract" + python_pdf)
        # BEST PRACTICE: Use os.path.join and absolute paths.  This makes it
        # work correctly regardless of where you run the script from.
        # Assume the contract file is in a 'contracts' folder in your project root.
        # contract_path = os.path.join(app.root_path, 'contracts', 'resolution_contract.pdf')

        # # Check if the file exists (important for security!)
        # if not os.path.exists(contract_path):
        #     return "Contract file not found", 404  # Return a 404 error

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
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Get input data from the frontend (adjust as needed)
        data = request.get_json()
        input_text1 = data.get('inputText1')
        input_text2 = data.get('inputText2')  # Add more as needed

        # Store the data in the Flask session.  This is the key change.
        # session['contract_data'] = {
        #     'input_text1': input_text1,
        #     'input_text2': input_text2,
        # }

        # Generate a unique ID
        # token = str(uuid.uuid4())

        token = secrets.token_hex(16)  # 32-character hex string

        # Store in memory (can also write to Redis, file, or db)
        print("Token = " + token)
        temp_storage[token] = (input_text1, input_text2)

        # python_pdf = question_flow.lawyerup_process(input_text1, input_text2, False)

        # --- Your Custom Logic (Placeholder) ---
        # This is where you'd call your backend scripts.
        # For now, just process the input data.  Replace this
        # with calls to your actual functions.
        processed_result = f"Processed: {input_text1} and {input_text2}"
        price_in_cents = 0  # Example 1000 = $10.00

        # store_contract_data(token, contract_string1, contract_string2)
        
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
            success_url=f'http://localhost:5000/success?session_id={token}', #Change to deployed URL
            cancel_url='http://localhost:5000/cancel',  # Change to deployed URL
            # Pass your processed data as metadata (optional)
            # metadata={
            #   'token': token,
            # }

            #               'python_pdf': python_pdf,
            #   'inputText1': input_text1,
            #   'inputText2': input_text2
        )
        return jsonify({'id': checkout_session.id})

    except Exception as e:
        return jsonify(error=str(e)), 400

# --- Success/Cancel Routes (Simple) ---
@app.route("/success")
def success():
    session_id = request.args.get('session_id')
    if not session_id:
        return "No session ID found", 400

    # try:
        # checkout_session = stripe.checkout.Session.retrieve(session_id)
        # token = checkout_session.metadata.get('token')
        # token
    #     input_text2 = checkout_session.metadata.get('input_text2')

    #     if input_text1 is None or input_text2 is None:
    #         return "Error: Required data missing from metadata.", 500

    #     pdf_buffer = question_flow.lawyerup_process(input_text1,
    #         input_text2, False)
    #     # pdf_buffer = generate_redacted_contract(
    #     #     "Party 1", "Party 2", input_text1, input_text2  # Replace with actual party names
    #     # )

    #     if pdf_buffer is None:
    #         return "Error generating contract.", 500

    #     return send_file(
    #         pdf_buffer,
    #         mimetype='application/pdf',
    #         download_name='resolution_contract.pdf',
    #         as_attachment=True
    #     )

    # except stripe.error.StripeError as e:
    #     print(f"Stripe error: {e}")
    #     return "Stripe error: " + str(e), 500
    # except Exception as e:
    #     print(f"Error in success route: {e}")
    #     return "An unexpected error occurred.", 500

    # session_id = request.args.get('session_id') #Get session id
    # if session_id:
    #     checkout_session = stripe.checkout.Session.retrieve(session_id) #Retrieve the data
    #     # python_pdf = checkout_session.metadata.get('python_pdf') # Get custom string
    #     input_text1 = checkout_session.metadata.get('input_text1') # Get custom string
    #     input_text2 = checkout_session.metadata.get('input_text2') # Get custom string
    #     python_pdf = question_flow.lawyerup_process(input_text1, input_text2, False)

    #     # Store the data in the Flask session.  This is the key change.
    #     session['contract_data'] = {
    #         'input_text1': input_text1,
    #         'input_text2': input_text2,
    #     }
    return render_template("success.html", token=session_id)

@app.route("/cancel")
def cancel():
  return render_template("cancel.html")

if __name__ == "__main__":
    app.run(debug=True)  # Use debug=True for development only