import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from churn_model import predict_churn


# ========== LOAD DATA (ONCE AT STARTUP) ==========
print("Loading data...")
dua_df = pd.read_csv("data/advanced_dua.csv")
ret_df = pd.read_csv("data/advanced_retention.csv")
mobile_df = pd.read_csv("data/mobile_analytics.csv")

dua_df['date'] = pd.to_datetime(dua_df['date'])
mobile_df['date'] = pd.to_datetime(mobile_df['date'])
ret_df['first_date'] = pd.to_datetime(ret_df['first_date'])

# Derive metrics once
dua_df['sessions_per_user'] = dua_df['total_sessions'] / dua_df['dau']
dua_df['dau_growth'] = dua_df['dau'].pct_change() * 100

print("Data loaded successfully!")

# ========== PRECOMPUTE METRICS ==========
total_dau = dua_df['dau'].mean()
avg_session = dua_df['avg_session_duration'].mean()
avg_retention = ret_df['retention_rate'].mean()
total_opens = mobile_df['app_opens'].sum()
avg_screens = dua_df['avg_screens_per_session'].mean()

# ========== SAMPLE DATA FOR LARGE DATASETS ==========
# If mobile_df is very large, sample it for better performance
if len(mobile_df) > 10000:
    mobile_df_display = mobile_df.sample(n=10000, random_state=42)
    print(f"Sampled mobile data from {len(mobile_df)} to {len(mobile_df_display)} rows for display")
else:
    mobile_df_display = mobile_df

# ========== KPI CARDS ==========
def create_kpi_card(title, value, color):
    return html.Div(
        style={
            'backgroundColor': color,
            'borderRadius': '15px',
            'padding': '15px',
            'width': '18%',
            'minWidth': '150px',
            'color': 'white',
            'textAlign': 'center',
            'boxShadow': '2px 2px 8px rgba(0,0,0,0.2)'
        },
        children=[
            html.H4(title, style={'fontSize': '16px', 'margin': '5px 0'}),
            html.H2(value, style={'fontSize': '24px', 'margin': '5px 0'})
        ]
    )

kpi_cards = [
    create_kpi_card('👥 Avg Daily Active Users', f'{total_dau:,.0f}', '#3498db'),
    create_kpi_card('⏱️ Avg Session Duration', f'{avg_session:.1f} min', '#2ecc71'),
    create_kpi_card('🔄 Retention Rate', f'{avg_retention:.1f}%', '#e74c3c'),
    create_kpi_card('📱 Total App Opens', f'{total_opens:,.0f}', '#f39c12'),
    create_kpi_card('📊 Avg Screens/Session', f'{avg_screens:.1f}', '#9b59b6')
]

# ========== INITIALIZE APP ==========
app = Dash(__name__)
app.config.suppress_callback_exceptions = True

