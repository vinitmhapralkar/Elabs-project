import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from pathlib import Path

# Load and clean data
df = pd.read_csv("data/news.csv")
df.dropna(inplace=True)

X = df['title']
y = df['label']

# Vectorize
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_vect = tfidf.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and vectorizer
Path("model").mkdir(exist_ok=True)
pickle.dump((model, tfidf), open("model/fake_news_model.pkl", "wb"))

# Save test results
Path("test_results").mkdir(exist_ok=True)
y_pred = model.predict(X_test)
with open("test_results/evaluation.txt", "w") as f:
    f.write(classification_report(y_test, y_pred))

print("Training complete. Model saved to model/fake_news_model.pkl")