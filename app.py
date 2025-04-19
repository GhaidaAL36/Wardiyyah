from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template
import io
import json


app = Flask(__name__)
CORS(app)
model = load_model("flower_model.h5")

#read the class name from the txt
with open("flower_class_labels.txt", "r", encoding="utf-8") as f:
    class_labels = [line.strip() for line in f.readlines()]

#read from JSON
with open("flower_info.json", "r", encoding="utf-8") as f:
    flower_info = json.load(f)

@app.route('/app', methods=['POST'])
#read data img
def predict_flower():
    if 'file' not in request.files:
        return jsonify({'error': 'لم يتم تحميل صورة'}), 400


    file = request.files['file']
    img_bytes = file.read()

    try:
        img = image.load_img(io.BytesIO(img_bytes), target_size=(224, 224))
    except Exception:
        return jsonify({'error': 'فشل في معالجة الصورة. تأكد أنها صورة صالحة.'}), 400

    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    class_id = class_labels[predicted_index]
    flower_data = flower_info.get(class_id, None)

    confidence_percent = round(confidence * 100, 2)

    flower_name = flower_data.get("name_ar") if flower_data else None
    flower_nameEN = flower_data.get("name_en") if flower_data else None
    description = flower_data.get("description") if flower_data else None

    if confidence_percent < 50 or flower_data is None:
        return jsonify({
            'label': class_id,
            'flower': "زهرة غير معروفة",
            'description': "لم أتمكن من التعرف على هذه الزهرة بدقة، الرجاء تجربة صورة أخرى",
            'confidence': confidence_percent
        })

    elif confidence_percent < 85:
        return jsonify({
            'label': class_id,
            'flower': flower_data.get("name_ar", "زهرة غير معروفة") + " (⚠️ الدقة منخفضة)",
            'flower_en': flower_nameEN,
            'description': flower_data.get("description", "— لا يوجد وصف متاح حالياً —"),
            'confidence': confidence_percent
        })

    return jsonify({
        'label': class_id,
        'flower': flower_data.get("name_ar", "زهرة غير معروفة"),
        'flower_en': flower_nameEN,
        'description': flower_data.get("description", "— لا يوجد وصف متاح حالياً —"),
        'confidence': confidence_percent
    })

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

