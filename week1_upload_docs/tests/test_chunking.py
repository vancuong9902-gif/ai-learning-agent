import sys
import os

sys.path.append(os.path.abspath("."))

from ingest.extract import extract_text
from ingest.chunking import chunk_text


# 1. Extract text
pages  = extract_text("documents/upload/raw_docs/BT Big.docx")

print("Type extract_text:", type(pages))

# 2. JOIN LIST -> STRING
text = "\n".join(p["text"] for p in pages)

print("📄 Original tokens:", len(text.split()))


# 2. Chunking
chunks = chunk_text(text)

print("📦 Total chunks:", len(chunks))


# 3. Check size từng chunk
print("\n🔍 CHECK CHUNK SIZE")
for i, c in enumerate(chunks):
    size = len(c.split())
    print(f"Chunk {i}: {size} tokens")
    if size < 300 or size > 650:
        print("❌ FAIL SIZE")


# 4. Check overlap
print("\n🔁 CHECK OVERLAP")
def overlap_tokens(c1, c2, n=100):
    t1 = c1.split()[-n:]
    t2 = c2.split()[:n]
    return len(set(t1) & set(t2))

for i in range(len(chunks) - 1):
    overlap = overlap_tokens(chunks[i], chunks[i+1])
    print(f"Chunk {i} -> {i+1} overlap: {overlap}")


# 5. Check mất text
print("\n🧩 CHECK TEXT LOSS")
reconstructed = " ".join(chunks)
print("Reconstructed tokens:", len(reconstructed.split()))

print("\nORIGINAL START:")
print(text[:200])

print("\nRECONSTRUCTED START:")
print(reconstructed[:200])

print("\nORIGINAL END:")
print(text[-200:])

print("\nRECONSTRUCTED END:")
print(reconstructed[-200:])
