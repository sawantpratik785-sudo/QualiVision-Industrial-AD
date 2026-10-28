import torch
from dataset import MVTecDataset
from patchcore import PatchCore
from db_logger import init_db, log_inspection, fetch_recent_logs
from torch.utils.data import DataLoader
import numpy as np

def run_pipeline():
    print("==================================================")
    print("STEP 1: INITIALIZING SQLITE DATABASE")
    print("==================================================")
    init_db()
    print("Database `inspections.db` ready.")

    print("\n==================================================")
    print("STEP 2: LOADING TRAINING DATA & BUILDING MEMORY BANK")
    print("==================================================")
    train_ds = MVTecDataset('./data', 'bottle', split='train')
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=False)
    print(f"Loaded {len(train_ds)} normal training images.")

    # Initialize PatchCore from scratch
    model = PatchCore(backbone_name='resnet18', coreset_ratio=0.01, device='cpu')
    model.fit(train_loader)

    print("\n==================================================")
    print("STEP 3: RUNNING INFERENCE & COMPARISON")
    print("==================================================")
    test_ds = MVTecDataset('./data', 'bottle', split='test')
    
    # Grab one defect sample and one good sample
    good_sample = None
    defect_sample = None
    for s in test_ds:
        if s['label'] == 0 and good_sample is None:
            good_sample = s
        elif s['label'] == 1 and defect_sample is None:
            defect_sample = s
        if good_sample is not None and defect_sample is not None:
            break

    threshold = 3.0

    # 1. Defective Sample
    print(f"\n---> [TEST 1] Defective Sample ({defect_sample['defect_type']})")
    score_def, map_def, lat_def = model.predict(defect_sample['image'].unsqueeze(0))
    verdict_def = "DEFECT" if score_def >= threshold else "PASS"
    print(f"     Calculated Anomaly Score : {score_def:.4f}")
    print(f"     Configured Threshold    : {threshold:.4f}")
    print(f"     Inference Latency       : {lat_def:.1f} ms")
    print(f"     Verdict                 : {verdict_def}")
    log_inspection('bottle', 'PatchCore', score_def, threshold, verdict_def, lat_def, f"{defect_sample['defect_type']}.png")

    # 2. Good Sample
    print(f"\n---> [TEST 2] Normal (Good) Sample ({good_sample['defect_type']})")
    score_good, map_good, lat_good = model.predict(good_sample['image'].unsqueeze(0))
    verdict_good = "DEFECT" if score_good >= threshold else "PASS"
    print(f"     Calculated Anomaly Score : {score_good:.4f}")
    print(f"     Configured Threshold    : {threshold:.4f}")
    print(f"     Inference Latency       : {lat_good:.1f} ms")
    print(f"     Verdict                 : {verdict_good}")
    log_inspection('bottle', 'PatchCore', score_good, threshold, verdict_good, lat_good, "good_sample.png")

    print("\n==================================================")
    print("STEP 4: INSPECTING SQLITE AUDIT TRAIL RECORDS")
    print("==================================================")
    logs = fetch_recent_logs(limit=4)
    print(f"{'Timestamp':<20} | {'Part':<8} | {'Model':<10} | {'Score':<8} | {'Verdict':<8} | {'Latency':<8}")
    print("-" * 75)
    for r in logs:
        print(f"{r[0]:<20} | {r[1]:<8} | {r[2]:<10} | {r[3]:<8.4f} | {r[5]:<8} | {r[6]:<8.1f} ms")

if __name__ == "__main__":
    run_pipeline()