# ========== APP LAYOUT ==========
app.layout = html.Div([
    html.H1(" Mobile App Analytics Dashboard", style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50'}),
    
    # KPI Cards
    html.Div(kpi_cards, style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '30px 0', 'flexWrap': 'wrap', 'gap': '10px'}),
    
    # ========== EXECUTIVE SUMMARY SECTION ==========
    html.Div([
        html.H2("📊 Executive Summary", style={
            'textAlign': 'center', 
            'color': '#2c3e50', 
            'marginTop': '40px',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div([
                html.H4("Key Insights", style={'color': '#2980b9', 'marginBottom': '15px'}),
                html.Ul([
                    html.Li(f"Daily active users averaged {total_dau:,.0f} with an average session duration of {avg_session:.1f} minutes"),
                    html.Li(f"User retention rate stands at {avg_retention:.1f}%, indicating {'strong' if avg_retention > 40 else 'moderate' if avg_retention > 25 else 'weak'} user engagement"),
                    html.Li(f"Users view an average of {avg_screens:.1f} screens per session"),
                    html.Li(f"Total app opens reached {total_opens:,.0f} across the analysis period")
                ], style={'lineHeight': '1.8', 'fontSize': '15px'})
            ], style={
                'backgroundColor': '#e8f4f8',
                'padding': '20px',
                'borderRadius': '10px',
                'width': '48%',
                'minWidth': '300px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
            }),
            
            html.Div([
                html.H4("Recommendations", style={'color': '#27ae60', 'marginBottom': '15px'}),
                html.Ul([
                    html.Li("Focus retention efforts on high-churn segments identified in predictions"),
                    html.Li("Optimize onboarding flow to increase early engagement"),
                    html.Li("Implement personalized push notifications for at-risk users"),
                    html.Li("A/B test features to improve session duration and screen views")
                ], style={'lineHeight': '1.8', 'fontSize': '15px'})
            ], style={
                'backgroundColor': '#e8f8f5',
                'padding': '20px',
                'borderRadius': '10px',
                'width': '48%',
                'minWidth': '300px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'gap': '20px',
            'marginBottom': '40px',
            'flexWrap': 'wrap'
        })
    ], style={'marginTop': '30px'}),
    
    # ========== REFRESH BUTTON ==========
    html.Div([
        html.Button(" Refresh Data", id='refresh-btn',
                    style={
                        'margin': '10px auto',
                        'display': 'block',
                        'padding': '12px 30px',
                        'fontSize': '16px',
                        'backgroundColor': '#2980b9',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '8px',
                        'cursor': 'pointer',
                        'boxShadow': '0 2px 5px rgba(0,0,0,0.2)',
                        'transition': 'background-color 0.3s'
                    }),
        dcc.ConfirmDialog(id='refresh-dialog', message=' Data refreshed successfully!')
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),    
    # Store to track what's been loaded
    dcc.Store(id='growth-loaded', data=False),
    dcc.Store(id='retention-loaded', data=False),
    dcc.Store(id='user-loaded', data=False),
    
    # Collapsible sections
    html.Div([
        dcc.Loading(
            id="loading-growth",
            type="circle",
            children=[
                html.Button(" Toggle Growth & Engagement Charts", id='btn-growth', n_clicks=0, 
                           style={'margin': '10px', 'padding': '12px 24px', 'fontSize': '16px', 'cursor': 'pointer', 
                                  'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}),
                html.Div(id='growth-section', style={'display': 'none'})
            ]
        ),
        #Retention section
        dcc.Loading(
            id="loading-retention",
            type="circle",
             children=[
                html.Button(" Toggle Retention Analytics", id='btn-retention', n_clicks=0,
                           style={
                               'margin': '10px', 
                               'padding': '12px 24px', 
                               'fontSize': '16px', 
                               'cursor': 'pointer',
                               'backgroundColor': '#e74c3c', 
                               'color': 'white', 
                               'border': 'none', 
                               'borderRadius': '5px',
                               'boxShadow': '0 2px 5px rgba(0,0,0,0.15)'
                           }),
                html.Div(id='retention-section', style={'display': 'none'})
            ]
        ),

        #User behavior section
        dcc.Loading(
            id="loading-user",
            type="circle",
            children=[
                html.Button(" Toggle User Behavior & Funnel", id='btn-user', n_clicks=0,
                           style={
                               'margin': '10px', 
                               'padding': '12px 24px', 
                               'fontSize': '16px', 
                               'cursor': 'pointer',
                               'backgroundColor': '#9b59b6', 
                               'color': 'white', 
                               'border': 'none', 
                               'borderRadius': '5px',
                               'boxShadow': '0 2px 5px rgba(0,0,0,0.15)'
                           }),
                html.Div(id='user-section', style={'display': 'none'})
            ]
        ),

        # Churn Prediction Section
        dcc.Loading(
            id="loading-churn",
            type="circle",
            children=[
                html.Button(" Toggle Churn Prediction Results", id='btn-churn', n_clicks=0,
                           style={'margin': '10px', 'padding': '12px 24px', 'fontSize': '16px', 'cursor': 'pointer',
                                  'backgroundColor': '#16a085', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.15)'}),
                html.Div(id='churn-section', style={'display': 'none'})
            ]
        ),
    ])
], style={'padding': '20px', 'maxWidth': '1400px', 'margin': '0 auto'})

# ========== OPTIMIZED CALLBACKS WITH LAZY LOADING ==========
# Growth & Engagement Callback
@app.callback(
    Output('growth-section', 'children'),
    Output('growth-section', 'style'),
    Output('growth-loaded', 'data'),
    Input('btn-growth', 'n_clicks'),
    State('growth-loaded', 'data'),
    prevent_initial_call=True
)
def toggle_growth(n_clicks, loaded):
    if n_clicks % 2 == 1:  # Show
        if not loaded:  # Generate only once
            print("Generating growth charts...")
            charts = [
                dcc.Graph(figure=px.line(dua_df, x='date', y='dau', title='Daily Active Users').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(dua_df, x='date', y='total_sessions', title='Total Sessions').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(dua_df, x='date', y='avg_session_duration', title='Avg Session Duration').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.bar(dua_df, x='date', y='total_screens_viewed', title='Total Screens Viewed').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(dua_df, x='date', y='avg_screens_per_session', title='Avg Screens per Session').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(dua_df, x='date', y='sessions_per_user', title='Sessions per User').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(dua_df, x='date', y='dau_growth', title='DAU Growth Rate (%)').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40)))
            ]
            return charts, {'display': 'block', 'marginTop': '20px'}, True
        return dash.no_update, {'display': 'block', 'marginTop': '20px'}, True
    else:  # Hide
        return dash.no_update, {'display': 'none'}, loaded

# Retention Analytics Callback
@app.callback(
    Output('retention-section', 'children'),
    Output('retention-section', 'style'),
    Output('retention-loaded', 'data'),
    Input('btn-retention', 'n_clicks'),
    State('retention-loaded', 'data'),
    prevent_initial_call=True
)
def toggle_retention(n_clicks, loaded):
    if n_clicks % 2 == 1:  # Show
        if not loaded:  # Generate only once
            print("Generating retention charts...")
            charts = [
                dcc.Graph(figure=px.line(ret_df, x='first_date', y='retention_rate', title='Retention Rate').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(ret_df, x='first_date', y='churn_rate', title='Churn Rate').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.line(ret_df, x='first_date', y='churn_rate_smooth', title='Smoothed Churn Rate').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40)))
            ]
            return charts, {'display': 'block', 'marginTop': '20px'}, True
        return dash.no_update, {'display': 'block', 'marginTop': '20px'}, True
    else:  # Hide
        return dash.no_update, {'display': 'none'}, loaded

# User Behavior Callback
@app.callback(
    Output('user-section', 'children'),
    Output('user-section', 'style'),
    Output('user-loaded', 'data'),
    Input('btn-user', 'n_clicks'),
    State('user-loaded', 'data'),
    prevent_initial_call=True
)
def toggle_user(n_clicks, loaded):
    if n_clicks % 2 == 1:  # Show
        if not loaded:  # Generate only once
            print("Generating user behavior charts...")
            
            # Aggregate data for funnel to avoid large datasets
            funnel_df = pd.DataFrame({
                'stage': ['App Opens', 'Screens Viewed', 'Session Minutes'],
                'value': [
                    mobile_df['app_opens'].sum(),
                    mobile_df['screens_viewed'].sum(),
                    mobile_df['session_duration'].sum()
                ]
            })
            
            # Use aggregated data for bar charts
            segment_screens = mobile_df.groupby('user_segment')['screens_viewed'].mean().reset_index()
            segment_duration = mobile_df.groupby('user_segment')['session_duration'].mean().reset_index()
            
            charts = [
                dcc.Graph(figure=px.histogram(mobile_df_display, x='session_duration', nbins=30, title='Session Duration Distribution').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.box(mobile_df_display, x='device_type', y='session_duration', title='Session Duration by Device').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.box(mobile_df_display, x='user_acquisition_channel', y='session_duration', title='Session Duration by Channel').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.bar(segment_screens, x='user_segment', y='screens_viewed', title='Avg Screens per Segment').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.bar(segment_duration, x='user_segment', y='session_duration', title='Avg Session Duration per Segment').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40))),
                dcc.Graph(figure=px.funnel(funnel_df, x='value', y='stage', title='User Engagement Funnel').update_layout(height=350, template='plotly_white', margin=dict(l=40, r=40, t=40, b=40)))
            ]
            return charts, {'display': 'block', 'marginTop': '20px'}, True
        return dash.no_update, {'display': 'block', 'marginTop': '20px'}, True
    else:  # Hide
        return dash.no_update, {'display': 'none'}, loaded

