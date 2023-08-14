import plotly.graph_objects as go

def progress_plot(value, title, min, max):
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = value,
    number = { "suffix": "%" },
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': title},
    gauge = {
        'axis': {'range': [min, max], "tickmode": "auto", "nticks": 10, 'tickcolor': "darkblue"},
        'bar': {'color': "#1B5FAA"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray"
        }))
    return fig