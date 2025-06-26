import torch
import mlflow
import json
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import evaluate


def main():
    # 1. Load IndoNLI dataset
    print("Loading IndoNLI dataset...")
    dataset = load_dataset("afaji/indonli", trust_remote_code=True)

    print("Dataset loaded.")
    print(dataset)

    # 2. Preprocessing function
    def preprocess_function(examples, tokenizer):
        return tokenizer(examples["premise"], examples["hypothesis"], truncation=True, padding="max_length")

        # 3. Fine-tune indoreoberta

    print("\n--- Fine-tuning indoreoberta ---")
    model_name_roberta = "flax-community/indonesian-roberta-base"
    tokenizer_roberta = AutoTokenizer.from_pretrained(model_name_roberta)
    model_roberta = AutoModelForSequenceClassification.from_pretrained(model_name_roberta, num_labels=3)

    tokenized_datasets_roberta = dataset.map(lambda x: preprocess_function(x, tokenizer_roberta), batched=True)

    training_args_roberta = TrainingArguments(
        output_dir="./results_indoreoberta",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=1,  # CHANGED: Set to 1 epoch
        weight_decay=0.01,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to=["mlflow", "tensorboard"],
    )

    metric = evaluate.load("accuracy")

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

    mlflow.start_run(run_name="indoreoberta-finetune")

    trainer_roberta.train()
    print("indoreoberta fine-tuning complete.")
    print("Evaluating indoreoberta...")
    eval_results_roberta = trainer_roberta.evaluate()
    print(f"indoreoberta evaluation results: {eval_results_roberta}")
    mlflow.log_metrics(eval_results_roberta)

    # Save metrics for DVC
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/roberta_metrics.json", "w") as f:
        json.dump(eval_results_roberta, f, indent=4)

    mlflow.end_run()

    # 4. Fine-tune indoBERT
    print("\n--- Fine-tuning indoBERT ---")
    model_name_bert = "indobenchmark/indobert-base-p1"
    tokenizer_bert = AutoTokenizer.from_pretrained(model_name_bert)
    model_bert = AutoModelForSequenceClassification.from_pretrained(model_name_bert, num_labels=3)

    tokenized_datasets_bert = dataset.map(lambda x: preprocess_function(x, tokenizer_bert), batched=True)

    training_args_bert = TrainingArguments(
        output_dir="./results_indobert",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=1,  # CHANGED: Set to 1 epoch
        weight_decay=0.01,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to=["mlflow", "tensorboard"],
    )

    trainer_bert = Trainer(
        model=model_bert,
        args=training_args_bert,
        train_dataset=tokenized_datasets_bert["train"],
        eval_dataset=tokenized_datasets_bert["validation"],
        tokenizer=tokenizer_bert,
        compute_metrics=compute_metrics,
    )

    mlflow.start_run(run_name="indobert-finetune")

    trainer_bert.train()
    print("indoBERT fine-tuning complete.")
    print("Evaluating indoBERT...")
    eval_results_bert = trainer_bert.evaluate()
    print(f"indoBERT evaluation results: {eval_results_bert}")
    mlflow.log_metrics(eval_results_bert)

    # Save metrics for DVC
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/bert_metrics.json", "w") as f:
        json.dump(eval_results_bert, f, indent=4)

    mlflow.end_run()


if __name__ == "__main__":
    # ADD THIS LINE to prevent the out-of-memory error by only using the first GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    main()
    )
<<<<<<< HEAD

    mlflow.start_run(run_name="indoreoberta-finetune")

    trainer_roberta.train()
    print("indoreoberta fine-tuning complete.")
    print("Evaluating indoreoberta...")
    eval_results_roberta = trainer_roberta.evaluate()
    print(f"indoreoberta evaluation results: {eval_results_roberta}")
    mlflow.log_metrics(eval_results_roberta)

    # Save metrics for DVC
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/roberta_metrics.json", "w") as f:
        json.dump(eval_results_roberta, f, indent=4)

    mlflow.end_run()

    # 4. Fine-tune indoBERT
    print("\n--- Fine-tuning indoBERT ---")
    model_name_bert = "indobenchmark/indobert-base-p1"
    tokenizer_bert = AutoTokenizer.from_pretrained(model_name_bert)
    model_bert = AutoModelForSequenceClassification.from_pretrained(model_name_bert, num_labels=3)

    tokenized_datasets_bert = dataset.map(lambda x: preprocess_function(x, tokenizer_bert), batched=True)

    training_args_bert = TrainingArguments(
        output_dir="./results_indobert",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=1,  # CHANGED: Set to 1 epoch
        weight_decay=0.01,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to=["mlflow", "tensorboard"],
    )

    trainer_bert = Trainer(
        model=model_bert,
        args=training_args_bert,
        train_dataset=tokenized_datasets_bert["train"],
        eval_dataset=tokenized_datasets_bert["validation"],
        tokenizer=tokenizer_bert,
        compute_metrics=compute_metrics,
    )

    mlflow.start_run(run_name="indobert-finetune")

    trainer_bert.train()
    print("indoBERT fine-tuning complete.")
    print("Evaluating indoBERT...")
    eval_results_bert = trainer_bert.evaluate()
    print(f"indoBERT evaluation results: {eval_results_bert}")
    mlflow.log_metrics(eval_results_bert)

    # Save metrics for DVC
    os.makedirs("metrics", exist_ok=True)
    with open("metrics/bert_metrics.json", "w") as f:
        json.dump(eval_results_bert, f, indent=4)

    mlflow.end_run()
=======
    
    # Log final results
    logger.info(f"Best metric: {history['best_metric']:.4f} at epoch {history['best_epoch']}")
    logger.info("Training completed!")
>>>>>>> 147e4c19ac7b1e058ebde56670c99049c449e4f9


if __name__ == "__main__":
    # ADD THIS LINE to prevent the out-of-memory error by only using the first GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    main()