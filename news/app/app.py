import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Fake News Detector")

model, vectorizer = pickle.load(open("../model/fake_news_model.pkl", "rb"))

st.title("Fake News Detector")
st.subheader("Check if a news headline is Real or Fake")

mode = st.radio("Choose Mode:", ["Single Headline", "Batch CSV Upload"])

if mode == "Single Headline":
    headline = st.text_input("Enter headline:")
    if st.button("Predict"):
        X = vectorizer.transform([headline])
        prediction = model.predict(X)[0]
        proba = model.predict_proba(X).max()
        st.success(f"Prediction: {'Real' if prediction == 1 else 'Fake'} ({proba:.2%} confidence)")

else:
    uploaded = st.file_uploader("Upload CSV with 'title' column", type='csv')
    if uploaded:
        df = pd.read_csv(uploaded)
        X = vectorizer.transform(df['title'])
        preds = model.predict(X)
        df['Prediction'] = ['Real' if p == 1 else 'Fake' for p in preds]
        st.write(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Predictions", csv, "results.csv", "text/csv")