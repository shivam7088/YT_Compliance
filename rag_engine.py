from pathlib import Path
import re
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ComplianceRAG:
    """
    Small local RAG system:
    PDF rules -> chunks -> TF-IDF vectors -> similarity search.
    No Azure and no vector database required.
    """

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.chunks = []
        self.vectorizer = None
        self.matrix = None

    def _chunk_text(self, text, size=1200, overlap=200):
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            return []

        chunks = []
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            chunk = text[start:end]

            # Try not to cut in the middle of a sentence.
            if end < len(text):
                last_stop = max(chunk.rfind(". "), chunk.rfind("."))
                if last_stop > size * 0.6:
                    end = start + last_stop + 1
                    chunk = text[start:end]

            chunks.append(chunk.strip())
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
        return chunks

    def load_documents(self):
        self.chunks = []

        for pdf in sorted(self.data_dir.glob("*.pdf")):
            reader = PdfReader(str(pdf))
            full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

            for chunk in self._chunk_text(full_text):
                self.chunks.append({
                    "source": pdf.name,
                    "text": chunk,
                })

        if not self.chunks:
            raise RuntimeError("No PDF compliance documents found in the data folder.")

        texts = [x["text"] for x in self.chunks]
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=20000
        )
        self.matrix = self.vectorizer.fit_transform(texts)

    def retrieve(self, query, top_k=5):
        if self.matrix is None:
            self.load_documents()

        q = self.vectorizer.transform([query[:20000]])
        scores = cosine_similarity(q, self.matrix)[0]
        indices = scores.argsort()[::-1][:top_k]

        results = []
        for i in indices:
            if scores[i] <= 0:
                continue
            results.append({
                **self.chunks[i],
                "score": float(scores[i])
            })
        return results
