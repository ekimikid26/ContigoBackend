"""
Script de fine-tuning de BETO para detección de indicadores 
lingüísticos asociados al TAG en texto en español.
"""

import json
import os
import numpy as np

SYNTHETIC_TEXTS = [
    {"text": "Hoy fue un día tranquilo, me siento bien descansado.", "label": 0},
    {"text": "Salí a caminar y me sentí con energía.", "label": 0},
    {"text": "Me costó un poco concentrarme hoy.", "label": 1},
    {"text": "Estuve pensando mucho en el trabajo de mañana.", "label": 1},
    {"text": "No puedo dejar de preocuparme por todo.", "label": 2},
    {"text": "Estoy muy tenso y no sé por qué.", "label": 2},
    {"text": "Siento que algo malo va a pasar, no puedo calmarme.", "label": 3},
    {"text": "Estoy en pánico y no sé cómo manejarlo.", "label": 3},
]

def prepare_dataset():
    """Prepara el dataset para fine-tuning de BETO."""
    try:
        from datasets import Dataset
        from transformers import (
            AutoTokenizer, AutoModelForSequenceClassification,
            TrainingArguments, Trainer
        )
        
        print("Cargando BETO...")
        model_name = "dccuchile/bert-base-spanish-wwm-cased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        dataset = Dataset.from_list(SYNTHETIC_TEXTS)
        dataset = dataset.train_test_split(test_size=0.2, seed=42)
        
        def tokenize(batch):
            return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=128)
        
        tokenized = dataset.map(tokenize, batched=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=4)
        
        output_dir = "ml/models/beto_contigo"
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=8,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            logging_dir="ml/logs",
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized["train"],
            eval_dataset=tokenized["test"],
        )
        
        print("Iniciando fine-tuning...")
        trainer.train()
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"✅ Modelo BETO guardado en: {output_dir}")
        
    except ImportError as e:
        print(f"Instala dependencias: pip install transformers datasets torch")

if __name__ == "__main__":
    prepare_dataset()