# Churn Prediction Callback
@app.callback(
    Output('churn-section', 'children'),
    Output('churn-section', 'style'),
    Input('btn-churn', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_churn(n_clicks):
    if n_clicks % 2 == 1:
        print("Generating churn prediction results...")

        
        try:
            # Use mobile_df which has all required columns
            predictions = predict_churn(mobile_df)
            
            # Convert user_id to same type before merging
            predictions['user_id'] = predictions['user_id'].astype(str)
            mobile_df_temp = mobile_df.copy()
            mobile_df_temp['user_id'] = mobile_df_temp['user_id'].astype(str)

            # Add user_segment back for analysis
            predictions = predictions.merge(
                mobile_df[['user_id', 'user_segment']].drop_duplicates(),
                on='user_id',
                how='left'
            )
            
            # Create visualizations
            fig1 = px.histogram(predictions, x='churn_probability', nbins=30, 
                               title=' Predicted Churn Probability Distribution',
                               labels={'churn_probability': 'Churn Probability'})
            fig1.update_layout(height=400, template='plotly_white', 
                              margin=dict(l=40, r=40, t=60, b=40))

            fig2 = px.bar(predictions.groupby('user_segment')['churn_prediction'].mean().reset_index(),
                          x='user_segment', y='churn_prediction',
                          title=' Average Churn Rate by User Segment',
                          labels={'churn_prediction': 'Avg Churn Rate', 'user_segment': 'User Segment'})
            fig2.update_layout(height=400, template='plotly_white',
                              margin=dict(l=40, r=40, t=60, b=40))
            
            # High-risk users
            high_risk = predictions[predictions['churn_probability'] > 0.7]
            high_risk_count = len(high_risk)
            
            # Summary metrics
            avg_churn_prob = predictions['churn_probability'].mean()
            predicted_churners = predictions['churn_prediction'].sum()
            
            summary_card = html.Div([
                html.H3("🚨 Churn Prediction Summary", style={'color': '#e74c3c', 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.H4(f"{avg_churn_prob:.1%}", style={'color': '#e74c3c', 'margin': '5px'}),
                        html.P("Avg Churn Probability", style={'fontSize': '14px'})
                    ], style={
                        'textAlign': 'center', 
                        'padding': '15px', 
                        'backgroundColor': '#f8f9fa', 
                        'borderRadius': '10px', 
                        'margin': '10px',
                        'flex': '1',
                        'minWidth': '150px'
                    }),
                    html.Div([
                        html.H4(f"{predicted_churners:,.0f}", style={'color': '#e67e22', 'margin': '5px'}),
                        html.P("Predicted Churners", style={'fontSize': '14px'})
                    ], style={
                        'textAlign': 'center', 
                        'padding': '15px', 
                        'backgroundColor': '#f8f9fa', 
                        'borderRadius': '10px', 
                        'margin': '10px',
                        'flex': '1',
                        'minWidth': '150px'
                    }),
                    html.Div([
                        html.H4(f"{high_risk_count:,.0f}", style={'color': '#c0392b', 'margin': '5px'}),
                        html.P("High-Risk Users (>70%)", style={'fontSize': '14px'})
                    ], style={
                        'textAlign': 'center', 
                        'padding': '15px', 
                        'backgroundColor': '#f8f9fa', 
                        'borderRadius': '10px', 
                        'margin': '10px',
                        'flex': '1',
                        'minWidth': '150px'
                    }),
                ], style={
                    'display': 'flex', 
                    'justifyContent': 'space-around', 
                    'marginTop': '20px', 
                    'flexWrap': 'wrap'
                })
            ], style={
                'backgroundColor': '#ecf0f1', 
                'padding': '20px', 
                'borderRadius': '15px', 
                'marginBottom': '30px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
            })

            return [summary_card, dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)], {'display': 'block', 'marginTop': '20px'}
        
        except Exception as e:
            error_msg = html.Div([
                html.H3(" Error in Churn Prediction", style={'color': '#e74c3c'}),
                html.P(f"Error: {str(e)}", style={'color': '#555', 'fontSize': '14px'}),
                html.P("Please ensure your data has the required columns for churn prediction.", 
                      style={'color': '#777', 'fontSize': '13px', 'marginTop': '10px'})
            ], style={
                'backgroundColor': '#ffe6e6', 
                'padding': '20px', 
                'borderRadius': '10px',
                'margin': '20px 0'
            })
            return [error_msg], {'display': 'block', 'marginTop': '20px'}
    else:
        return dash.no_update, {'display': 'none'}

