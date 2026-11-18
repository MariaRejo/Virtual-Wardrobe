import os
import random
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import app, db
from models import User, Cloth
from utils.image_processing import analyze_image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# --- DATABASE AUTO-CREATE ---
with app.app_context():
    db.create_all()
    print("Database connected/created successfully")


# --- HELPERS ---

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def verify_password(user, password):
    """Check a password against the stored hash.

    Accounts created before hashing was added still have a plain-text password.
    Those are accepted once and upgraded to a hash on that login.
    """
    if user.password.startswith(('scrypt:', 'pbkdf2:')):
        return check_password_hash(user.password, password)
    if user.password == password:
        user.password = generate_password_hash(password)
        db.session.commit()
        return True
    return False


# --- ROUTES ---

@app.route('/')
def home():
    if 'user_id' not in session: return redirect(url_for('login'))

    # If the user no longer exists in the database, log out
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    clothes = Cloth.query.filter_by(user_id=session['user_id']).all()
    return render_template('wardrobe.html', items=clothes, username=user.username)

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    all_clothes = Cloth.query.filter_by(user_id=session['user_id']).all()

    stats = {
        'tops': len([c for c in all_clothes if c.category == 'Top']),
        'pants': len([c for c in all_clothes if c.category == 'Pant']),
        'shoes': len([c for c in all_clothes if c.category == 'Shoe']),
        'total': len(all_clothes)
    }

    return render_template('profile.html', user=user, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required!')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash('Registration Successful! Please Login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and verify_password(user, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Invalid Username or Password!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# HYBRID LOGIC: the user can pick values manually, or choose "Auto" to let the AI decide
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session: return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files: return redirect(request.url)
        file = request.files['file']

        # 1. Capture form inputs (Auto / Top / Pant ...)
        manual_category = request.form.get('category', 'Auto')
        manual_color = request.form.get('color', 'Auto')
        manual_season = request.form.get('season', 'All')
        manual_occasion = request.form.get('occasion', 'Casual')

        if file and file.filename != '':
            # 2. Only accept image files
            if not allowed_file(file.filename):
                flash('Please upload a PNG, JPG, JPEG or WEBP image.')
                return redirect(url_for('upload'))

            # 3. Save with a unique name so two files with the same name never overwrite each other
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            final_category = manual_category
            final_color = manual_color

            # 4. AI logic (only when Auto is selected)
            if manual_category == "Auto" or manual_color == "Auto":
                ai_cat, ai_col = "Unknown", "Unknown"
                try:
                    print(f"AI analyzing: {filename}")
                    ai_cat, ai_col = analyze_image(filepath)
                except Exception as e:
                    print(f"AI Error: {e}")

                if manual_category == "Auto":
                    if ai_cat in ("Unknown", "Error"):
                        # Do not save a wrong category. Ask the user to choose it.
                        os.remove(filepath)
                        flash('AI could not detect the category. Please choose it manually.')
                        return redirect(url_for('upload'))
                    final_category = ai_cat

                if manual_color == "Auto":
                    final_color = "Multi" if ai_col in ("Unknown", "Error") else ai_col

                print(f"Final decision: {final_category} | {final_color}")
            else:
                print("User manual override active")

            # 5. Save to database
            new_cloth = Cloth(
                category=final_category,
                color=final_color,
                image_path=filename,
                season=manual_season,
                occasion=manual_occasion,
                user_id=session['user_id']
            )
            db.session.add(new_cloth)
            db.session.commit()

            return redirect(url_for('home'))

    return render_template('upload.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if 'user_id' not in session: return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    selected_occasion = "Casual"
    if request.method == 'POST':
        selected_occasion = request.form.get('occasion_selector')

    # Get all clothes
    all_clothes = Cloth.query.filter_by(user_id=session['user_id']).all()

    # Filter by occasion
    filtered_clothes = [c for c in all_clothes if c.occasion == selected_occasion or c.occasion == "All"]

    tops = [c for c in filtered_clothes if c.category == 'Top']
    pants = [c for c in filtered_clothes if c.category == 'Pant']
    shoes = [c for c in filtered_clothes if c.category == 'Shoe']
    accessories = [c for c in filtered_clothes if c.category == 'Accessory']

    suggestions = []

    # Suggest only if we have at least 1 Top, 1 Pant, 1 Shoe
    if len(tops) > 0 and len(pants) > 0 and len(shoes) > 0:
        outfit = {
            'top': random.choice(tops),
            'pant': random.choice(pants),
            'shoe': random.choice(shoes),
            'accessory': random.choice(accessories) if accessories else None
        }
        suggestions.append(outfit)

    return render_template('recommend.html', suggestions=suggestions, current_occasion=selected_occasion, weather="Hot - Sunny ☀️")

if __name__ == '__main__':
    app.run(debug=True)
