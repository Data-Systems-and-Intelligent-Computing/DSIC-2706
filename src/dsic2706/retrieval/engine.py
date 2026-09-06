import numpy as np
from ..features.mfcc import batch_cosine_similarity


def compute_query_retrieval(query_emb: np.ndarray,
                            query_label: str,
                            gallery_embs: np.ndarray,
                            gallery_labels: list,
                            k_values: list = [1, 5, 10]) -> dict:
    """
    Menghitung metrik retrieval untuk satu audio query terhadap seluruh item gallery.
    """
    q_norm = np.linalg.norm(query_emb)
    if q_norm > 1e-8:
        q_vec = query_emb / q_norm
    else:
        q_vec = query_emb

    g_norms = np.linalg.norm(gallery_embs, axis=1, keepdims=True)
    g_norms[g_norms < 1e-8] = 1e-8
    g_matrix = gallery_embs / g_norms

    scores = np.dot(g_matrix, q_vec)
    ranked_indices = np.argsort(-scores)
    sorted_scores = scores[ranked_indices]
    sorted_labels = [gallery_labels[i] for i in ranked_indices]

    relevance = np.array([1 if lbl == query_label else 0 for lbl in sorted_labels], dtype=int)
    total_relevant = int(np.sum(relevance))

    results = {
        "ranked_indices": ranked_indices,
        "ranked_scores": sorted_scores,
        "ranked_labels": sorted_labels,
        "max_score": float(sorted_scores[0]) if len(sorted_scores) > 0 else 0.0,
        "top1_match": int(relevance[0]) if len(relevance) > 0 else 0,
        "total_relevant_in_gallery": total_relevant
    }

    for k in k_values:
        k_capped = min(k, len(relevance))
        rel_k = relevance[:k_capped]
        hits = int(np.sum(rel_k))

        results[f"P@{k}"] = hits / k_capped if k_capped > 0 else 0.0
        results[f"R@{k}"] = (hits / total_relevant) if total_relevant > 0 else 0.0

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
                              k_values: list = [1, 5, 10]) -> tuple:
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
