from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_keywords(content, num_keywords=12):
    tokens = word_tokenize(content)
    tagged_tokens = pos_tag(tokens)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word, tag in tagged_tokens if tag in ('NN', 'NNS', 'NNP', 'NNPS') and word.lower() not in stop_words]
    freq_dist = nltk.FreqDist(keywords)
    most_common = [word for word, count in freq_dist.most_common(num_keywords)]
    return most_common


def generate_question(sentence, keyword):
    return sentence.replace(keyword, '______')


def generate_options(keyword, distractors):
    options = [keyword] + distractors
    random.shuffle(options)
    return options


def generate_questions(content):
    sentences = sent_tokenize(content)
    questions = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)

        for (word, tag) in tagged_words:
            if tag.startswith('NNP'):
                questions.append(f'Who or what is {word}?')
            elif tag.startswith('NN') and wn.synsets(word):
                questions.append(f'What is the purpose of {word}?')
            elif tag.startswith('VB'):
                questions.append(f'What action is {word} describing?')
            elif tag.startswith('JJ'):
                questions.append(f'How would you describe {word}?')
            elif tag.startswith('RB'):
                questions.append(f'In what manner does {word} happen?')
            elif tag.startswith('PRP'):
                questions.append(f'Who does {word} refer to?')
            elif tag.startswith('IN'):
                questions.append(f'What is the relationship between {word} and other elements?')

    return list(set(questions))[:10]  


def generate_hard_questions(content, num_questions=5):
    
    sentences = re.split(r'[.!?]', content)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    questions = [
        f"What is the significance of '{sent}'?" for sent in sentences
    ] + [
        f"Explain the importance of '{sent}'."
        for sent in sentences
    ] + [
        f"How does '{sent}' contribute to the overall theme?"
        for sent in sentences
    ] + [
        f"Discuss the role of '{sent}' in the context provided."
        for sent in sentences
    ] + [
        f"Elaborate on the meaning behind '{sent}'."
        for sent in sentences
    ] + [
        f"In what way does '{sent}' impact the narrative?"
        for sent in sentences
    ] + [
        f"Describe the implications of '{sent}' in the given context."
        for sent in sentences
    ] + [
        f"Analyze the role and significance of '{sent}'."
        for sent in sentences
    ] + [
        f"Examine the influence of '{sent}' on the larger story."
        for sent in sentences
    ] + [
        f"What insights can be drawn from '{sent}'?"
        for sent in sentences
    ] + [
        f"Consider the significance of '{sent}' within the text."
        for sent in sentences
    ] + [
        f"Explore the deeper meaning of '{sent}'."
        for sent in sentences
    ] + [
        f"Evaluate the importance of '{sent}' in the narrative."
        for sent in sentences
    ] + [
        f"Break down the elements and importance of '{sent}'."
        for sent in sentences
    ] + [
        f"How does line '{sent}' contribute to the overall message of the passage?"
        for sent in sentences
    ]

    selected_questions = random.sample(questions, k=min(num_questions, len(questions)))

    return selected_questions


