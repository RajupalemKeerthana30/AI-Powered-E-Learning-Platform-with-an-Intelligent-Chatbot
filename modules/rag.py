from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGSystem:

    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )
        self.document_vectors = None

    def add_documents(self, chunks):

        if not chunks:
            return

        self.documents.extend(chunks)

        self.document_vectors = self.vectorizer.fit_transform(
            self.documents
        )

    def search(self, question, top_k=3):

        if not self.documents:
            return ""

        question_vector = self.vectorizer.transform(
            [question]
        )

        similarities = cosine_similarity(
            question_vector,
            self.document_vectors
        )[0]

        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []

        for index in top_indices:
            if similarities[index] > 0:
                results.append(
                    self.documents[index]
                )

        return "\n\n".join(results)