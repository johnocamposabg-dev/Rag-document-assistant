from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size, overlap):
    chunk = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end]
        if len(piece) > 50:      
            chunk.append(piece)
        start += chunk_size - overlap
    return chunk


def get_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings.tolist()