import torch
from PIL import Image
import clip

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

RISK_LABELS = [
    "a conservative investor",
    "a moderate risk-taker",
    "a high-risk aggressive investor",
    "a luxury-seeking individual",
    "a calm, cautious person"
]

def classify_image(image_path, labels=RISK_LABELS):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    text_inputs = torch.cat([clip.tokenize(label) for label in labels]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        best_match_idx = similarity.argmax().item()

    return labels[best_match_idx], similarity[0][best_match_idx].item()
