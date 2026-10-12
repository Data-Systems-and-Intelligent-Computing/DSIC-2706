"""Independent synthetic tests; never import model/audio code or touch user's project."""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CODE = HERE / "run_e4_five_locations_v10_stage7.py.draft"
RUN_ID_CODE = HERE / "e4_run_identity_v2.py"

root_ast = ast.parse(CODE.read_text(encoding="utf-8"))
functions = [
    node for node in root_ast.body if isinstance(node, ast.FunctionDef) and node.name in {
        "write_json_new", "write_df_replace", "validate_run_identity", "_expected_pool_names",
        "validate_condition_rows", "load_condition_snapshot", "save_condition_snapshot", "precheck_snapshots"
    }
]
assert len(functions) == 8, "Snapshot helper API changed"
run_namespace = {"__name__": "synthetic_resume_test", "Path": Path, "pd": pd, "np": np,
                 "os": os, "json": json, "math": math, "SNAPSHOT_SCHEMA": "E4_condition_snapshot_v1",
                 "SUMMARY_KEYS": {"representation", "repeat_id", "habitat", "condition", "snr_db",
                                  "mAP@10", "Top1_Accuracy", "Precision@10", "Recall@10", "relative_retention"}}
run_id_namespace = {"__name__": "run_identity_test"}
exec(compile(RUN_ID_CODE.read_text(encoding="utf-8"), str(RUN_ID_CODE), "exec"), run_id_namespace)
run_namespace["sha256_file"] = run_id_namespace["sha256_file"]
run_namespace["fingerprint_json"] = run_id_namespace["fingerprint_json"]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(CODE), "exec"), run_namespace)


def check_failure(callable_, expected_exception, name):
    try:
        callable_()
    except expected_exception:
        print(f"[PASS] {name}")
        return
    raise AssertionError(f"Expected {expected_exception} for {name}")


