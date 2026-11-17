import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

# 👇 Imports Logic
from config import app, db
from models import User, Cloth
from utils.image_processing import analyze_image 

# --- DATABASE AUTO-CREATE ---
with app.app_context():
    db.create_all()
    print("✅ Database connected/created successfully!")

# --- ROUTES ---

@app.route('/')
def home():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    # 🛑 CRASH FIX: User database-la illana logout pannidu
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
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration Successful! Please Login.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
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

# 👇 INDHA ROUTE DHAAN MUKKIYAM (HYBRID LOGIC)
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
        
        # 1. Capture Form Inputs
        manual_category = request.form.get('category') # Auto / Top / Pant...
        manual_color = request.form.get('color')       # Auto / Black / Blue...
        manual_season = request.form.get('season')
        manual_occasion = request.form.get('occasion')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # 2. DEFAULT VALUES
            final_category = "Unknown"
            final_color = "Multi"

            # 3. AI LOGIC (Only if Auto is selected)
            if manual_category == "Auto" or manual_color == "Auto":
                try:
                    print(f"🧠 AI Analyzing: {filename}")
                    ai_cat, ai_col = analyze_image(filepath)
                    
                    # Smart Decision: If User said Auto, use AI. Else use User choice.
                    final_category = ai_cat if manual_category == "Auto" else manual_category
                    final_color = ai_col if manual_color == "Auto" else manual_color
                    
                    print(f"✅ Final Decision: {final_category} | {final_color}")
                except Exception as e:
                    print(f"⚠️ AI Error: {e}")
                    # Fallback if AI fails but User selected Auto (Default to Top/Multi)
                    final_category = manual_category if manual_category != "Auto" else "Top"
                    final_color = manual_color if manual_color != "Auto" else "Multi"
            else:
                # 4. MANUAL OVERRIDE (User Manually Selected Everything)
                print("👤 User Manual Override Active")
                final_category = manual_category
                final_color = manual_color

            # 5. SAVE TO DB
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
    
    # Filter by Occasion
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