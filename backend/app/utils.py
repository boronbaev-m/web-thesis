import torch
from transformers import RobertaTokenizer, AutoModelForSequenceClassification
from app.models import Code
from app import db

model_path = "model"
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
model = AutoModelForSequenceClassification.from_pretrained(model_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

def check_code(code_id):
    code_entry = Code.query.get(code_id)
    tokenized_input = tokenizer(code_entry.content, return_tensors='pt', truncation=True, padding=True)
    input_ids = tokenized_input['input_ids'].to(device)
    attention_mask = tokenized_input['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        prediction = predictions.cpu().item()
    code_entry.result = str(prediction)
    db.session.commit()
    return code_entry.id

def check_code_raw(code):
    tokenized_input = tokenizer(code, return_tensors='pt', truncation=True, padding=True)
    input_ids = tokenized_input['input_ids'].to(device)
    attention_mask = tokenized_input['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        prediction = predictions.cpu().item()
    return str(prediction)
