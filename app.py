# Import necessary libraries
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import jsonify
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app

# Function to generate 3D plot with cylinder and points from CSV
def generate_plot(data_file, radius, length):
    # Read data from CSV
    df = pd.read_csv(data_file)

    # Create Plotly 3D Scatter plot for points from CSV
    plot_data = go.Scatter3d(
        x=df['x'],
        y=df['y'],
        z=df['z'],
        mode='markers',
        marker=dict(
            size=5,
            color='green',
            opacity=0.9
        )
    )

    # Create cylinder surface
    cylinder_theta = np.linspace(0, 2 * np.pi, 100)
    cylinder_y = radius * np.cos(cylinder_theta)  # Rotate along y-axis for horizontal orientation
    cylinder_z = radius * np.sin(cylinder_theta)  # Rotate along z-axis for horizontal orientation
    cylinder_x = np.linspace(-length/2, length/2, 100)

    # Create the surface of the cylinder
    cylinder_surface = go.Surface(
        x=np.outer(cylinder_x, np.ones_like(cylinder_theta)),
        y=np.outer(np.ones_like(cylinder_x), cylinder_y),
        z=np.outer(np.ones_like(cylinder_x), cylinder_z),
        opacity=0.5,
        colorscale='Blues'
    )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(range=[-length/2 - 4, length/2 + 4]),
            yaxis=dict(range=[-radius - 4, radius + 4]),
            zaxis=dict(range=[-radius - 4, radius + 4]),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1)
        ),
        height=800  # Adjust the height of the plot here
    )

    # Create a Plotly figure including both scatter plot and cylinder surface
    fig = go.Figure(data=[plot_data, cylinder_surface], layout=layout)

    # Convert Plotly figure to HTML div
    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Also return data as JSON for API endpoint
    x_data = df['x'].tolist()
    y_data = df['y'].tolist()
    z_data = df['z'].tolist()

    return plot_div, jsonify({'x': x_data, 'y': y_data, 'z': z_data})

@app.route('/')
def index():
    data_file = 'data.csv'  # Path to your CSV file
    radius = 21  # Customize the radius of the cylinder
    length = 40  # Customize the length of the cylinder
    plot_div = generate_plot(data_file, radius, length)
    return render_template('index.html', plot_div=plot_div)

@app.route('/api/data')
def get_plot_data_api():
    data_file = 'data.csv'  # Path to your CSV file
    radius = 21  # Customize the radius of the cylinder
    length = 40  # Customize the length of the cylinder
    
    plot_div, plot_data_json = generate_plot(data_file, radius, length)

    return plot_data_json

    # Generate plot data
    df = pd.read_csv(data_file)
    x_data = df['x'].tolist()
    y_data = df['y'].tolist()
    z_data = df['z'].tolist()

    return jsonify({'x': x_data, 'y': y_data, 'z': z_data})

if __name__ == '__main__':
    app.run(debug=True)
