import argparse

p = argparse.ArgumentParser()
p.add_argument('--experiment', required=True)
args = p.parse_args()
print(f'TODO: run experiment {args.experiment}')
