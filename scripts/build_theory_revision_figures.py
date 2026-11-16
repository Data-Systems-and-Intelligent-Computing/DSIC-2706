"""Build Figures 6 and 8, or figures from specified experiment results.
Only the new requested output directory is written; legacy figures stay intact.
"""
from pathlib import Path
import argparse,hashlib,json,sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]

def main(output):
    output=Path(output).resolve()
    if output.parent!=(ROOT/'paper/figures').resolve():raise ValueError('Use a new child of paper/figures')
    if output.exists():raise FileExistsError(output)
    manifest=ROOT/'data/manifests/dataset_split.csv'
    split=pd.read_csv(manifest)
    gallery=split[split.split_role.eq('gallery')].groupby('species_key').size().rename('gallery_count')
    query=split[split.split_role.eq('query_clean')].groupby('species_key').size().rename('query_count')
    table=pd.concat([gallery,query],axis=1).reset_index()
    table['recall10_ceiling']=np.minimum(1,10/table.gallery_count)
    ceiling=np.average(table.recall10_ceiling,weights=table.query_count)
    e1=pd.read_csv(ROOT/'results/tables/10_e1_clean_retrieval_summary.csv')
    output.mkdir(parents=True,exist_ok=False)
    table.to_csv(output/'recall10_ceiling_by_species.csv',index=False)
    fig,ax=plt.subplots(figsize=(13,5.7));ax.set_xlim(0,13);ax.set_ylim(0,5.7);ax.axis('off')
    boxes=[(.3,2.1,3.5,2.1,'Rekaman burung Xeno-Canto\n20 spesies Indonesia\n311 query yang sama\nGallery tetap: 673 rekaman','#edf3fa'),(4.5,3.1,3.7,1.6,'E2: noise dari pool ITERA\n1 segmen per query\nSNR +20, +10, 0, -5 dB','#fff4df'),(4.5,.7,3.7,1.8,'E4: noise dari 5 lokasi\n4 ulangan pemilihan segmen\nSNR +20, +10, 0, -5 dB\n6 kategori AudioMoth dipasangkan','#e5f4ec'),(9,1.9,3.6,2.4,'Ekstraksi R0-R3 beku\nCosine similarity\nRanking dan AP@10 per query\n\nE4: sensitivitas profil lokasi\nAyunan absolut dan retensi','#eef1f5')]
    for x,y,w,h,t,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.08',facecolor=color,edgecolor='#526579',linewidth=1.3));ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=11)
    for a,b in [((3.9,3.5),(4.35,3.9)),((3.9,2.5),(4.35,1.7)),((8.35,3.9),(8.85,3.5)),((8.35,1.7),(8.85,2.5))]:ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#526579','lw':1.5})
    ax.text(6.5,5.25,'Gambar 6. E2 dan E4 memakai pencampuran aditif terkontrol',ha='center',fontsize=15,weight='bold')
    ax.text(6.5,.12,'Lima lokasi: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, sekitar GKU 1.\nDesain ini tidak mengukur burung in-situ, propagasi jarak, atau reverberasi.',ha='center',fontsize=10,color='#364152')
    fig.tight_layout();fig.savefig(output/'fig06_e4_noise_profiles.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,5.8))
    axes[0].bar(e1.representation,e1['Recall@10'],color=['#64748b','#d95f02','#16856e','#aa6699'])
    axes[0].axhline(ceiling,color='#b45309',linestyle='--',label=f'Batas rata-rata berbobot query: {ceiling:.4f}')
    for i,val in enumerate(e1['Recall@10']):axes[0].text(i,val+.008,f'{val:.4f}',ha='center')
    axes[0].set_ylim(0,.42);axes[0].set_ylabel('Rata-rata Recall@10 (311 query)');axes[0].set_title('E1 pada gallery aktif: 673 rekaman');axes[0].legend(fontsize=9,loc='upper left');axes[0].grid(axis='y',alpha=.2)
    ordered=table.sort_values('recall10_ceiling')
    axes[1].barh(ordered.species_key,ordered.recall10_ceiling,color='#93b7ce');axes[1].set_xlabel('Batas per spesies: min(1, 10 / jumlah gallery relevan)');axes[1].set_xlim(0,.73);axes[1].set_title('15-100 gallery relevan per spesies');axes[1].tick_params(axis='y',labelsize=8)
    fig.suptitle('Gambar 8. Batas Recall@10 membatasi nilai maksimum; kualitas ranking menentukan nilai aktual',fontsize=12,weight='bold')
    fig.tight_layout();fig.savefig(output/'fig08_recall_ceiling_active.png',dpi=180);plt.close(fig)
    sources=[manifest,ROOT/'results/tables/10_e1_clean_retrieval_summary.csv',ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json']
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    info={'script_sha256':digest(Path(__file__)),'sources_sha256':{p.relative_to(ROOT).as_posix():digest(p) for p in sources},'gallery_count':int(gallery.sum()),'query_count':int(query.sum()),'species_mean_ceiling':table.recall10_ceiling.mean(),'query_weighted_mean_ceiling':ceiling,'outputs_sha256':{p.name:digest(p) for p in output.iterdir() if p.is_file()}}
    (output/'metadata.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf8')
    print(json.dumps(info,indent=2))

REPRESENTATIONS = {
    "R0": ("MFCC", "#64748b"),
    "R1": ("PANNs CNN14", "#b45309"),
    "R2": ("BirdNET", "#147d64"),
    "R3": ("Kontrol acak", "#8b5a9f"),
}
CONDITIONS = ("Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB")
CONDITION_LABELS = ("Acuan", "+20", "+10", "0", "−5")

def plot_e2(frame, output):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.7), layout="constrained")
    for rep, (label, color) in REPRESENTATIONS.items():
        rows = frame.loc[frame.representation.eq(rep)].set_index("condition").loc[list(CONDITIONS)]
        axes[0].plot(CONDITION_LABELS, rows["mAP@10"], "o-", color=color, label=label)
        axes[1].plot(CONDITION_LABELS, 100 * rows.relative_retention, "o-", color=color)
    axes[0].set_ylabel("mAP@10")
    axes[1].set_ylabel("Retensi mAP@10 (%)")
    axes[1].axhline(100, color="#68717b", linestyle=":", linewidth=1)
    for ax in axes:
        ax.set_xlabel("Kondisi kueri dan SNR (dB)")
        ax.grid(axis="y", alpha=0.23)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside upper center", ncol=4, frameon=False)
    fig.savefig(output, dpi=300, facecolor="white")
    plt.close(fig)

