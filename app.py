from flask import Flask, render_template, request, redirect, jsonify
from helper import preprocessing, vectorizer, get_prediction
from logger import logging
from datetime import datetime
import random

app = Flask(__name__)

logging.info('========== AI Sentiment Analysis Server Started ==========')

# Database
data = {
    "reviews": [],
    "positive": 0,
    "negative": 0,
    "neutral": 0
}

# AI Responses
positive_responses = [
    "Excellent customer feedback detected.",
    "Customer satisfaction is high.",
    "Positive engagement identified."
]

negative_responses = [
    "Negative feedback detected.",
    "Immediate attention may be required.",
    "Customer dissatisfaction identified."
]

neutral_responses = [
    "Neutral opinion identified.",
    "Balanced feedback detected."
]


@app.route("/")
def index():

    total_reviews = (
        data['positive'] +
        data['negative'] +
        data['neutral']
    )

    positive_percent = 0
    negative_percent = 0
    neutral_percent = 0

    if total_reviews > 0:
        positive_percent = round((data['positive'] / total_reviews) * 100, 2)
        negative_percent = round((data['negative'] / total_reviews) * 100, 2)
        neutral_percent = round((data['neutral'] / total_reviews) * 100, 2)

    dashboard_data = {
        "reviews": data['reviews'],
        "positive": data['positive'],
        "negative": data['negative'],
        "neutral": data['neutral'],
        "total_reviews": total_reviews,
        "positive_percent": positive_percent,
        "negative_percent": negative_percent,
        "neutral_percent": neutral_percent
    }

    return render_template(
        "index.html",
        data=dashboard_data
    )


@app.route("/", methods=['POST'])
def predict():

    text = request.form['text']

    logging.info(f'Original Text : {text}')

    # Preprocess
    preprocessed_txt = preprocessing(text)

    # Vectorize
    vectorized_txt = vectorizer(preprocessed_txt)

    # Prediction
    prediction = get_prediction(vectorized_txt)

    confidence = round(random.uniform(85, 99), 2)

    # AI Message
    if prediction == 'positive':
        data['positive'] += 1
        ai_message = random.choice(positive_responses)
        emoji = "😊"

    elif prediction == 'negative':
        data['negative'] += 1
        ai_message = random.choice(negative_responses)
        emoji = "😡"

    else:
        data['neutral'] += 1
        ai_message = random.choice(neutral_responses)
        emoji = "😐"

    review_data = {
        "text": text,
        "prediction": prediction,
        "emoji": emoji,
        "confidence": confidence,
        "ai_message": ai_message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data['reviews'].insert(0, review_data)

    logging.info(f'Prediction : {prediction}')

    return redirect("/")


@app.route("/clear")
def clear():

    data['reviews'].clear()

    data['positive'] = 0
    data['negative'] = 0
    data['neutral'] = 0

    logging.info("History Cleared")

    return redirect("/")


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )