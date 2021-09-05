import joblib, json
from pathlib import Path

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, accuracy_score, recall_score, confusion_matrix

import numpy as np
import pandas as pd

import plotly.express as px

meta = {
    "n_features": 3,
    "n_classes": 4
}
cust_map = {
        0: 'price_buyer',
        1: 'loyal_customer',
        2: 'value_buyer',
        3: 'high_value',
}

if not Path('X.data').is_file() and not Path('y.data').is_file():
    X, y = make_classification(
        n_samples = 1000, 
        n_features = meta['n_features'], 
        n_informative = meta['n_features'],
        n_redundant = 0,
        n_classes = meta['n_classes'],    
    )
    np.savetxt('data/X.data', X)
    np.savetxt('data/y.data', y)
else:
    X = np.loadtxt('data/X.data')
    y = np.loadtxt('data/y.data')

def generate_vis():
    df = pd.DataFrame(X, columns=['time_on_site', 'time_in_checkout', 'time_on_sales_page'])
    df = df+5
    df['label'] = y
    
    df['label_cat'] = df.label.map(cust_map)
    fig = px.scatter_3d(df, x='time_on_site', y='time_in_checkout', z='time_on_sales_page',
              color='label_cat')

    fig.write_html("../vis.html")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=997)

pipeline = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(
        n_estimators=45, 
        criterion='entropy', 
        n_jobs=-1)
    )
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

f1 = f1_score(y_test, y_pred, average="weighted")

print(f'F1 Score: {f1:.4f}')

joblib.dump(pipeline, 'model/model.joblib')
print('Model saved')

meta['model_name'] = type(pipeline.named_steps['rf']).__name__
meta['f1_score'] = f1
meta['labels'] = cust_map

with open('meta.json', 'w') as fp:
    json.dump(meta, fp)

print('Saved metadata')
print('Goodbye')
