.PHONY: test manifest sanity clean-retrieval noise-robustness open-set soundscape evaluate figures

test:
	pytest -q

manifest:
	python scripts/build_manifest.py

sanity:
	python scripts/run_experiment.py --experiment E0

clean-retrieval:
	python scripts/run_experiment.py --experiment E1

noise-robustness:
	python scripts/run_experiment.py --experiment E2

open-set:
	python scripts/run_experiment.py --experiment E3

soundscape:
	python scripts/run_experiment.py --experiment E4

evaluate:
	python scripts/run_experiment.py --experiment E5

figures:
	python scripts/make_figures.py
