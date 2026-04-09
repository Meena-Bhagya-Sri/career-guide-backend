import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# =========================
# 1. Load Dataset
# =========================
DATASET_PATH = "skill_career_dataset.csv"
df = pd.read_csv(DATASET_PATH)

# =========================
# 2. Separate Features & Target
# =========================
X = df.drop(columns=["career_label"])
y = df["career_label"]

# =========================
# 3. Encode Target Labels
# =========================
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# =========================
# 4. Train-Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.3,
    random_state=42,
    stratify=y_encoded
)

# =========================
# 5. Train Random Forest
# =========================
rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    class_weight="balanced"
)

rf_model.fit(X_train, y_train)

# =========================
# 6. Evaluate Model
# =========================
y_pred = rf_model.predict(X_test)

print("\n✅ Model Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# =========================
# 7. Save Model & Encoder
# =========================
joblib.dump(rf_model, "career_rf_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("\n✅ Model saved as career_rf_model.pkl")
print("✅ Label encoder saved as label_encoder.pkl")