def plot_query_example(manifest_path, score_path, output):
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from src.mfcc import extract_mfcc_representation
    from src.mix_noise import mix_audio_at_snr
    from src.preprocess import TARGET_SR, preprocess_audio

    manifest = pd.read_csv(manifest_path).set_index("recording_id")
    recording_id = "XC42472"
    row = manifest.loc[recording_id]
    score = pd.read_csv(score_path, low_memory=False).set_index("query_id").loc[recording_id]
    clean = preprocess_audio(str(ROOT / row.file_path))
    noisy, audit = mix_audio_at_snr(
        clean, float(score.snr_db), seed=int(score.noise_seed), return_audit_info=True,
    )
    if (audit["noise_file"] != score.noise_file
            or audit["noise_start_sample"] != score.noise_start_sample
            or not np.isclose(audit["snr_db_achieved"], score.snr_db_achieved, atol=1e-6, rtol=0)):
        raise ValueError(f"Potongan derau tidak cocok untuk {recording_id}")

    fig, axes = plt.subplots(2, 2, figsize=(9, 5.2), layout="constrained")
    time = np.arange(len(clean)) / TARGET_SR
    peak = max(np.max(np.abs(clean)), np.max(np.abs(noisy))) * 1.03
    conditions = ((clean, "Tanpa derau tambahan"), (noisy, f"SNR tercapai {audit['snr_db_achieved']:.0f} dB"))
    for index, (audio, label) in enumerate(conditions):
        waveform, feature = axes[:, index]
        waveform.plot(time, audio, color="#176e73", lw=0.6)
        waveform.set(xlabel="Waktu (detik)", title=label, xlim=(0, time[-1]), ylim=(-peak, peak))
        vector = extract_mfcc_representation(audio, TARGET_SR)
        feature.bar(np.arange(1, 21), vector[:20], color="#176e73", label="Rata-rata")
        feature.bar(np.arange(21, 41), vector[20:], color="#ad6738", label="Simpangan baku")
        feature.set_xlabel("Komponen vektor MFCC")
        feature.grid(axis="y", alpha=0.2)
    axes[0, 0].set_ylabel("Amplitudo")
    axes[1, 0].set_ylabel("Nilai ternormalisasi")
    axes[1, 1].legend(loc="lower right", frameon=False, fontsize=8)
    fig.suptitle(f"Rekaman {recording_id} · {row.scientific_name}")
    axes[1, 1].sharey(axes[1, 0])
    fig.savefig(output, dpi=300, facecolor="white")
    plt.close(fig)
    return {"query_id": recording_id, "noise_file": audit["noise_file"], "noise_start_sample": audit["noise_start_sample"]}

