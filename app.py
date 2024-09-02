from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_file():
    file = request.files.get('file')
    format = request.form.get('format')

    if not file or not format:
        return jsonify({'message': 'File or format missing'}), 400

    input_ext = file.filename.split('.')[-1]
    input_path = os.path.join('C:/tmp', f'input.{input_ext}')
    output_path = os.path.join('C:/tmp', f'output.{format}')

    # Create temporary directory if it does not exist
    if not os.path.exists('C:/tmp'):
        os.makedirs('C:/tmp')

    file.save(input_path)

    try:
        # Call Calibre's ebook-convert command
        result = subprocess.run(
            ['ebook-convert', input_path, output_path],
            capture_output=True,
            text=True
        )

        # Check for errors in the conversion process
        if result.returncode != 0:
            return jsonify({'message': 'Conversion failed', 'error': result.stderr}), 500

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({'message': 'Conversion failed', 'error': str(e)}), 500

    finally:
        # Clean up input file
        if os.path.exists(input_path):
            os.remove(input_path)
        # Optionally, clean up output file after sending it to the user
        # if os.path.exists(output_path):
        #     os.remove(output_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
