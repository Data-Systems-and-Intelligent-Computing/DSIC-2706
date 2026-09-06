"""
Script: src/retrieve.py
Fungsi: Engine pencarian kemiripan audio (Audio Similarity Retrieval Engine) dan evaluasi metrik retrieval.
Sesuai Bab 10.2 & Bab 15 Dokumen Audit:
- Jarak: Cosine similarity sim(q, g) = (e_q . e_g) / (|e_q| * |e_g|)
- Metrik Primer:
  1. Average Precision @ k (AP@k) dan mAP@k
  2. Recall@k (Recall@1, Recall@5, Recall@10)
  3. Precision@k
  4. Top-1 match & max similarity score
"""

import numpy as np


def compute_query_retrieval(query_emb: np.ndarray,
                            query_label: str,
                            gallery_embs: np.ndarray,
                            gallery_labels: list,
                            k_values: list = [1, 5, 10]) -> dict:
    """
    Menghitung metrik retrieval untuk satu audio query terhadap seluruh item gallery.
    """
    # Pastikan L2-normalized
    q_norm = np.linalg.norm(query_emb)
    if q_norm > 1e-8:
        q_vec = query_emb / q_norm
    else:
        q_vec = query_emb

    g_norms = np.linalg.norm(gallery_embs, axis=1, keepdims=True)
    g_norms[g_norms < 1e-8] = 1e-8
    g_matrix = gallery_embs / g_norms

    # Cosine similarities
    scores = np.dot(g_matrix, q_vec)

    # Ranking descending
    ranked_indices = np.argsort(-scores)
    sorted_scores = scores[ranked_indices]
    sorted_labels = [gallery_labels[i] for i in ranked_indices]

    # Ground truth relevance (1 jika spesies cocok, 0 jika beda)
    relevance = np.array([1 if lbl == query_label else 0 for lbl in sorted_labels], dtype=int)
    total_relevant = int(np.sum(relevance))

    results = {
        "max_score": float(sorted_scores[0]) if len(sorted_scores) > 0 else 0.0,
        "top1_match": int(relevance[0]) if len(relevance) > 0 else 0,
        "total_relevant_in_gallery": total_relevant
    }

    # Hitung Precision@k, Recall@k, AP@k
    for k in k_values:
        k_capped = min(k, len(relevance))
        rel_k = relevance[:k_capped]
        hits = int(np.sum(rel_k))

        # Precision@k
        prec_k = hits / k_capped if k_capped > 0 else 0.0
        results[f"P@{k}"] = prec_k

        # Recall@k
        if total_relevant > 0:
            rec_k = hits / total_relevant
        else:
            rec_k = 0.0
        results[f"R@{k}"] = rec_k

        # Average Precision @ k (AP@k)
        if total_relevant > 0:
            cum_hits = np.cumsum(rel_k)
            precisions = cum_hits / (np.arange(k_capped) + 1)
            ap_k = float(np.sum(precisions * rel_k) / min(total_relevant, k_capped))
        else:
            ap_k = 0.0
        results[f"AP@{k}"] = ap_k

    return results


def evaluate_retrieval_corpus(query_embs: np.ndarray,
                              query_labels: list,
                              gallery_embs: np.ndarray,
                              gallery_labels: list,
                              k_values: list = [1, 5, 10]) -> dict:
    """
    Mengevaluasi seluruh corpus query dan menghitung nilai agregat (mAP@k, Mean Recall@k).
    """
    n_queries = len(query_labels)
    all_metrics = []

    for i in range(n_queries):
        m = compute_query_retrieval(
            query_emb=query_embs[i],
            query_label=query_labels[i],
            gallery_embs=gallery_embs,
            gallery_labels=gallery_labels,
            k_values=k_values
        )
        all_metrics.append(m)

    summary = {
        "num_queries": n_queries,
        "mean_top1": float(np.mean([m["top1_match"] for m in all_metrics]))
    }

    for k in k_values:
        summary[f"mAP@{k}"] = float(np.mean([m[f"AP@{k}"] for m in all_metrics]))
        summary[f"Recall@{k}"] = float(np.mean([m[f"R@{k}"] for m in all_metrics]))
        summary[f"Precision@{k}"] = float(np.mean([m[f"P@{k}"] for m in all_metrics]))

    return summary, all_metrics


if __name__ == "__main__":
    print("[*] Menguji fungsi retrieval engine...")
    q = np.array([1.0, 0.0, 0.0])
    G = np.array([
        [0.9, 0.1, 0.0],
        [0.0, 1.0, 0.0],
        [0.8, 0.2, 0.0]
    ])
    lbls = ["sp_A", "sp_B", "sp_A"]
    res = compute_query_retrieval(q, "sp_A", G, lbls, k_values=[1, 2, 3])
    print("[+] Retrieval result:", res)
    assert res["P@1"] == 1.0
    print("[+] Test retrieval berhasil!")
