from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Spanish verb database with common verbs
VERBS = {
    'hablar': {
        'english': 'to speak',
        'type': 'regular',
        'presente': {
            'yo': 'hablo', 'tú': 'hablas', 'él/ella': 'habla',
            'nosotros': 'hablamos', 'vosotros': 'habláis', 'ellos': 'hablan'
        },
        'pretérito': {
            'yo': 'hablé', 'tú': 'hablaste', 'él/ella': 'habló',
            'nosotros': 'hablamos', 'vosotros': 'hablasteis', 'ellos': 'hablaron'
        }
    },
    'comer': {
        'english': 'to eat',
        'type': 'regular',
        'presente': {
            'yo': 'como', 'tú': 'comes', 'él/ella': 'come',
            'nosotros': 'comemos', 'vosotros': 'coméis', 'ellos': 'comen'
        },
        'pretérito': {
            'yo': 'comí', 'tú': 'comiste', 'él/ella': 'comió',
            'nosotros': 'comimos', 'vosotros': 'comisteis', 'ellos': 'comieron'
        }
    },
    'vivir': {
        'english': 'to live',
        'type': 'regular',
        'presente': {
            'yo': 'vivo', 'tú': 'vives', 'él/ella': 'vive',
            'nosotros': 'vivimos', 'vosotros': 'vivís', 'ellos': 'viven'
        },
        'pretérito': {
            'yo': 'viví', 'tú': 'viviste', 'él/ella': 'vivió',
            'nosotros': 'vivimos', 'vosotros': 'vivisteis', 'ellos': 'vivieron'
        }
    },
    'ser': {
        'english': 'to be',
        'type': 'irregular',
        'presente': {
            'yo': 'soy', 'tú': 'eres', 'él/ella': 'es',
            'nosotros': 'somos', 'vosotros': 'sois', 'ellos': 'son'
        },
        'pretérito': {
            'yo': 'fui', 'tú': 'fuiste', 'él/ella': 'fue',
            'nosotros': 'fuimos', 'vosotros': 'fuisteis', 'ellos': 'fueron'
        }
    },
    'estar': {
        'english': 'to be (location/condition)',
        'type': 'irregular',
        'presente': {
            'yo': 'estoy', 'tú': 'estás', 'él/ella': 'está',
            'nosotros': 'estamos', 'vosotros': 'estáis', 'ellos': 'están'
        },
        'pretérito': {
            'yo': 'estuve', 'tú': 'estuviste', 'él/ella': 'estuvo',
            'nosotros': 'estuvimos', 'vosotros': 'estuvisteis', 'ellos': 'estuvieron'
        }
    },
    'tener': {
        'english': 'to have',
        'type': 'irregular',
        'presente': {
            'yo': 'tengo', 'tú': 'tienes', 'él/ella': 'tiene',
            'nosotros': 'tenemos', 'vosotros': 'tenéis', 'ellos': 'tienen'
        },
        'pretérito': {
            'yo': 'tuve', 'tú': 'tuviste', 'él/ella': 'tuvo',
            'nosotros': 'tuvimos', 'vosotros': 'tuvisteis', 'ellos': 'tuvieron'
        }
    },
    'hacer': {
        'english': 'to do/make',
        'type': 'irregular',
        'presente': {
            'yo': 'hago', 'tú': 'haces', 'él/ella': 'hace',
            'nosotros': 'hacemos', 'vosotros': 'hacéis', 'ellos': 'hacen'
        },
        'pretérito': {
            'yo': 'hice', 'tú': 'hiciste', 'él/ella': 'hizo',
            'nosotros': 'hicimos', 'vosotros': 'hicisteis', 'ellos': 'hicieron'
        }
    },
    'ir': {
        'english': 'to go',
        'type': 'irregular',
        'presente': {
            'yo': 'voy', 'tú': 'vas', 'él/ella': 'va',
            'nosotros': 'vamos', 'vosotros': 'vais', 'ellos': 'van'
        },
        'pretérito': {
            'yo': 'fui', 'tú': 'fuiste', 'él/ella': 'fue',
            'nosotros': 'fuimos', 'vosotros': 'fuisteis', 'ellos': 'fueron'
        }
    },
    'decir': {
        'english': 'to say/tell',
        'type': 'irregular',
        'presente': {
            'yo': 'digo', 'tú': 'dices', 'él/ella': 'dice',
            'nosotros': 'decimos', 'vosotros': 'decís', 'ellos': 'dicen'
        },
        'pretérito': {
            'yo': 'dije', 'tú': 'dijiste', 'él/ella': 'dijo',
            'nosotros': 'dijimos', 'vosotros': 'dijisteis', 'ellos': 'dijeron'
        }
    },
    'poder': {
        'english': 'to be able to',
        'type': 'irregular',
        'presente': {
            'yo': 'puedo', 'tú': 'puedes', 'él/ella': 'puede',
            'nosotros': 'podemos', 'vosotros': 'podéis', 'ellos': 'pueden'
        },
        'pretérito': {
            'yo': 'pude', 'tú': 'pudiste', 'él/ella': 'pudo',
            'nosotros': 'pudimos', 'vosotros': 'pudisteis', 'ellos': 'pudieron'
        }
    }
}

PRONOUNS = ['yo', 'tú', 'él/ella', 'nosotros', 'vosotros', 'ellos']
TENSES = ['presente', 'pretérito']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question', methods=['GET'])
def get_question():
    """Generate a random verb conjugation question"""
    verb_infinitive = random.choice(list(VERBS.keys()))
    verb_data = VERBS[verb_infinitive]
    tense = random.choice(TENSES)
    pronoun = random.choice(PRONOUNS)
    
    correct_answer = verb_data[tense][pronoun]
    
    # Generate 3 wrong answers from other conjugations
    all_conjugations = []
    for t in TENSES:
        all_conjugations.extend(verb_data[t].values())
    
    wrong_answers = [conj for conj in all_conjugations if conj != correct_answer]
    wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
    
    # Combine and shuffle
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)
    
    return jsonify({
        'verb': verb_infinitive,
        'english': verb_data['english'],
        'pronoun': pronoun,
        'tense': tense,
        'tense_english': 'Present' if tense == 'presente' else 'Preterite',
        'options': all_answers,
        'correct_answer': correct_answer
    })

@app.route('/api/check', methods=['POST'])
def check_answer():
    """Check if the submitted answer is correct"""
    data = request.json
    user_answer = data.get('answer', '').strip().lower()
    correct_answer = data.get('correct_answer', '').strip().lower()
    
    is_correct = user_answer == correct_answer
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': data.get('correct_answer')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
