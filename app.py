from flask import Flask, render_template, jsonify, request
import random
import json
import os

app = Flask(__name__)

# Load verbs from JSON file
def load_verbs():
    verbs_path = os.path.join(os.path.dirname(__file__), 'verbs.json')
    with open(verbs_path, 'r', encoding='utf-8') as f:
        return json.load(f)

VERBS = load_verbs()

PRONOUNS = ['yo', 'tú', 'él/ella', 'nosotros', 'vosotros', 'ellos']
TENSES = ['presente', 'pretérito', 'imperfecto', 'futuro', 'condicional', 'perfecto', 'pluscuamperfecto', 'futuro perfecto']
TENSE_NAMES = {
    'presente': 'Presente',
    'pretérito': 'Pretérito',
    'imperfecto': 'Imperfecto',
    'futuro': 'Futuro',
    'condicional': 'Condicional',
    'perfecto': 'Pretérito Perfecto',
    'pluscuamperfecto': 'Pluscuamperfecto',
    'futuro perfecto': 'Futuro Perfecto'
}
TENSE_DESCRIPTIONS = {
    'presente': 'Used for current actions, habitual actions, and general truths.',
    'pretérito': 'Used for completed actions in the past with a specific time frame.',
    'imperfecto': 'Used for ongoing past actions, habitual past actions, and descriptions in the past.',
    'futuro': 'Used for actions that will happen in the future.',
    'condicional': 'Used for hypothetical situations, polite requests, and future actions from a past perspective.',
    'perfecto': 'Used for actions that happened in the recent past or have relevance to the present.',
    'pluscuamperfecto': 'Used for actions that had happened before another past action.',
    'futuro perfecto': 'Used for actions that will have been completed by a certain point in the future.'
}

# Regular verb conjugation hints
CONJUGATION_HINTS = {
    'presente': {
        '-ar': {'yo': '-o', 'tú': '-as', 'él/ella': '-a', 'nosotros': '-amos', 'vosotros': '-áis', 'ellos': '-an'},
        '-er': {'yo': '-o', 'tú': '-es', 'él/ella': '-e', 'nosotros': '-emos', 'vosotros': '-éis', 'ellos': '-en'},
        '-ir': {'yo': '-o', 'tú': '-es', 'él/ella': '-e', 'nosotros': '-imos', 'vosotros': '-ís', 'ellos': '-en'}
    },
    'pretérito': {
        '-ar': {'yo': '-é', 'tú': '-aste', 'él/ella': '-ó', 'nosotros': '-amos', 'vosotros': '-asteis', 'ellos': '-aron'},
        '-er': {'yo': '-í', 'tú': '-iste', 'él/ella': '-ió', 'nosotros': '-imos', 'vosotros': '-isteis', 'ellos': '-ieron'},
        '-ir': {'yo': '-í', 'tú': '-iste', 'él/ella': '-ió', 'nosotros': '-imos', 'vosotros': '-isteis', 'ellos': '-ieron'}
    },
    'imperfecto': {
        '-ar': {'yo': '-aba', 'tú': '-abas', 'él/ella': '-aba', 'nosotros': '-ábamos', 'vosotros': '-abais', 'ellos': '-aban'},
        '-er': {'yo': '-ía', 'tú': '-ías', 'él/ella': '-ía', 'nosotros': '-íamos', 'vosotros': '-íais', 'ellos': '-ían'},
        '-ir': {'yo': '-ía', 'tú': '-ías', 'él/ella': '-ía', 'nosotros': '-íamos', 'vosotros': '-íais', 'ellos': '-ían'}
    },
    'futuro': {
        '-ar': {'yo': '-é', 'tú': '-ás', 'él/ella': '-á', 'nosotros': '-emos', 'vosotros': '-éis', 'ellos': '-án'},
        '-er': {'yo': '-é', 'tú': '-ás', 'él/ella': '-á', 'nosotros': '-emos', 'vosotros': '-éis', 'ellos': '-án'},
        '-ir': {'yo': '-é', 'tú': '-ás', 'él/ella': '-á', 'nosotros': '-emos', 'vosotros': '-éis', 'ellos': '-án'}
    },
    'condicional': {
        '-ar': {'yo': '-ía', 'tú': '-ías', 'él/ella': '-ía', 'nosotros': '-íamos', 'vosotros': '-íais', 'ellos': '-ían'},
        '-er': {'yo': '-ía', 'tú': '-ías', 'él/ella': '-ía', 'nosotros': '-íamos', 'vosotros': '-íais', 'ellos': '-ían'},
        '-ir': {'yo': '-ía', 'tú': '-ías', 'él/ella': '-ía', 'nosotros': '-íamos', 'vosotros': '-íais', 'ellos': '-ían'}
    }
}

# Irregular verb hints - common patterns
IRREGULAR_HINTS = {
    'ser': '"Ser" is highly irregular. Memorize its forms: soy, eres, es, somos...',
    'estar': '"Estar" has irregular forms in pretérito: estuve, estuviste, estuvo...',
    'ir': '"Ir" shares pretérito forms with "ser": fui, fuiste, fue...',
    'tener': '"Tener" has stem change to teng- in yo form presente, and tuv- in pretérito',
    'hacer': '"Hacer" becomes hic- in pretérito (except él/ella: hizo)',
    'poder': '"Poder" is o→ue stem-changing and has irregular pretérito: pude, pudiste...',
    'poner': '"Poner" becomes pong- in yo presente, and pus- in pretérito',
    'decir': '"Decir" has many irregularities: digo in presente, dije in pretérito',
    'venir': '"Venir" becomes veng- in yo presente, vin- in pretérito, vendr- in futuro',
    'salir': '"Salir" becomes salg- in yo presente, and saldr- in futuro',
    'traer': '"Traer" becomes traig- in yo presente, and traj- in pretérito',
    'caer': '"Caer" becomes caig- in yo presente, and has spelling changes with í/y',
    'oír': '"Oír" becomes oig- in yo presente, and has spelling changes with í/y',
    'ver': '"Ver" has irregular participle "visto" and imperfecto: veía, veías...',
    'dar': '"Dar" is irregular in pretérito: di, diste, dio (no accent marks)',
    'saber': '"Saber" becomes sé in yo presente, and sup- in pretérito',
    'querer': '"Querer" is e→ie stem-changing and has irregular pretérito: quise, quisiste...',
    'parecer': '"Parecer" becomes parezc- in yo presente (like other -ecer verbs)',
    'conocer': '"Conocer" becomes conozc- in yo presente (like other -ocer verbs)',
    'seguir': '"Seguir" is e→i stem-changing and becomes sig- in some forms',
    'encontrar': '"Encontrar" is o→ue stem-changing in presente: encuentro, encuentras...',
    'sentir': '"Sentir" is e→ie stem-changing and also changes in pretérito él/ella: sintió',
    'pensar': '"Pensar" is e→ie stem-changing in presente: pienso, piensas...',
    'dormir': '"Dormir" is o→ue stem-changing and also changes in pretérito: durmió, durmieron',
    'pedir': '"Pedir" is e→i stem-changing in presente and pretérito: pido, pidió...',
    'escribir': '"Escribir" conjugates regularly but has irregular participle: escrito',
    'leer': '"Leer" has spelling changes i→y in pretérito: leyó, leyeron',
    'comenzar': '"Comenzar" is e→ie stem-changing and has z→c spelling change: comienzo, comencé',
    'morir': '"Morir" is o→ue stem-changing and has irregular participle: muerto',
    'abrir': '"Abrir" conjugates regularly but has irregular participle: abierto',
    'cerrar': '"Cerrar" is e→ie stem-changing in presente: cierro, cierras, cierra...',
    'volver': '"Volver" is o→ue stem-changing and has irregular participle: vuelto',
    'entender': '"Entender" is e→ie stem-changing in presente: entiendo, entiendes...'
}

# Pronoun identification hints based on verb endings
PRONOUN_HINTS = {
    'yo': 'Look for -o in presente, -é/-í in pretérito, -aba/-ía in imperfecto',
    'tú': 'Look for -s ending: -as/-es in presente, -aste/-iste in pretérito',
    'él/ella': 'Look for -a/-e in presente, -ó/-ió in pretérito (with accent!)',
    'nosotros': 'Look for -mos ending in all tenses',
    'vosotros': 'Look for -áis/-éis/-ís in presente, -ais/-eis in imperfecto',
    'ellos': 'Look for -n ending: -an/-en in presente, -aron/-ieron in pretérito'
}

