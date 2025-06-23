import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset, load_metric

def main():
    # 1. Load IndoNLI dataset
    print("Loading IndoNLI dataset...")
    # You might need to specify the correct dataset name or path
    # For example: dataset = load_dataset("indonli") or load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
    # For now, using a placeholder
    try:
        dataset = load_dataset("indonli")
    except Exception as e:
        print(f"Could not load 'indonli' directly. Please ensure it's available or provide a local path. Error: {e}")
        print("Attempting to load a dummy dataset for demonstration purposes.")
        # Create a dummy dataset for demonstration if indonli is not directly available
        from datasets import Dataset
        dummy_data = {
            "premise": ["This is a premise.", "Another premise here."],
            "hypothesis": ["This is a hypothesis.", "And another one."],
            "label": [0, 1] # Example labels
        }
        dataset = Dataset.from_dict(dummy_data).train_test_split(test_size=0.2)
        dataset["validation"] = dataset["test"] # Use test split as validation for simplicity

    print("Dataset loaded.")
    print(dataset)

    # 2. Preprocessing function
    def preprocess_function(examples, tokenizer):
        return tokenizer(examples["premise"], examples["hypothesis"], truncation=True, padding="max_length")

    # 3. Fine-tune indoreoberta
    print("\n--- Fine-tuning indoreoberta ---")
    model_name_roberta = "indolem/indoreoberta-base"
    tokenizer_roberta = AutoTokenizer.from_pretrained(model_name_roberta)
    model_roberta = AutoModelForSequenceClassification.from_pretrained(model_name_roberta, num_labels=3) # Assuming 3 labels for NLI (entailment, neutral, contradiction)

    tokenized_datasets_roberta = dataset.map(lambda x: preprocess_function(x, tokenizer_roberta), batched=True)

    training_args_roberta = TrainingArguments(
        output_dir="./results_indoreoberta",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
    )

    metric = load_metric("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = torch.argmax(torch.tensor(logits), dim=-1)
        return metric.compute(predictions=predictions, references=labels)

    trainer_roberta = Trainer(
        model=model_roberta,
        args=training_args_roberta,
        train_dataset=tokenized_datasets_roberta["train"],
        eval_dataset=tokenized_datasets_roberta["validation"],
        tokenizer=tokenizer_roberta,
        compute_metrics=compute_metrics,
    )

    trainer_roberta.train()
    print("indoreoberta fine-tuning complete.")
    print("Evaluating indoreoberta...")
    eval_results_roberta = trainer_roberta.evaluate()
    print(f"indoreoberta evaluation results: {eval_results_roberta}")

    # 4. Fine-tune indoBERT
    print("\n--- Fine-tuning indoBERT ---")
    model_name_bert = "indobenchmark/indobert-base-p1" # Or indobenchmark/indobert-large-p2
    tokenizer_bert = AutoTokenizer.from_pretrained(model_name_bert)
    model_bert = AutoModelForSequenceClassification.from_pretrained(model_name_bert, num_labels=3) # Assuming 3 labels for NLI

    tokenized_datasets_bert = dataset.map(lambda x: preprocess_function(x, tokenizer_bert), batched=True)

    training_args_bert = TrainingArguments(
        output_dir="./results_indobert",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
    )

    trainer_bert = Trainer(
        model=model_bert,
        args=training_args_bert,
        train_dataset=tokenized_datasets_bert["train"],
        eval_dataset=tokenized_datasets_bert["validation"],
        tokenizer=tokenizer_bert,
        compute_metrics=compute_metrics,
    )

    trainer_bert.train()
    print("indoBERT fine-tuning complete.")
    print("Evaluating indoBERT...")
    eval_results_bert = trainer_bert.evaluate()
    print(f"indoBERT evaluation results: {eval_results_bert}")

if __name__ == "__main__":
    main()
