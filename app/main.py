import requests

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# >>> import plotly.express as px
# >>> fig = px.box(range(10))
# >>> fig.write_html('test.html')

df = pd.DataFrame({
    'col1': [1,2,3,4],
    'col2': [10*i for i in range(1,5)]
})

# Title
st.title('Predicting Customer Value from Previous Session')
HtmlFile = open("vis.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
print(source_code)
components.html(source_code, height=1000)

st.sidebar.title("Previous Session Statistics")
x1 = st.sidebar.text_input("time on site (mins)", 4.8)
x2 = st.sidebar.text_input("time in checkout (mins)", 8.3)
x3 = st.sidebar.text_input("time on sales page (mins)", 3.35)

predict_vars = st.sidebar.button("predict")

def map_pred(pred_idx):
    preds = ['budget buyer', 'value buyer', 'high value buyer', 'loyal buyer']
    return preds[pred_idx]

def normalize(inputs):
    return [{"x1": x1, "x2": x2, "x3": x3}]


if predict_vars:
    print('Regenerating predictions')
    model_inputs = [x1, x2, x3]
    
    try:
        model_inputs = [int(i) for i in model_inputs]
    except ValueError:
        st.error('Model inputs must be an integer')
        model_inputs = None
    
    if model_inputs is not None:
        data = normalize(model_inputs)
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            res = requests.post("http://localhost:8001/predict", 
                json=data,
                headers=header
            )
            prediction = res.json()['prediction'][0]
            st.write(f"This customer is likely a {map_pred(prediction)}")

        except KeyError:
            st.error('Unable to make prediction due to invalid inputs')
        except ConnectionError:
            st.error('Unable to connect to API right now, please contact administrator')

