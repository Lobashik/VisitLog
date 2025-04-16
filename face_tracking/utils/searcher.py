import faiss
import numpy as np


class FaceSearcher:
    def __init__(self, path):
        data = np.load(path, allow_pickle=True)
        self.embeddings = data["embeddings"].astype("float32")
        self.labels = data["names"]

        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, emb, k=1):
        emb = emb.astype("float32").reshape(1, -1)
        D, I = self.index.search(emb, k)
        return self.labels[I[0][0]], D[0][0]
