import os
from huggingface_hub import hf_hub_download

REPO = "YassineCHN/SISE_Models"

FILES = {
    "data": [
        "donnees_dpe_73_clean.csv",
        "donnees_dpe_existants_73.csv",
        "donnees_dpe_neufs_73.csv",
    ],
    "models": [
        "model_CONSO_Random_Forest.pkl",
        "model_DPE_latest.pkl",
        "model_DPE_Random_Forest.pkl",
        "model_MPR_latest.pkl",
        "model_MPR_Random_Forest.pkl",
        "preprocessor_conso.pkl",
    ],
}

def ensure_dirs():
    os.makedirs("/app/data", exist_ok=True)
    os.makedirs("/app/models", exist_ok=True)

def download_all():
    for folder, file_list in FILES.items():
        for fname in file_list:
            target = f"/app/{folder}"
            print(f"⬇️  Téléchargement {fname} → {target}")
            path = hf_hub_download(
                repo_id=REPO,
                filename=fname,
                repo_type="dataset",
                local_dir=target,
                local_dir_use_symlinks=False,
                token=os.getenv("HF_TOKEN")
            )
            print(f"✅ {fname} prêt ({path})")

if __name__ == "__main__":
    ensure_dirs()
    download_all()
    print("\n✅ Tous les fichiers Hugging Face sont disponibles.")
