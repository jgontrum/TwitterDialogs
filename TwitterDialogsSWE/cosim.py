from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = (
"Der Hund ist wEggelaufen ",
"The sun is bright",
"weggelaufen ist der hund  ?",
"We can see the shining sun, the bright sun"
)


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

print cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
