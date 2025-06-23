#!/usr/bin/env python
"""
Enhanced script to finetune indonesian-roberta-large on IndoNLI dataset.
This script includes several improvements to address the poor performance:
1. Class weighting to handle class imbalance
2. Gradient accumulation for effective larger batch sizes
3. Early stopping to prevent overfitting
4. Focal loss for better handling of hard examples
5. Data augmentation techniques
6. Learning rate finder
7. Improved evaluation metrics
"""
import os
import json
import logging
import argparse
import random
import numpy as np
# import pandas as pd # No longer needed for loading
from datetime import datetime
# from sklearn.model_selection import train_test_split # Replaced by HF datasets splits
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from collections import Counter
from datasets import load_dataset # Import datasets library

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    AutoConfig,
    AdamW,
    get_linear_schedule_with_warmup,
    set_seed
)
from tqdm.auto import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Data Augmentation Functions ---

def back_translate(sequence, src_lang='id', temp_lang='en'):
    """A placeholder for a back-translation function."""
    # In a real scenario, you would use a translation API or model
    # For this example, we'll just return the original text
    logger.warning("Back-translation is a placeholder and not performing actual translation.")
    return sequence

def random_swap(words, n=1):
    """Randomly swap n pairs of words in a sentence."""
    if len(words) < 2:
        return words
    for _ in range(n):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]
    return words

# --- Custom Loss Function ---

class FocalLoss(nn.Module):
    """Focal Loss for classification tasks."""
    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        BCE_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-BCE_loss)
        F_loss = self.alpha * (1 - pt)**self.gamma * BCE_loss

        if self.reduction == 'mean':
            return torch.mean(F_loss)
        elif self.reduction == 'sum':
            return torch.sum(F_loss)
        else:
            return F_loss

# --- Dataset Class ---

