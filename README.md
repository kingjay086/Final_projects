# 🎬 Content-Based Movie Recommender System

This project is a **Streamlit web app** that recommends similar movies based on your input. It uses a **content-based filtering approach** with NLP techniques and cosine similarity.

---

## 🚀 Features

- Recommend 5 similar movies based on selected movie
- Uses TMDB 5000 dataset (`movies` + `credits`)
- Google Drive fallback for pre-trained model files

---

## 🧠 Recommendation Logic

The recommendation system uses **content-based filtering** with **cosine similarity** on movie metadata such as:

- **Overview** (description)
- **Genres**
- **Keywords**
- **Top 3 Cast members**
- **Director**

### 🔍 Steps:
1. Extract key features from each movie and combine them into a "tag" string
2. Convert tags into numerical vectors using `CountVectorizer`
3. Calculate **cosine similarity** between movie vectors
4. Recommend the top 5 most similar movies (excluding the input movie)

---

## 📁 Dataset

Used the **TMDB 5000 Movie Dataset** from Kaggle:  
🔗 [TMDB 5000 Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

## 🛠️ Tech Stack

- Python
- Pandas, scikit-learn
- Streamlit
- gdown (for downloading model files)
- Pickle (for saving models)

---

## 🧾 Files and Structure

```bash
├── finalproject.py        # Data cleaning and model training
├── app.py                 # Streamlit UI for recommendation
├── App Link
├── movies.pkl(in data)             # Processed movie data (title + tags)
├── similarity.pkl(in data)         # Cosine similarity matrix
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```


## 📸 Sample Output
<img width="1498" height="1224" alt="image" src="https://github.com/user-attachments/assets/96912732-d93e-47b0-b940-2497ccdff60c" />

https://finalprojects-4rcg8gtm6s2ipe3ktyky3u.streamlit.app/
---
