"""Regression tests on synthetic temporary files; no experiment execution."""
import ast
import csv
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("restart_audit", ROOT / "scripts/audit_manifests.py")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class ManifestPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "data/manifests").mkdir(parents=True)
        self.known = []
        self.download = []
        for index, role in enumerate(("gallery", "query_clean", "calibration")):
            relative = f"data/xeno_canto_indonesia/species/XC{index}.mp3"
            digest = self.audio(relative, f"different known content {index}".encode())
            self.known.append(dict(recording_id=f"XC{index}", species_key="species", scientific_name="Known species",
                                   author=f"Author {index}", file_path=relative, split_role=role))
            self.download.append(dict(recording_id=f"XC{index}", file_path=relative, sha256=digest,
                                      bytes=(self.root / relative).stat().st_size, status="SUCCESS"))
        self.noise = []
        self.unknown = []
        for index, role in enumerate(("unknown_calibration", "unknown_test")):
            relative = f"data/xeno_canto_indonesia_unknowns/bird/XC{index+100}.mp3"
            digest = self.audio(relative, f"unknown bird {index}".encode())
            self.unknown.append(dict(unknown_id=f"BIRD{index}", split_role=role, source_category="non_target_species",
                                     source_label=f"Other species {index}", file_path=relative, sha256=digest))
            relative = f"data/itera_noise/site/20260920_00000{index}.WAV"
            digest = self.audio(relative, f"noise {index}".encode())
            self.noise.append(dict(filename=relative.removeprefix("data/itera_noise/"), sha256_checksum=digest))
            self.unknown.append(dict(unknown_id=f"NOISE{index}", split_role=role, source_category="environmental_noise",
                                     source_label="site", file_path=relative, sha256=digest))
        self.save_tables()

    def audio(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return hashlib.sha256(content).hexdigest()

    def save_tables(self):
        for name, rows in (("dataset_split.csv", self.known), ("download_manifest.csv", self.download),
                           ("itera_noise_manifest.csv", self.noise), ("unknown_open_set_manifest.csv", self.unknown)):
            with (self.root / "data/manifests" / name).open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

    def report(self):
        return AUDIT.audit_project(self.root)

    def codes(self):
        return {item["code"] for item in self.report()["issues"]}

    def test_valid_files_and_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        report = self.report()
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(report["status"], "PASS_WITH_WARNINGS")
        self.assertEqual(report["hashed_physical_files"], 7)
        self.assertEqual(report["reserved_noise"], 2)
        self.assertIn("noise_session_overlap", {i["code"] for i in report["issues"]})

    def test_missing_and_corrupted_audio(self):
        (self.root / self.known[0]["file_path"]).unlink()
        (self.root / self.known[1]["file_path"]).write_bytes(b"corrupted")
        self.assertTrue({"missing_audio", "checksum_mismatch", "byte_size_mismatch"}.issubset(self.codes()))

    def test_manifest_changed_while_audio_is_being_checked(self):
        original = AUDIT.sha256
        changed = False
        def change_during_hash(path):
            nonlocal changed
            if not changed:
                manifest = self.root / "data/manifests/dataset_split.csv"
                manifest.write_bytes(manifest.read_bytes() + b"\n")
                changed = True
            return original(path)
        with patch.object(AUDIT, "sha256", change_during_hash):
            self.assertIn("manifest_changed_during_audit", self.codes())

    def test_actual_manifest_status_and_noise_category(self):
        self.download[0]["status"] = "VERIFIED_EXISTING"
        for row in self.unknown:
            if row["source_category"] == "environmental_noise":
                row["source_category"] = "itera_environmental_noise"
        self.save_tables()
        report = self.report()
        self.assertNotEqual(report["status"], "FAIL")
        self.assertEqual(report["reserved_noise"], 2)

    def test_historical_download_log_is_not_active_split_failure(self):
        extra_path = "data/xeno_canto_indonesia/species/old.mp3"
        digest = self.audio(extra_path, b"old downloaded file")
        rows = self.download + [dict(recording_id="OLD", file_path=extra_path, sha256=digest,
                                    bytes=len(b"old downloaded file"), status="SUCCESS")]
        with (self.root / "data/manifests/download_audit_log.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        report = self.report()
        self.assertNotEqual(report["status"], "FAIL")
        self.assertIn("audit_download_ids", {i["code"] for i in report["issues"]})

    def test_duplicate_ids_and_normalized_recordist_leak(self):
        self.known[1]["recording_id"] = self.known[0]["recording_id"]
        self.known[1]["author"] = "  AUTHOR   0 "
        self.save_tables()
        self.assertTrue({"duplicate_or_empty_id", "author_overlap"}.issubset(self.codes()))

    def test_exact_audio_cross_role_even_when_checksums_are_updated(self):
        content = (self.root / self.known[0]["file_path"]).read_bytes()
        query = self.known[1]["file_path"]
        self.download[1]["sha256"] = self.audio(query, content)
        self.download[1]["bytes"] = len(content)
        self.save_tables()
        self.assertIn("cross_role_identical_audio", self.codes())

    def test_unused_duplicate_is_warning_not_cross_split_leak(self):
        content = (self.root / self.known[0]["file_path"]).read_bytes()
        self.audio("data/xeno_canto_indonesia/species/unused.mp3", content)
        codes = self.codes()
        self.assertIn("physical_duplicate", codes)
        self.assertNotIn("cross_role_identical_audio", codes)

    def test_unknown_species_and_path_escape(self):
        self.unknown[2]["source_label"] = self.unknown[0]["source_label"]
        self.known[0]["file_path"] = "../outside.mp3"
        self.save_tables()
        self.assertTrue({"unknown_species_overlap", "unsafe_path"}.issubset(self.codes()))


class H3ReportingTests(unittest.TestCase):
    def test_nonsignificant_result_is_not_replaced_by_forced_claim(self):
        # Evaluate only the reporting row, not the experiment/bootstrap runner.
        tree = ast.parse((ROOT / "src/bootstrap_inference.py").read_text(encoding="utf-8"))
        candidates = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                mapping = {key.value: value for key, value in zip(node.keys, node.values) if isinstance(key, ast.Constant)}
                title = mapping.get("Pengujian")
                if isinstance(title, ast.Constant) and title.value == "Fluktuasi Rentang Habitat (-5 dB)":
                    candidates.append(node)
        self.assertEqual(len(candidates), 1)
        expression = ast.fix_missing_locations(ast.Expression(candidates[0]))
        for p_value, significant in (("0.8", False), ("0.01", True)):
            values = dict(mean_v=-0.1, low=-0.3, high=0.1, p_str=p_value, sig=significant, obs_delta=-0.1)
            row = eval(compile(expression, "H3-report-only", "eval"), {"__builtins__": {}}, values)
            self.assertEqual(row["p_value"], p_value)
            self.assertIs(row["Signifikan_0.05"], significant)
            self.assertNotIn("Terdukung", row["Catatan"])


if __name__ == "__main__":
    unittest.main()