with TemporaryDirectory() as temp:
    root = Path(temp)
    asset_paths = {}
    for name in sorted(run_id_namespace["REQUIRED_ASSETS"]):
        path = root / f"asset_{name}.txt"
        path.write_text(name, encoding="utf-8")
        asset_paths[name] = path
    design = {"representations": ["R0", "R1", "R2", "R3"],
              "locations": ["Kebun_Raya", "Embung_F", "Gedung_F", "Masjid_At_Tanwir", "Sekitar_GKU_1"],
              "noise_categories": ["Amplitudo-High", "Amplitudo-Medium", "Amplitudo-Low",
                                   "Frequency-High", "Frequency-Medium", "Frequency-Low"],
              "snr_db": [20, 10, 0, -5], "repeat_ids": [0, 1, 2, 3],
              "category_seed": 20261012,
              "noise_seed_rule": "5000 + 100000 * repeat_id + query_index (0-based)",
              "n_gallery": 673, "n_queries": 311, "r3_seed": 42}
    identity, sha = run_id_namespace["build_run_identity"](
        root, "a" * 64, "b" * 64, asset_paths, design)
    identity_path = root / "run_identity.json"
    run_namespace["write_json_new"](identity_path, {"identity": identity, "sha256": sha})
    run_namespace["validate_run_identity"](identity_path, identity, sha)
    print("[PASS] run identity baru, hashes 19 aset, verifikasi resume")
    check_failure(lambda: run_namespace["validate_run_identity"](identity_path, identity, "0" * 64),
                  ValueError, "run identity mismatch ditolak")
    check_failure(lambda: run_namespace["write_json_new"](identity_path, {}),
                  FileExistsError, "identitas tidak ditimpa")
    asset_paths["R0_cache"].write_text("modified", encoding="utf-8")
    _, changed_sha = run_id_namespace["build_run_identity"](root, "a" * 64, "b" * 64, asset_paths, design)
    assert sha != changed_sha
    print("[PASS] perubahan cache terdeteksi oleh SHA256 run")

    noise_root = root / "noise"
    configs = list(design["noise_categories"])
    pools = {k: [noise_root / (k + ".wav")] for k in configs}
    query_ids = [f"XC{i:07d}" for i in range(311)]
    query_df = pd.DataFrame({"recording_id": query_ids, "species_key": ["spA"] * 311})
    config_per_query = [configs[i % len(configs)] for i in range(311)]
    rep, repeat_id, hab, snr = "R2", 2, "Kebun_Raya", -5
    summary = {"representation": rep, "repeat_id": repeat_id, "habitat": hab,
               "condition": "SNR_-5dB", "snr_db": -5,
               "mAP@10": 0.4, "Top1_Accuracy": 0.5, "Precision@10": 0.6,
               "Recall@10": 0.7, "relative_retention": 0.8}
    rows = []
    for i, (qid, config) in enumerate(zip(query_ids, config_per_query)):
        rows.append({"query_id": qid, "species_key": "spA", "representation": rep,
                     "repeat_id": repeat_id, "habitat": hab, "condition": "SNR_-5dB", "snr_db": snr,
                     "noise_file": config + ".wav", "noise_config": config,
                     "noise_seed": 5000 + 100000 * repeat_id + i,
                     "noise_start_sample": i, "noise_segment_samples": 32000,
                     "noise_raw_rms": 0.02, "snr_db_target": -5.0,
                     "snr_db_achieved": -5.0, "mix_skipped_silent_signal": False,
                     "AP@10": 0.4, "top1_correct": 0.5,
                     "Precision@10": 0.6, "Recall@10": 0.7})
    # install NOISE_DIR to direct the standalone precheck
    run_namespace["NOISE_DIR"] = noise_root
    base = root / "raw" / "E4_R2_conditions" / "repeat_2"
    base.mkdir(parents=True)
    csv = base / "Kebun_Raya_SNR_-5dB.csv"
    save = run_namespace["save_condition_snapshot"]
    load = run_namespace["load_condition_snapshot"]
    save(csv, rows, summary, sha, query_df, config_per_query, pools, noise_root)
    recovered_summary, recovered_rows = load(csv, sha, query_df, config_per_query,
                                              pools, noise_root, rep, repeat_id, hab, snr)
    assert recovered_summary == summary and len(recovered_rows) == 311
    print("[PASS] 311-row CSV + JSON atomik, bisa dilanjutkan")
    precheck = run_namespace["precheck_snapshots"]
    checked = precheck(root / "raw", ["R0", "R1", "R2", "R3"],
                       {hab: []}, [snr], query_df, config_per_query,
                       {hab: pools}, sha)
    assert list(checked) == [(rep, repeat_id, hab, snr)]
    print("[PASS] pre-scan resume: representasi yang belum dibuat diperbolehkan")
    orphan = base / "unused.csv.tmp"
    orphan.write_text("partial", encoding="utf-8")
    check_failure(lambda: precheck(root / "raw", [rep], {hab: []}, [snr],
                                  query_df, config_per_query, {hab: pools}, sha),
                  ValueError, "snapshot temporer sisa crash ditolak")
    orphan.unlink()
    check_failure(lambda: save(csv, rows, summary, sha, query_df, config_per_query,
                               pools, noise_root), FileExistsError, "snapshot tidak ditimpa")
    check_failure(lambda: load(csv, "9" * 64, query_df, config_per_query,
                               pools, noise_root, rep, repeat_id, hab, snr),
                  ValueError, "snapshot beda run ditolak")
    validate = run_namespace["validate_condition_rows"]
    bad_rows = pd.DataFrame(rows)
    bad_rows.loc[0, "noise_seed"] = 42
    check_failure(lambda: validate(bad_rows, summary, query_df, config_per_query,
                                   pools, noise_root, rep, repeat_id, hab, snr),
                  ValueError, "seed noise salah ditolak")
    bad_rows = pd.DataFrame(rows)
    bad_rows.loc[0, "query_id"] = "OTHER"
    check_failure(lambda: validate(bad_rows, summary, query_df, config_per_query,
                                   pools, noise_root, rep, repeat_id, hab, snr),
                  ValueError, "urutan Query salah ditolak")
    before = csv.read_bytes()
    csv.write_bytes(before + b"\n")
    check_failure(lambda: load(csv, sha, query_df, config_per_query,
                               pools, noise_root, rep, repeat_id, hab, snr),
                  ValueError, "snapshot CSV termodifikasi ditolak")
    csv.write_bytes(before)
    # semantic tamper with both CSV digest and sidecar adjusted must still be rejected
    frame = pd.read_csv(csv)
    frame.loc[0, "query_id"] = "OTHER"
    frame.to_csv(csv, index=False)
    meta_path = csv.with_suffix(".json")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["csv_sha256"] = run_namespace["sha256_file"](csv)
    meta_path.write_text(json.dumps(meta), encoding="utf-8")
    check_failure(lambda: load(csv, sha, query_df, config_per_query,
                               pools, noise_root, rep, repeat_id, hab, snr),
                  ValueError, "CSV dan JSON diubah bersama tetap ditolak secara semantik")
    print("\nHASIL: SEMUA PENGUJIAN SINTETIS LULUS")
