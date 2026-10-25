import requests
import random
import html

EDUCATION_CATEGORY_ID = 9  
API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def get_education_questions():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0 and data["results"]:
            return data["results"]
    return None

def run_quiz():
    questions = get_education_questions()

    if not questions:
        print("failed to fetch educational questions")
        return 

    score = 0
    print("Welcome to the education quiz")
    for i,q in enumerate(questions,1):
        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])
        incorrects = [html.unescape(a) for a in q["incorrect_answers"]]