# Tense identification hints
TENSE_ID_HINTS = {
    'presente': 'Present tense: Simple forms like hablo, comes, vive',
    'pretérito': 'Preterite: Look for accents on final syllable (habló, comí) or -aste/-iste endings',
    'imperfecto': 'Imperfect: Look for -aba (for -ar) or -ía (for -er/-ir) patterns',
    'futuro': 'Future: Full infinitive + endings with accents (hablaré, comeré)',
    'condicional': 'Conditional: Full infinitive + -ía endings (hablaría, comería)',
    'perfecto': 'Present perfect: Uses "he/has/ha/hemos/habéis/han" + past participle',
    'pluscuamperfecto': 'Pluperfect: Uses "había/habías/habíamos..." + past participle',
    'futuro perfecto': 'Future perfect: Uses "habré/habrás/habrá/habremos/habréis/habrán" + past participle'
}

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
    
    # Randomly select question type: 25% each
    rand = random.random()
    if rand < 0.25:
        question_type = 'identify-tense'
    elif rand < 0.50:
        question_type = 'identify-pronoun'
    elif rand < 0.75:
        question_type = 'identify-infinitive'
    else:
        question_type = 'conjugation'
    
    if question_type == 'identify-tense':
        # Show conjugated verb, ask for the tense
        # Generate options with tense names
        all_tense_names = list(TENSE_NAMES.values())
        correct_tense_name = TENSE_NAMES[tense]
        
        # Get wrong tense names (we have 5 tenses, so get up to 3 others)
        wrong_tenses = [t for t in all_tense_names if t != correct_tense_name]
        # Since we have 5 tenses, we'll get 3 wrong ones for a total of 4 options
        if len(wrong_tenses) > 3:
            wrong_tenses = random.sample(wrong_tenses, 3)
        
        # Combine and shuffle
        all_options = [correct_tense_name] + wrong_tenses
        random.shuffle(all_options)
        
        # Ensure all options are unique
        all_options = list(dict.fromkeys(all_options))
        
        return jsonify({
            'question_type': 'identify-tense',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'pronoun': pronoun,
            'conjugated_form': correct_answer,
            'tense': tense,
            'options': all_options,
            'correct_answer': correct_tense_name
        })
    elif question_type == 'identify-pronoun':
        # Show conjugated verb, ask for the pronoun
        # Generate options with pronouns
        correct_pronoun = pronoun
        
        # Get 3 wrong pronouns
        wrong_pronouns = [p for p in PRONOUNS if p != correct_pronoun]
        wrong_pronouns = random.sample(wrong_pronouns, min(3, len(wrong_pronouns)))
        
        # Combine and shuffle
        all_options = [correct_pronoun] + wrong_pronouns
        random.shuffle(all_options)
        
        # Ensure all options are unique
        all_options = list(dict.fromkeys(all_options))
        
        return jsonify({
            'question_type': 'identify-pronoun',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'tense': tense,
            'tense_name': TENSE_NAMES[tense],
            'conjugated_form': correct_answer,
            'pronoun': pronoun,
            'options': all_options,
            'correct_answer': correct_pronoun
        })
    elif question_type == 'identify-infinitive':
        # Show conjugated verb, ask for the infinitive
        # Generate options with verb infinitives
        correct_infinitive = verb_infinitive
        
        # Get 3 wrong infinitives
        all_verbs = list(VERBS.keys())
        wrong_infinitives = [v for v in all_verbs if v != correct_infinitive]
        wrong_infinitives = random.sample(wrong_infinitives, min(3, len(wrong_infinitives)))
        
        # Combine and shuffle
        all_options = [correct_infinitive] + wrong_infinitives
        random.shuffle(all_options)
        
        # Ensure all options are unique
        all_options = list(dict.fromkeys(all_options))
        
        return jsonify({
            'question_type': 'identify-infinitive',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'tense': tense,
            'tense_name': TENSE_NAMES[tense],
            'pronoun': pronoun,
            'conjugated_form': correct_answer,
            'options': all_options,
            'correct_answer': correct_infinitive
        })
    else:
        # Standard conjugation question
        # Generate 3 wrong answers from other conjugations
        all_conjugations = []
        for t in TENSES:
            all_conjugations.extend(verb_data[t].values())
        
        # Get unique wrong answers
        wrong_answers = [conj for conj in all_conjugations if conj != correct_answer]
        # Remove duplicates
        wrong_answers = list(set(wrong_answers))
        wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
        
        # Combine and shuffle
        all_answers = [correct_answer] + wrong_answers
        random.shuffle(all_answers)
        
        # Ensure all options are unique (should be, but double check)
        all_answers = list(dict.fromkeys(all_answers))
        
        return jsonify({
            'question_type': 'conjugation',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'pronoun': pronoun,
            'tense': tense,
            'tense_english': TENSE_NAMES[tense],
            'options': all_answers,
            'correct_answer': correct_answer
        })

