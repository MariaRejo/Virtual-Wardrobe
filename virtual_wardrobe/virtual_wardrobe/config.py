import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setup Flask
app = Flask(__name__)
app.secret_key = 'super_secret_key_mamey' # Change this for production!

# === PATH SETUP ===
# Get the absolute path to the project directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# === DATABASE PATH ===
DB_FOLDER = os.path.join(BASE_DIR, 'database')
# Create database folder if it doesn't exist
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
    print(f"✅ Created database folder at: {DB_FOLDER}")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_FOLDER, 'wardrobe.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# === UPLOAD FOLDER (THE FIX) ===
# The folder must be 'static/uploads' to be served by the browser
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder automatically if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"✅ Created upload folder at: {UPLOAD_FOLDER}")
else:
    print(f"✅ Upload folder verified at: {UPLOAD_FOLDER}")

# Initialize Database
db = SQLAlchemy(app)