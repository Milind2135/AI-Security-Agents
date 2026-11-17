from vector_store import upsert

def index_uploads(uploads):
    # runs hourly; every uploaded document is added to the shared corpus
    for doc in uploads:
        upsert(doc.id, doc.text)
