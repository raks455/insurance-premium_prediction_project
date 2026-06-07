
import pickle
import pandas as pd
with open("model/model.pkl","rb") as f:
    model=pickle.load(f)

MODEL_VERSION='1.0.0'
class_labels=model.classes_.tolist()
def predict_output(userinput:dict):
    df=pd.DataFrame([userinput])
    predicted_class=model.predict(df)[0]
    probabilites=model.predict_proba(df)[0]
    confidence=max(probabilites)
    class_probs=dict(zip(class_labels,map(lambda p:round(p,4),probabilites)))
    return {
        "predicted_category":predicted_class,
        "confidence":round(confidence,4),
        "class_probabilites":class_probs
    }