@app.route('/api/check', methods=['POST'])
def check_answer():
    """Check if the submitted answer is correct"""
    data = request.json
    user_answer = data.get('answer', '').strip().lower()
    correct_answer = data.get('correct_answer', '').strip().lower()
    tense = data.get('tense', '')
    verb = data.get('verb', '')
    pronoun = data.get('pronoun', '')
    question_type = data.get('question_type', 'conjugation')
    
    is_correct = user_answer == correct_answer
    
    response = {
        'correct': is_correct,
        'correct_answer': data.get('correct_answer')
    }
    
    # Add tense description if tense is provided
    if tense and tense in TENSE_DESCRIPTIONS:
        response['tense_description'] = TENSE_DESCRIPTIONS[tense]
        response['tense_name'] = TENSE_NAMES[tense]
    
    # Add hints for wrong answers based on question type
    if not is_correct:
        # Conjugation hints
        if question_type == 'conjugation' and verb and tense and pronoun:
            verb_data = VERBS.get(verb, {})
            
            # Regular verb hint
            if verb_data.get('type') == 'regular' and tense in CONJUGATION_HINTS:
                if verb.endswith('ar'):
                    verb_ending = '-ar'
                elif verb.endswith('er'):
                    verb_ending = '-er'
                elif verb.endswith('ir'):
                    verb_ending = '-ir'
                else:
                    verb_ending = None
                
                if verb_ending and verb_ending in CONJUGATION_HINTS[tense]:
                    ending = CONJUGATION_HINTS[tense][verb_ending].get(pronoun, '')
                    if ending:
                        stem = verb[:-2]
                        if tense in ['futuro', 'condicional']:
                            response['hint'] = f"💡 Hint: For regular {verb_ending} verbs in {TENSE_NAMES[tense]}, add '{ending}' to the infinitive: {verb} + {ending}"
                        else:
                            response['hint'] = f"💡 Hint: For regular {verb_ending} verbs in {TENSE_NAMES[tense]}, use stem '{stem}' + '{ending}'"
            
            # Irregular verb hint
            elif verb_data.get('type') == 'irregular' and verb in IRREGULAR_HINTS:
                response['hint'] = f"💡 {IRREGULAR_HINTS[verb]}"
        
        # Tense identification hints
        elif question_type == 'identify-tense' and tense:
            if tense in TENSE_ID_HINTS:
                response['hint'] = f"💡 {TENSE_ID_HINTS[tense]}"
        
        # Pronoun identification hints
        elif question_type == 'identify-pronoun' and pronoun:
            if pronoun in PRONOUN_HINTS:
                response['hint'] = f"💡 {PRONOUN_HINTS[pronoun]}"
        
        # Infinitive identification hints
        elif question_type == 'identify-infinitive' and verb:
            verb_data = VERBS.get(verb, {})
            if verb.endswith('ar'):
                response['hint'] = f"💡 This is an -ar verb. Think about common -ar verbs like hablar, llamar, or estar."
            elif verb.endswith('er'):
                response['hint'] = f"💡 This is an -er verb. Think about common -er verbs like comer, tener, or hacer."
            elif verb.endswith('ir'):
                response['hint'] = f"💡 This is an -ir verb. Think about common -ir verbs like vivir, ir, or venir."
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
