from flask import Flask, render_template, request, send_from_directory
import os
import uuid
from realesrgan_ncnn_py import Realesrgan
from PIL import Image

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)



realesrgan = Realesrgan(gpuid=-1, model=0)


def enhance_image(img_path, outpath):
    with Image.open(img_path) as image:
        image = realesrgan.process_pil(image)
        image.save(f"{outpath}", quality=100)

    return outpath


@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>AI Image Enhancer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
                text-align: center;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 8px;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input[type="file"] {
                margin-bottom: 15px;
            }
            button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            #download {
                margin-top: 20px;
                display: none;
            }
            img {
                margin-top: 20px;
                max-width: 100%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AI Image Enhancer</h2>
            <form id="uploadForm">
                <input type="file" name="image" id="image" required><br>
                <button type="submit">Enhance</button>
            </form>
            <div id="result">
                <img id="outputImage" />
                <br>
                <a id="download" href="#" download>Download Enhanced Image</a>
            </div>
        </div>

        <script>
            document.getElementById("uploadForm").onsubmit = async function (e) {
                e.preventDefault();
                const formData = new FormData();
                const fileInput = document.getElementById("image");
                formData.append("image", fileInput.files[0]);

                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData,
                });
                const data = await response.json();
                const imageUrl = "/" + data.url;

                document.getElementById("outputImage").src = imageUrl;
                const downloadLink = document.getElementById("download");
                downloadLink.href = imageUrl;
                downloadLink.style.display = "inline-block";
            };
        </script>
    </body>
    </html>
    """




@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    uid = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{uid}.png")
    output_path = os.path.join(OUTPUT_FOLDER, f"{uid}.png")
    image.save(input_path)

    enhance_image(input_path, output_path)
    if os.path.exists(input_path):
        os.remove(input_path)
    return {'url': f'/output/{uid}.png'}

@app.route('/output/<filename>')
def output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run()
