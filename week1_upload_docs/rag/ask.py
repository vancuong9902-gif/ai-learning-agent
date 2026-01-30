def answer(query, sources):
    answer = f"Câu hỏi: {query}\n\nCác đoạn liên quan:\n"
    for s in sources:
        answer += f"- ({s['doc_id']} – chunk {s['chunk_id']})\n"
    return answer
