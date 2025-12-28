# Spanish Verb Conjugation Practice 🎯

A fun and interactive web application for practicing Spanish verb conjugation, inspired by Duolingo's engaging learning approach.

## Features

- 🎮 **Gamified Learning**: Score points, build streaks, and track your best performance
- 📊 **Progress Tracking**: Visual progress bar and real-time statistics
- 🎯 **Multiple Choice**: Choose the correct conjugation from four options
- ⚡ **Instant Feedback**: Immediate confirmation with encouraging messages
- 🌟 **10+ Common Verbs**: Practice both regular and irregular verbs
- 📱 **Responsive Design**: Works great on desktop and mobile devices
- ⌨️ **Keyboard Shortcuts**: Use numbers 1-4 to quickly select answers

## Verb Coverage

### Regular Verbs
- hablar (to speak)
- comer (to eat)
- vivir (to live)

### Irregular Verbs
- ser (to be)
- estar (to be - location/condition)
- tener (to have)
- hacer (to do/make)
- ir (to go)
- decir (to say/tell)
- poder (to be able to)

## Tenses Covered
- **Presente** (Present tense)
- **Pretérito** (Preterite/Past tense)

## Installation

1. Make sure you have Python 3.7+ installed

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Start practicing! 🎉

## Running Tests

The application includes comprehensive unit and integration tests.

### Run all tests:
```bash
python run_tests.py
```

### Run specific test files:
```bash
# Unit tests
python -m unittest test_app.py

# Integration tests
python -m unittest test_integration.py
```

### Test Coverage

The test suite includes:
- **23 tests** covering all functionality
- **Unit tests** for verb database, Flask routes, and API endpoints
- **Integration tests** for complete user workflows
- **Coverage tests** for all verbs, tenses, and pronouns

Test categories:
- Verb database structure and validation
- JSON file integrity
- Flask API endpoints (`/`, `/api/question`, `/api/check`)
- Question generation and randomization
- Answer checking (correct/incorrect/case-insensitive)
- Complete user workflows
- Edge cases and error handling

## How to Play

1. **Read the Verb**: See the infinitive form and its English translation
2. **Check the Tense**: Note whether you need present or preterite
3. **See the Pronoun**: Look at which pronoun you need to conjugate for
4. **Select Your Answer**: Click the correct conjugation from the options
5. **Get Feedback**: Receive immediate feedback and track your score
6. **Keep Going**: Build your streak and improve your Spanish skills!

## Tips

- Focus on one tense at a time when starting out
- Pay attention to irregular verbs - they have unique patterns
- Use the streak counter as motivation to maintain accuracy
- Practice regularly for best results

## Future Enhancements

Potential features to add:
- More verb tenses (imperfect, future, conditional, subjunctive)
- Difficulty levels
- Timed challenges
- Verb conjugation charts
- Custom verb lists
- User accounts and progress saving
- Audio pronunciation
- Hints system

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Storage**: LocalStorage for best streak persistence

---

¡Buena suerte! (Good luck!) 🌟
