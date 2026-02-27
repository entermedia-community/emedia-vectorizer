from sentence_transformers import SentenceTransformer
import numpy as np 
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = SentenceTransformer('all-MiniLM-L6-v2', device=device, backend='torch' if device == "cuda" else 'onnx')

def parsenp(obj):
  if isinstance(obj, np.ndarray):
    return obj.tolist()
  if isinstance(obj, np.float32):
    return float(obj)
  if isinstance(obj, np.int64):
    return int(obj)
  return obj

def represent(data):
  results = []
  for d in data:
    id = d['id']
    text = d['text']
    try:
      embedding = model.encode(text)
      obj = {
        "id": id,
        "embedding": parsenp(embedding)
      }
      results.append(obj)
    except Exception as e:
      print(f"Error processing {id}: {e}")
      continue
  
  data = {
    "results": results,
    "received": len(data),
    "processed": len(results),
    "error": len(data) - len(results)
  }
  return parsenp(data)
