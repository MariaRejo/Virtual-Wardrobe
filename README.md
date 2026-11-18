# Virtual Wardrobe

An AI-powered web app for managing your wardrobe and getting outfit suggestions. Upload photos of your clothes, let the app categorize them automatically, and get matching outfit ideas for different occasions.

**Built with:** Python · Flask · TensorFlow · OpenCV · SQLite

---

## Features

- **User accounts**: register, log in and keep your own private wardrobe.
- **Digital wardrobe**: upload photos of tops, pants, shoes and accessories and browse them in one place.
- **AI categorization**: choose `Auto` and the app detects the clothing category and color from the image (TensorFlow + OpenCV).
- **Manual override**: set the category, color, season and occasion yourself whenever you prefer.
- **Outfit recommendations**: pick an occasion (Casual, Formal, Party, ...) and get a Top + Pant + Shoe combination, with an optional accessory.
- **Profile stats**: see how many tops, pants and shoes you own at a glance.

---

## Tech Stack

| Layer      | Technology                    |
|------------|-------------------------------|
| Backend    | Python, Flask, Flask-SQLAlchemy |
| AI / Vision| TensorFlow, OpenCV, NumPy     |
| Database   | SQLite                        |
| Frontend   | HTML templates (Jinja2), CSS  |

---

## Project Structure

```
Virtual-Wardrobe/
├── app.py                  # Routes and main application logic
├── config.py               # Flask, database and upload folder setup
├── models.py               # User and Cloth database models
├── requirements.txt        # Python dependencies
├── dataset/                # Training images (accessories, pants, shoes, tops)
├── training/
│   ├── preprocess.py
│   └── train_model.py      # Trains the category model and saves models/recommender_model.h5
├── models/                 # Trained model (created by train_model.py)
├── utils/
│   ├── image_processing.py # analyze_image(): category + color detection
│   ├── recommend.py
│   └── weather_api.py
├── templates/              # HTML pages (login, register, wardrobe, upload, profile, recommend)
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/            # Uploaded clothing images (created automatically)
└── database/               # SQLite database (created automatically)
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MariaRejo/Virtual-Wardrobe.git
cd Virtual-Wardrobe
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the category model

The AI model is not stored in the repository. Create it once from the images in `dataset/`:

```bash
python training/train_model.py
```

This saves `models/recommender_model.h5`. Without it, choose the category manually when uploading.

### 5. Run the app

Run it from the project folder (the one that contains `app.py`):

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. The database and upload folders are created automatically on first run.

Optional: set a `SECRET_KEY` environment variable to a long random text. If it is not set, a temporary key is used and users are logged out each time the app restarts.

---

## How to Use

1. **Register** a new account and **log in**.
2. Go to **Upload** and add a photo of a clothing item.
   - Select `Auto` for category/color to let the AI decide, or choose them manually.
   - Set the **season** and **occasion**.
3. Open your **Wardrobe** to see everything you have uploaded.
4. Open **Recommend**, choose an occasion and get an outfit suggestion.
   - You need at least **1 top, 1 pant and 1 shoe** for that occasion.
5. Check your **Profile** for wardrobe statistics.

---

## Roadmap

- [ ] Real-time weather integration (currently a placeholder value)
- [ ] Color-coordination logic for smarter outfit matching
- [ ] Multiple outfit suggestions per request
- [x] Password hashing and secret key from environment variables
- [x] Image validation and unique filenames on upload
- [ ] Delete / edit clothing items
- [ ] Deployment guide (Render / Railway / PythonAnywhere)

---

## Contributing

Contributions, issues and feature requests are welcome. Fork the repo, create a branch, and open a pull request.

---

## Author

**Maria Rejo J**

GitHub: https://github.com/MariaRejo

Built with Python, Flask and TensorFlow.
