import numpy as np
from typing import Dict
from evaluate import load
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Load ROUGE for SOAP note evaluation
rouge_metric = load("rouge")

def compute_metrics(eval_preds):
    """
    Computes multi-task metrics for MedGemma.
    This function expects to handle different labels based on the prompt task.
    In practice, for instruction tuning, one might need to parse the generated response
    back into task-specific formats for proper evaluation.
    """
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    
    # Placeholder for multi-task metric aggregation
    # Real implementation would separate tasks by inspecting the input tokens
    
    # Generic accuracy for classification tasks (Triage/Red-flag)
    # Note: For generative SOAP notes, ROUGE is more appropriate.
    
    return {
        "accuracy": accuracy_score(labels.flatten(), predictions.flatten())
    }

def calculate_triage_metrics(y_true, y_pred):
    """
    Calculates ESI Triage specific metrics: Accuracy, Sensitivity, Specificity.
    """
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    
    return {
        "triage_accuracy": accuracy,
        "triage_f1": f1,
        "triage_sensitivity": recall, # Recall is sensitivity for the positive class or weighted
    }

def calculate_redflag_metrics(y_true, y_pred):
    """
    Calculates Precision/Recall for Red-flag detection.
    """
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', pos_label=1, zero_division=0)
    return {
        "redflag_precision": precision,
        "redflag_recall": recall,
        "redflag_f1": f1
    }

def calculate_soap_metrics(predictions: list, references: list):
    """
    Calculates ROUGE scores for SOAP notes.
    """
    results = rouge_metric.compute(predictions=predictions, references=references)
    return {
        "soap_rouge1": results["rouge1"],
        "soap_rouge2": results["rouge2"],
        "soap_rougeL": results["rougeL"]
    }
