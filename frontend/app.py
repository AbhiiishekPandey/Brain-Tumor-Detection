import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference import get_engine
from src.report_generator import generate_pdf_report

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-for-brain-tumor-detection')

# Configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
GRADCAM_FOLDER = os.path.join('static', 'gradcam')
REPORTS_FOLDER = os.path.join('static', 'reports')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GRADCAM_FOLDER'] = GRADCAM_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure folders exist
for folder in [UPLOAD_FOLDER, GRADCAM_FOLDER, REPORTS_FOLDER]:
    os.makedirs(os.path.join(app.root_path, folder), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        logger.warning("Analyze request with no file part")
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        logger.warning("Analyze request with empty filename")
        return redirect(url_for('home'))

    if file and allowed_file(file.filename):
        try:
            # Save original image with secure filename
            filename = secure_filename(file.filename)
            base_filename = os.path.splitext(filename)[0]
            filepath = os.path.join(app.root_path, UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            logger.info(f"Analyzing file: {filename}")

            # Run AI Analysis
            engine = get_engine()
            result = engine.predict(filepath, os.path.join(app.root_path, GRADCAM_FOLDER))

            # Save result metadata for report generation
            metadata_path = os.path.join(app.root_path, REPORTS_FOLDER, f"{base_filename}_meta.json")
            with open(metadata_path, 'w') as f:
                json.dump({
                    "result": result,
                    "original_path": filepath,
                    "heatmap_path": result['heatmap_path'],
                    "filename": filename
                }, f)

            # Convert absolute heatmap path to relative for URL
            heatmap_filename = os.path.basename(result['heatmap_path'])
            heatmap_url = url_for('static', filename=f'gradcam/{heatmap_filename}')
            original_url = url_for('static', filename=f'uploads/{filename}')

            return render_template('result.html',
                                image_path=original_url,
                                heatmap_path=heatmap_url,
                                result=result,
                                report_id=base_filename)
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return render_template('index.html', error="An error occurred during AI analysis. Please try again.")
    else:
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        return render_template('index.html', error="Invalid file type. Please upload a valid MRI image (PNG, JPG, or WEBP).")

@app.route('/download_report/<report_id>')
def download_report(report_id):
    try:
        # Prevent path traversal
        report_id = secure_filename(report_id)
        metadata_path = os.path.join(app.root_path, REPORTS_FOLDER, f"{report_id}_meta.json")
        
        if not os.path.exists(metadata_path):
            logger.warning(f"Report metadata missing for ID: {report_id}")
            return "Report not found", 404

        with open(metadata_path, 'r') as f:
            data = json.load(f)

        pdf_filename = f"{report_id}_diagnostic_report.pdf"
        pdf_path = os.path.join(app.root_path, REPORTS_FOLDER, pdf_filename)
        
        # Generate PDF on the fly or check if exists
        if not os.path.exists(pdf_path):
            generate_pdf_report(data['result'], data['original_path'], data['heatmap_path'], pdf_path)

        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error generating/downloading report: {str(e)}")
        return "Internal error during report generation", 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="404 - Page Not Found"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('index.html', error="500 - Internal Server Error"), 500

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
    app.run(debug=debug_mode, port=5000)
