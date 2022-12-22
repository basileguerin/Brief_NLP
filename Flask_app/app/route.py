from flask import render_template, request
from app import app
import joblib
from unidecode import unidecode
from nltk.corpus import stopwords

model = joblib.load('Brief_NLP/ML/for_app')['modele']
lemmatiser = joblib.load('Brief_NLP/ML/for_app')['lemmatiser']
vectoriser = joblib.load('Brief_NLP/ML/for_app')['vectoriser']

def standardize_lemmentize_vectorize(comment: str, lemmatizer, vectorizer):
    """Met en forme le commentaire pour pouvoir faire une prédiction"""
    comment = comment.replace(r"http\S+", "")
    comment = comment.replace(r"http", "")
    comment = comment.replace(r"@\S+", "")
    comment = comment.replace(r"[0-9(),!?@\'\:\.\/\^\-\`\"\_\n]", " ")
    comment = comment.replace(r"@", "at")
    comment = unidecode(comment)
    comment = comment.lower()
    comment = comment.split()
    comment = [word for word in comment if not word in set(stopwords.words('french'))]
    comment = [lemmatizer.lemmatize(word) for word in comment]
    comment = ' '.join(comment)
    comment = vectorizer.transform([comment])
    return comment

def prediction(model, comment):
    avis = {
        0 : 'Commentaire négatif',
        1 : 'Commentaire positif'
    }
    comment = standardize_lemmentize_vectorize(comment, lemmatiser, vectoriser)

    return avis[model.predict(comment)[0]]


@app.route('/', methods=["GET", "POST"])  
def index():
    if request.method == "GET":  
        
        return render_template('index.html')
        
    if request.method == "POST":
        comment = request.form['textarea']
        pred = prediction(model, comment)

        return render_template('index.html', pred=pred)

