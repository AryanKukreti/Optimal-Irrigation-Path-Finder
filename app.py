from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64
from utils.graph_utils import generate_graph
from utils.plot_utils import plot_results

app = Flask(__name__)

# Global variables to store the uploaded image and its data
image_array = None
points = None
starting_point = None

@app.route('/')
def index():
    return render_template('index.html')  # Main page that loads first

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload():
    global image_array, points, starting_point
    file = request.files.get('file')  # Use .get() to avoid KeyError

    if file:
        image = Image.open(file).convert("L")
        image_array = np.array(image)

        # Initialize points
        ditch_threshold = 60
        points = []
        while len(points) < 200:
            x = np.random.randint(0, image_array.shape[1])
            y = np.random.randint(0, image_array.shape[0])
            if image_array[y, x] > ditch_threshold:
                points.append([x, y])
        points = np.array(points)
        
        # Set initial starting point (center of the image)
        starting_point = [image_array.shape[1] // 2, image_array.shape[0] // 2]

        return jsonify({'message': 'Image uploaded successfully', 'starting_point': starting_point})
    else:
        return jsonify({'error': 'No file uploaded.'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    global starting_point, image_array, points
    if image_array is None:
        return jsonify({'error': "No image uploaded."})

    starting_point_x = int(request.form['starting_point_x'])
    starting_point_y = int(request.form['starting_point_y'])
    starting_point = [starting_point_x, starting_point_y]
    ditch_threshold = 60

    if image_array[starting_point_y, starting_point_x] < ditch_threshold:
        return jsonify({'error': "Invalid starting point. It's over a ditch."})

    # Generate the graph
    tri, G = generate_graph(points, image_array, ditch_threshold)
    
    # Plotting the results
    plot_results(tri, G, image_array, starting_point, points)

    # Save the plot as an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_url = base64.b64encode(buffer.getvalue()).decode('ascii')
    plt.close()  # Close the plot to avoid displaying it

    return jsonify({'plot_url': plot_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Update to listen on all interfaces
