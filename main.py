from flask import Flask, request, jsonify
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import os
from json import loads

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'

model = YOLO("./best.pt")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_image', methods=['POST'])
def process_image():

    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            results = model.predict(image_path, conf=0.5, iou=0.1, max_det=5)
            results = loads(results[0].tojson())
            sorted_results = sorted(
                [
                    (result["name"], result["box"], result["confidence"])
                    for result in results
                ],
                key=lambda x: x[1]["x1"]
            )

            boxes = [
                (
                    result[1]["x1"],
                    result[1]["x2"],
                    result[1]["y1"],
                    result[1]["y2"]
                ) for result in sorted_results
            ]

            return jsonify({'results': sorted_results})

        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({'error': 'Error processing image'}), 500

    else:
        return jsonify({'error': 'Unsupported file format'}), 415

if __name__ == '__main__':
    app.run(debug=True)
