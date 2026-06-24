print("welcome")
from transformers import pipeline 
nlp = pipeline("sentiment-analysis")
result = nlp("I love learning Python!")
print(result)