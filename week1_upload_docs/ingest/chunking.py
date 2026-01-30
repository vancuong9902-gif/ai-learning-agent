import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


def chunk_text(
    texts,
    chunk_size: int = 500,
    overlap: int = 100
):
    if overlap >= chunk_size:
        raise ValueError("overlap phải nhỏ hơn chunk_size")

    chunks = []

    for text in texts:
        if not text or not text.strip():
            continue

        # 🔒 CHỐT CHẶN RÁC (QUAN TRỌNG)
        if len(text.strip()) < 50:
            continue

        tokens = tokenizer.encode(text)
        start = 0
        length = len(tokens)

        while start < length:
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk = tokenizer.decode(chunk_tokens).strip()

            # 🔒 BỎ CHUNK QUÁ NGẮN
            if len(chunk) >= 100:
                chunks.append(chunk)

            start = end - overlap

    return chunks
