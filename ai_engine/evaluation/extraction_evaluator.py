import os
import pandas as pd
import matplotlib.pyplot as plt
from ai_engine.pipeline import analyze_document
from ai_engine.preprocessing.field_normalizer import normalize_field_value
from ai_engine.config.settings import DATA_PROCESSED_DIR

FIELDS_TO_EVALUATE = [
    "report_number",
    "state",
    "district",
    "block",
    "habitation_name",
    "habitation_id",
    "facility_name",
    "facility_category",
    "facility_subcategory",
    "inspection_date",
    "inspection_type",
    "inspector_name",
    "quality_status"
]

def evaluate_extraction(image_paths: list, ground_truth_records: list, output_plots_dir: str = None) -> tuple:
    """
    Evaluates OCR layout extraction accuracy against ground-truth records.
    Generates comparison tables, aggregates accuracies, and plots performance metrics.
    """
    if not image_paths or not ground_truth_records:
        raise ValueError("Image paths and ground-truth records list must not be empty.")

    all_extraction_results = []
    all_field_details = []

    for index, image_path in enumerate(image_paths):
        if index >= len(ground_truth_records):
            break

        ground_truth = ground_truth_records[index]

        # Run extraction pipeline
        result = analyze_document(image_path)
        extracted = result.get("extracted_fields", {})

        correct = 0
        total = 0

        for field in FIELDS_TO_EVALUATE:
            actual = normalize_field_value(field, ground_truth.get(field))
            predicted = normalize_field_value(field, extracted.get(field))

            # Skip checking if ground truth is empty
            if actual == "":
                continue

            total += 1
            if actual == predicted:
                correct += 1
                status = "CORRECT"
            else:
                status = "WRONG"

            all_field_details.append({
                "image": os.path.basename(image_path),
                "field": field,
                "ground_truth": ground_truth.get(field),
                "extracted": extracted.get(field),
                "status": status
            })

        accuracy = (correct / total * 100) if total else 0.0
        all_extraction_results.append({
            "image": os.path.basename(image_path),
            "correct": correct,
            "total": total,
            "accuracy": accuracy
        })

    accuracy_df = pd.DataFrame(all_extraction_results)
    field_details_df = pd.DataFrame(all_field_details)

    avg_accuracy = accuracy_df["accuracy"].mean() if not accuracy_df.empty else 0.0

    print(f"[Extraction Evaluator] Average field extraction accuracy: {avg_accuracy:.2f}%")

    # Generate graphs if directory is supplied
    if output_plots_dir:
        os.makedirs(output_plots_dir, exist_ok=True)
        plot_accuracy_chart(avg_accuracy, output_plots_dir)

    return accuracy_df, field_details_df

def plot_accuracy_chart(avg_accuracy: float, output_dir: str):
    """
    Saves the matplotlib bar charts for documentation and presentations.
    """
    try:
        # 1. OCR Field Extraction Bar Chart
        fig1, ax1 = plt.subplots(figsize=(10, 7), facecolor='white')
        ax1.bar(
            ['Average Field Extraction Accuracy'],
            [avg_accuracy],
            color='#4CAF50',
            width=0.4
        )
        ax1.text(
            0,
            avg_accuracy + 1,
            f'{avg_accuracy:.2f}%',
            ha='center',
            va='bottom',
            fontsize=18,
            color='black',
            fontweight='bold'
        )
        ax1.set_title(
            'Document AI / OCR Field Extraction Accuracy',
            fontsize=20,
            fontweight='bold',
            color='black',
            pad=20
        )
        ax1.set_ylabel('Accuracy (%)', fontsize=16, color='black', labelpad=15)
        ax1.set_ylim(0, 100)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        graph_path = os.path.join(output_dir, "ocr_accuracy_graph.png")
        plt.savefig(graph_path, dpi=300)
        plt.close()
        print(f"[Extraction Evaluator] Saved evaluation plot: {graph_path}")
    except Exception as e:
        print(f"[Extraction Evaluator Warning] Matplotlib plotting skipped: {str(e)}")