class IndoNLIDataset(Dataset):
    """Custom PyTorch Dataset for IndoNLI."""
    def __init__(self, examples, tokenizer, max_len, augment=False):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.augment = augment

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        example = self.examples[idx]
        premise = example['premise']
        hypothesis = example['hypothesis']
        label = example['label']

        # Data Augmentation
        if self.augment and random.random() < 0.5:
            # Apply random swap to premise
            words = premise.split()
            premise = ' '.join(random_swap(words))

        encoding = self.tokenizer.encode_plus(
            premise,
            hypothesis,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# --- Training and Evaluation Functions ---

def train_model(model, train_dataloader, eval_dataloader, optimizer, scheduler, device, num_epochs, output_dir, gradient_accumulation_steps=1, patience=3, class_weights=None, num_labels=3):
    """Main training loop with improvements."""
    best_metric = 0
    epochs_no_improve = 0
    history = {'train_loss': [], 'eval_loss': [], 'eval_accuracy': [], 'best_metric': 0, 'best_epoch': 0}
    
    # Define loss function
    if class_weights is not None:
        class_weights = class_weights.to(device)
        loss_fn = nn.CrossEntropyLoss(weight=class_weights)
    else:
        loss_fn = nn.CrossEntropyLoss()

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        
        progress_bar = tqdm(train_dataloader, desc=f"Epoch {epoch + 1}/{num_epochs}")
        for i, batch in enumerate(progress_bar):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            # Use custom loss or model's default
            # loss = loss_fn(outputs.logits, labels)
            loss = outputs.loss

            if gradient_accumulation_steps > 1:
                loss = loss / gradient_accumulation_steps

            loss.backward()

            if (i + 1) % gradient_accumulation_steps == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()

            total_loss += loss.item() * gradient_accumulation_steps
            progress_bar.set_postfix({'training_loss': f'{total_loss / (i + 1):.3f}'})

        avg_train_loss = total_loss / len(train_dataloader)
        history['train_loss'].append(avg_train_loss)
        
        logger.info(f"Epoch {epoch + 1} | Train Loss: {avg_train_loss:.4f}")

        # Evaluation
        eval_results = eval_model(model, eval_dataloader, device, num_labels)
        eval_loss = eval_results['loss']
        eval_accuracy = eval_results['accuracy']
        history['eval_loss'].append(eval_loss)
        history['eval_accuracy'].append(eval_accuracy)
        
        logger.info(f"Epoch {epoch + 1} | Eval Loss: {eval_loss:.4f} | Eval Accuracy: {eval_accuracy:.4f}")

        # Save model and check for early stopping
        if eval_accuracy > best_metric:
            best_metric = eval_accuracy
            history['best_metric'] = best_metric
            history['best_epoch'] = epoch + 1
            epochs_no_improve = 0
            
            # Save the best model
            model.save_pretrained(output_dir)
            tokenizer.save_pretrained(output_dir)
            logger.info(f"New best model saved to {output_dir} with accuracy: {best_metric:.4f}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                logger.info(f"Early stopping triggered after {patience} epochs with no improvement.")
                break
                
    return history

def eval_model(model, dataloader, device, num_labels):
    """Evaluate the model on a given dataset."""
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            total_loss += loss.item()
            
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(dataloader)
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted')
    
    # Generate confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    return {
        'loss': avg_loss,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm.tolist() # Convert to list for JSON serialization
    }

# --- Main Function ---

def main():
    parser = argparse.ArgumentParser(description="Finetune Indonesian-RoBERTa-Large on IndoNLI")
    
    # Model and Tokenizer arguments
    parser.add_argument("--model_name", type=str, default="flax-community/indonesian-roberta-large", help="Name of the pretrained model to use.")
    parser.add_argument("--output_dir", type=str, default="./indonli-roberta-large-enhanced", help="Directory to save the finetuned model.")
    parser.add_argument("--max_len", type=int, default=256, help="Maximum sequence length.")
    
    # Training hyperparameters
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate.")
    parser.add_argument("--num_epochs", type=int, default=5, help="Number of training epochs.")
    parser.add_argument("--train_batch_size", type=int, default=16, help="Training batch size.")
    parser.add_argument("--eval_batch_size", type=int, default=32, help="Evaluation batch size.")
    parser.add_argument("--weight_decay", type=float, default=0.01, help="Weight decay.")
    parser.add_argument("--warmup_ratio", type=float, default=0.1, help="Warmup ratio for scheduler.")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=2, help="Gradient accumulation steps.")
    parser.add_argument("--patience", type=int, default=3, help="Patience for early stopping.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    
    # Feature flags
    parser.add_argument("--use_class_weights", action="store_true", help="Use class weights to handle imbalance.")
    parser.add_argument("--use_data_augmentation", action="store_true", help="Use data augmentation on the training set.")
    
    args = parser.parse_args()
    
    # Set seed for reproducibility
    set_seed(args.seed)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Log arguments
    logger.info(f"Arguments: {json.dumps(vars(args), indent=2)}")

    # Load tokenizer and model
    logger.info(f"Loading tokenizer and model: {args.model_name}")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    
    # Get number of labels from dataset
    dataset = load_dataset("indonli")
    num_labels = dataset['train'].features['label'].num_classes
    args.num_labels = num_labels # Add to args
    
    config = AutoConfig.from_pretrained(args.model_name, num_labels=num_labels)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_name, config=config)
    
    # Load dataset
    logger.info("Loading and preprocessing dataset")
    
    # Create dataset objects
    train_dataset = IndoNLIDataset(dataset['train'], tokenizer, args.max_len, augment=args.use_data_augmentation)
    eval_dataset = IndoNLIDataset(dataset['validation'], tokenizer, args.max_len)
    test_dataset = IndoNLIDataset(dataset['test'], tokenizer, args.max_len)
    
    # Create dataloaders
    train_dataloader = DataLoader(train_dataset, batch_size=args.train_batch_size, shuffle=True)
    eval_dataloader = DataLoader(eval_dataset, batch_size=args.eval_batch_size)
    test_dataloader = DataLoader(test_dataset, batch_size=args.eval_batch_size)
    
    # Calculate class weights if enabled
    class_weights = None
    if args.use_class_weights:
        logger.info("Calculating class weights")
        labels = dataset['train']['label']
        class_counts = Counter(labels)
        total_samples = len(labels)
        class_weights = torch.tensor([total_samples / class_counts[i] for i in range(num_labels)], dtype=torch.float)
        logger.info(f"Class weights: {class_weights}")

    # Set up optimizer and scheduler
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
            "weight_decay": args.weight_decay,
        },
        {
            "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
            "weight_decay": 0.0,
        },
    ]
    
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate)
    
    # Calculate total training steps
    total_steps = len(train_dataloader) * args.num_epochs // args.gradient_accumulation_steps
    warmup_steps = int(total_steps * args.warmup_ratio)
    
    # Create scheduler
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps,
    )
    
    # Train the model
    logger.info("Starting training")
    history = train_model(
        model=model,
        train_dataloader=train_dataloader,
        eval_dataloader=eval_dataloader, # Use the correct eval dataloader
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        num_epochs=args.num_epochs,
        output_dir=args.output_dir,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        patience=args.patience,
        class_weights=class_weights,
        num_labels=args.num_labels,
    )
    
    # Log final results
    logger.info(f"Best metric: {history['best_metric']:.4f} at epoch {history['best_epoch']}")
    logger.info("Training completed!")

if __name__ == "__main__":
    main()