def plot_e3(scores, output):
    fig, axes = plt.subplots(2, 2, figsize=(9, 5.8), layout="constrained")
    for ax, (rep, (label, _)) in zip(axes.flat, REPRESENTATIONS.items()):
        rows = scores[scores.representation.eq(rep)]
        thresholds = rows.frozen_tau.unique()
        if len(thresholds) != 1:
            raise ValueError(f"Tidak ada satu ambang kalibrasi untuk {rep}")
        bins = np.histogram_bin_edges(rows.similarity_score, bins=22)
        for is_target, group_name, color in ((1, "Target", "#147d64"), (0, "Di luar target", "#b45309")):
            values = rows.loc[rows.ground_truth.eq(is_target), "similarity_score"]
            ax.hist(values, bins=bins, weights=np.ones(len(values)) / len(values) * 100,
                    alpha=0.65, color=color, label=group_name)
        tau = thresholds[0]
        ax.axvline(tau, color="#252525", linestyle="--", label=f"Ambang {tau:.4f}")
        ax.set(title=label, xlabel="Skor kemiripan tertinggi", ylabel="Persentase kueri (%)")
        ax.legend(fontsize=8, frameon=False)
    fig.suptitle("Skor dan ambang pada data kalibrasi")
    fig.savefig(output, dpi=300, facecolor="white")
    plt.close(fig)

def plot_e4(frame, output):
    measured = frame[frame.repeat_id.ge(0)]
    group_sizes = measured.groupby(["representation", "habitat", "snr_db"]).size()
    if len(group_sizes) != 80 or not group_sizes.eq(4).all():
        raise ValueError("Tabel E4 harus memuat lima lokasi, empat SNR, dan empat ulangan.")
    means = measured.groupby(["representation", "habitat", "snr_db"], as_index=False)["mAP@10"].mean()
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.1), sharex=True, sharey=True, layout="constrained")
    levels = [20, 10, 0, -5]
    for ax, (rep, (label, _)) in zip(axes.flat, REPRESENTATIONS.items()):
        panel = means[means.representation.eq(rep)]
        for habitat, rows in panel.groupby("habitat"):
            ax.plot(CONDITION_LABELS[1:], rows.set_index("snr_db").loc[levels, "mAP@10"],
                    "o-", lw=1.4, label=habitat.replace("_", " "))
        ax.set_title(label)
        ax.grid(axis="y", alpha=0.23)
    fig.supxlabel("SNR (dB)")
    fig.supylabel("mAP@10 rata-rata empat ulangan")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside upper center", ncol=3, frameon=False)
    fig.savefig(output, dpi=300, facecolor="white")
    plt.close(fig)

def build_experiment_figures(output, e2_run, e3_run=None, e4_run=None):
    output = output.resolve()
    if output.parent != (ROOT / "paper/figures").resolve():
        raise ValueError("Gunakan direktori keluaran di paper/figures.")
    e2_summary = e2_run.resolve() / "tables/e2_snr_robustness.csv"
    e2_example = e2_run.resolve() / "raw/R0_SNR_0dB.csv"
    manifest = ROOT / "data/manifests/dataset_split.csv"
    output.mkdir(parents=True, exist_ok=True)
    metadata_file = output / "sumber_gambar.json"
    sources = json.loads(metadata_file.read_text(encoding="utf-8")) if metadata_file.is_file() else {}
    plot_e2(pd.read_csv(e2_summary), output / "e2_kualitas_dan_retensi.png")
    sources["e2_kualitas_dan_retensi.png"] = {"table": str(e2_summary.relative_to(ROOT))}
    example = plot_query_example(manifest, e2_example, output / "e2_contoh_kueri_dan_mfcc.png")
    sources["e2_contoh_kueri_dan_mfcc.png"] = {
        "table": str(e2_example.relative_to(ROOT)), "manifest": str(manifest.relative_to(ROOT)), **example,
    }
    if e3_run:
        calibration = e3_run.resolve() / "raw/calibration_scores.csv"
        plot_e3(pd.read_csv(calibration), output / "e3_distribusi_skor_dan_ambang.png")
        sources["e3_distribusi_skor_dan_ambang.png"] = {"table": str(calibration.relative_to(ROOT))}
    if e4_run:
        locations = e4_run.resolve() / "tables/e4_domain_shift_table.csv"
        plot_e4(pd.read_csv(locations), output / "e4_perbandingan_lima_lokasi.png")
        sources["e4_perbandingan_lima_lokasi.png"] = {"table": str(locations.relative_to(ROOT))}
    metadata_file.write_text(json.dumps(sources, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Gambar hasil dan sumber tersedia di {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--e2-run", type=Path)
    parser.add_argument("--e3-run", type=Path)
    parser.add_argument("--e4-run", type=Path)
    args = parser.parse_args()
    if args.e2_run:
        build_experiment_figures(args.output_dir, args.e2_run, args.e3_run, args.e4_run)
    elif args.e3_run or args.e4_run:
        parser.error("--e3-run dan --e4-run memerlukan --e2-run")
    else:
        main(args.output_dir)
