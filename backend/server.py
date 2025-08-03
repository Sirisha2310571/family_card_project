from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    age = request.form.get('age')
    address = request.form.get('address')
    document = request.files['document']
    
    # Save document
    doc_path = os.path.join('static/uploads', document.filename)
    document.save(doc_path)

    # Dummy response
    return jsonify({
        "status": "success",
        "message": "Form submitted successfully!",
        "predicted_approval_days": 4  # mock prediction
    })

if __name__ == '__main__':
    app.run(debug=True)