# Refresh Data Callback
@app.callback(
    Output('refresh-dialog', 'displayed'),
    Input('refresh-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_data(n_clicks):
    global dua_df, ret_df, mobile_df, total_dau, avg_session, avg_retention, total_opens, avg_screens
    
    print(" Refreshing data...")
    # Reload data
    dua_df = pd.read_csv("data/advanced_dua.csv")
    ret_df = pd.read_csv("data/advanced_retention.csv")
    mobile_df = pd.read_csv("data/mobile_analytics.csv")
    
    # Reprocess dates
    dua_df['date'] = pd.to_datetime(dua_df['date'])
    mobile_df['date'] = pd.to_datetime(mobile_df['date'])
    ret_df['first_date'] = pd.to_datetime(ret_df['first_date'])
    
    # Recalculate metrics
    total_dau = dua_df['dau'].mean()
    avg_session = dua_df['avg_session_duration'].mean()
    avg_retention = ret_df['retention_rate'].mean()
    total_opens = mobile_df['app_opens'].sum()
    avg_screens = dua_df['avg_screens_per_session'].mean()
    
    dua_df['sessions_per_user'] = dua_df['total_sessions'] / dua_df['dau']
    dua_df['dau_growth'] = dua_df['dau'].pct_change() * 100
    
    print(" Data refresh complete!")
    return True

# ========== RUN APP ==========
if __name__ == '__main__':
    print("Starting dashboard server...")
    app.run(debug=True)
