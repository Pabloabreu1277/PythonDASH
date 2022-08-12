# Dropdown para colocar no layout
dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),



# call back
@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'