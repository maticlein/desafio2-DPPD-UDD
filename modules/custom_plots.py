import plotly.graph_objects as go

def progress_plot(value, title):
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = value,
    number = { "suffix": "%" },
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': title},
    gauge = {
        'axis': {'range': [0, 100], "tickmode": "auto", "nticks": 10, 'tickcolor': "darkblue"},
        'bar': {'color': "#1B5FAA"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 30], 'color': '#d93452'},
            {'range': [31, 60], 'color': '#fa6f4e'},
            {'range': [61, 90], 'color': '#fbc409'},
            {'range': [91, 100], 'color': '#34c077'}
            ]
        }))
    return fig