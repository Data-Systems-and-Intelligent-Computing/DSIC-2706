.PHONY: help test manifest sanity clean-retrieval noise-robustness open-set soundscape evaluate figures all clean

help:
	@echo "Perintah Otomasi Eksperimen DSIC-2706:"
	@echo "  make test             - Menjalankan seluruh unit test ilmiah & zero leakage"
	@echo "  make manifest         - Membangun partisi strict recordist-disjoint"
	@echo "  make sanity           - Menjalankan E0: Pipeline Sanity Check"
	@echo "  make clean-retrieval  - Menjalankan E1: Clean Retrieval Baseline"
	@echo "  make noise-robustness - Menjalankan E2: Paired Controlled Noise Robustness"
	@echo "  make open-set         - Menjalankan E3: Open-Set Calibration & Threshold Transfer"
	@echo "  make soundscape       - Menjalankan E4: External Soundscape Domain Shift"
	@echo "  make evaluate         - Menjalankan seluruh rangkaian benchmark komparatif (E1-E3)"
	@echo "  make figures          - Membuat grafik ilmiah mAP@10 dan retensi relatif"
	@echo "  make all              - Menjalankan test, evaluate, dan figures"

test:
	python run_tests.py

manifest:
	python src/build_manifest.py

sanity:
	python experiments/E0_pipeline_sanity/run_e0.py

clean-retrieval:
	python experiments/E1_clean_retrieval/run_e1.py

noise-robustness:
	python experiments/E2_noise_robustness/run_e2.py

open-set:
	python experiments/E3_open_set_threshold/run_e3.py

soundscape:
	python experiments/E4_real_soundscape/run_e4.py

evaluate:
	python src/run_benchmark.py

figures:
	python src/plot_results.py

all: test evaluate figures

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
