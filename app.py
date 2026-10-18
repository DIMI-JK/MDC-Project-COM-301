from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from pathlib import Path
import asyncio
import pandas as pd
import subprocess
import sys

from scrape import Url, scrape_reviews

# Resolve paths relative to this app.py file
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Initialize Flask only once
app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR)
)

CORS(app)

OUTPUT_FILE = BASE_DIR / "review_predictions.csv"
PREDICTION_SCRIPT = BASE_DIR / "predict.py"

@app.route("/")
def home():
    print("App location:", BASE_DIR)
    print("Template directory:", TEMPLATE_DIR)
    print("Template exists:", (TEMPLATE_DIR / "index.html").is_file())
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True) or {}
    product_url = data.get('url')

    if not product_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Step 1: Scrape product reviews
        formatted_url = Url(product_url)
        asyncio.run(scrape_reviews(formatted_url))

        # Step 2: Run the existing prediction script
        subprocess.run(
            [sys.executable, str(PREDICTION_SCRIPT)],
            check=True,
            cwd=str(BASE_DIR)
        )

        # Step 3: Read prediction results
        if not OUTPUT_FILE.exists():
            return jsonify({
                'error': 'Prediction output CSV was not found.'
            }), 500

        df = pd.read_csv(OUTPUT_FILE)

        if 'prediction' not in df.columns:
            return jsonify({
                'error': 'Prediction column is missing from CSV.'
            }), 500

        counts = df['prediction'].value_counts().to_dict()

        genuine_count = int(counts.get('OR (Genuine)', 0))
        fake_count = int(counts.get('CG (Fake)', 0))
        skipped_count = int(counts.get('Not evaluated', 0))
        evaluated_count = genuine_count + fake_count

        reviews_list = df.fillna("").to_dict(orient='records')

        return jsonify({
            'status': 'success',
            'url': str(formatted_url),
            'total_reviews': len(df),
            'summary': {
                'evaluated': evaluated_count,
                'genuine': genuine_count,
                'fake': fake_count,
                'skipped': skipped_count
            },
            'reviews': reviews_list
        })

    except Exception as e:
        app.logger.exception("Review analysis failed")
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['GET'])
def download_csv():
    if not OUTPUT_FILE.exists():
        return jsonify({
            'error': 'No prediction CSV available. Analyze a product first.'
        }), 404

    return send_file(
        OUTPUT_FILE,
        as_attachment=True,
        download_name='review_predictions.csv',
        mimetype='text/csv'
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)
