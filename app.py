import os
from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_handler():
    try:
        bucket_name = os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            print("ERROR: GCS_BUCKET_NAME environment variable not set.")
            return jsonify({"error": "Server configuration error"}), 500

        file_name = request.args.get("filename")
        if not file_name:
            return jsonify({"error": "Missing 'filename' query parameter"}), 400
        
        # This is where the connection to GCS happens
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        blob.upload_from_string(
            request.data,
            content_type=request.content_type
        )
        
        print(f"Successfully uploaded {file_name} to gs://{bucket_name}")
        return jsonify({
            "message": f"File '{file_name}' uploaded successfully.",
        }), 200

    except Exception as e:
        # This will print the *actual* error from Google Cloud to your terminal
        print(f"ERROR during upload: {e}")
        return jsonify({"error": "Failed to connect to cloud storage"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)