def generate_true_false_questions(content):
    
    sentences = sent_tokenize(content)
    questions = []
    for i, sentence in enumerate(sentences):
        
        rule_selector = random.randint(1, 4)

        if rule_selector == 1:  
            if i % 2 == 0:
                nouns = extract_nouns(sentence)
                if nouns:
                    random.shuffle(nouns)
                    noun = nouns.pop()
                    question = f"Does the mentioned sentence is disscused in the content?: {sentence.strip()}. (True/False)?"
                    answer = "True"
                else:
                    question = f"The sentence contains relevant information. (True/False)?"
                    answer = "True"
            else:
                question = f"{add_defect(sentence.strip())}. (True/False)?"
                answer = "False"

        elif rule_selector == 2:  
            if i % 2 == 0:
                adjectives = extract_adjectives(sentence)
                if adjectives:
                    random.shuffle(adjectives)
                    adjective = adjectives.pop()
                    question = f"Is the sentence present in the content mentioned earlier?: {sentence.strip()}. (True/False)?"
                    answer = "True"
                else:
                    question = f"The sentence contains relevant information. (True/False)?"
                    answer = "True"
            else:
                question = f"{add_defect(sentence.strip())}. (True/False)?"
                answer = "False"

        elif rule_selector == 3:  
            if i % 2 != 0:
                question = f"{add_defect(sentence.strip())}. (True/False)?"
                answer = "False"

        elif rule_selector == 4:  
            if i % 2 == 0:
                verbs = extract_verbs(sentence)
                if verbs:
                    random.shuffle(verbs)
                    verb = verbs.pop()
                    question = f"Can the sentence be found within the content provided?: {sentence.strip()}. (True/False)?"
                    answer = "True"
                else:
                    question = f"The sentence contains relevant information. (True/False)?"
                    answer = "True"
            else:
                question = f"{add_defect(sentence.strip())}. (True/False)?"
                answer = "False"

        while (question, answer) in questions:
            rule_selector = random.randint(1, 4)
            if rule_selector == 1:
                # Regenerate Rule 1 question
                if i % 2 == 0:
                    nouns = extract_nouns(sentence)
                    if nouns:
                        random.shuffle(nouns)
                        noun = nouns.pop()
                        question = f"Does the given sentence appear in the content above?: {sentence.strip()}. (True/False)?"
                        answer = "True"
                    else:
                        question = f"The sentence contains relevant information. (True/False)?"
                        answer = "True"
                else:
                    question = f"{add_defect(sentence.strip())}. (True/False)?"
                    answer = "False"
            elif rule_selector == 2:
                # Regenerate Rule 2 question
                if i % 2 == 0:
                    adjectives = extract_adjectives(sentence)
                    if adjectives:
                        random.shuffle(adjectives)
                        adjective = adjectives.pop()
                        question = f"{sentence.strip()}. (True/False)?"
                        answer = "True"
                    else:
                        question = f"The sentence contains relevant information. (True/False)?"
                        answer = "True"
                else:
                    question = f"{add_defect(sentence.strip())}. (True/False)?"
                    answer = "False"
            elif rule_selector == 3:
                # Regenerate Rule 3 question
                if i % 2 != 0:
                    question = f"{add_defect(sentence.strip())}. (True/False)?"
                    answer = "False"
            elif rule_selector == 4:
                # Regenerate Rule 4 question
                if i % 2 == 0:
                    verbs = extract_verbs(sentence)
                    if verbs:
                        random.shuffle(verbs)
                        verb = verbs.pop()
                        question = f"Tell, Is this sentence present in above content:{sentence.strip()}. (True/False)?"
                        answer = "True"
                    else:
                        question = f"The sentence contains relevant information. (True/False)?"
                        answer = "True"
                else:
                    question = f"{add_defect(sentence.strip())}. (True/False)?"
                    answer = "False"

        questions.append((question, answer))

    
    random.shuffle(questions)

    return questions

def extract_nouns(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    nouns = [word for word, pos in tagged_words if pos.startswith('N')]
    return nouns

def extract_adjectives(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    adjectives = [word for word, pos in tagged_words if pos.startswith('J')]
    return adjectives

def extract_verbs(sentence):
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    verbs = [word for word, pos in tagged_words if pos.startswith('V')]
    return verbs

def add_defect(sentence):
    
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)
    lemmatizer = WordNetLemmatizer()

    for i, (word, pos) in enumerate(tagged_words):
        if pos.startswith('V') and lemmatizer.lemmatize(word, 'v') == word:
            words.insert(i, "not")
            break

    return " ".join(words)

@app.route('/api/create_quiz', methods=['POST'])
def create_quiz():
    try:
        data = request.get_json()
        quiz_content = data.get('quizContent')
        keywords = extract_keywords(quiz_content)
        sentences = quiz_content.split('.')
        quiz = []
        used_keywords = []

        for i, sentence in enumerate(sentences):
            if sentence:
                for keyword in keywords:
                    if keyword in sentence and keyword not in used_keywords:
                        question = generate_question(sentence, keyword)
                        distractors = random.sample([word for word in keywords if word.lower() != keyword.lower()], 3)
                        options = generate_options(keyword, distractors)
                        quiz.append({'question_number': len(quiz) + 1, 'question': question, 'options': options, 'answer': keyword})
                        used_keywords.append(keyword)
                        break

        while len(quiz) < 8 and keywords:
            keyword = keywords.pop(0)
            for sentence in sentences:
                if keyword in sentence and keyword not in used_keywords:
                    question = generate_question(sentence, keyword)
                    distractors = random.sample([word for word in keywords if word.lower() != keyword.lower()], 3)
                    options = generate_options(keyword, distractors)
                    quiz.append({'question_number': len(quiz) + 1, 'question': question, 'options': options, 'answer': keyword})
                    used_keywords.append(keyword)
                    break

        return jsonify({'quizContent': quiz_content, 'processedQuiz': quiz})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hard', methods=['POST'])
def generate_hard_questions_route():
    try:
        data = request.get_json()
        quiz_content = data.get('quizContent')
        questions = generate_hard_questions(quiz_content, num_questions=5)
        return jsonify({'questions': questions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_medium_questions', methods=['POST'])
def generate_medium_questions_route():
    try:
        data = request.get_json()
        quiz_content = data.get('quizContent')
        questions = generate_true_false_questions(quiz_content)
        return jsonify({'questions': questions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
