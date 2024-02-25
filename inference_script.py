import json
from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from codecarbon import EmissionsTracker
import boto3
from botocore.exceptions import NoCredentialsError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = Flask(__name__)

# Load your model and tokenizer here
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

def upload_to_s3(bucket_name, file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except NoCredentialsError:
        print("Credentials not available")

@app.route('/invocations', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data.get("inputs", "")
        parameters_list = data.get("parameters_list", None)

        # Initialize and start CodeCarbon EmissionsTracker
        logging.info("Performing model prediction")
        tracker = EmissionsTracker(output_dir="/emissions_data")  # Specify the output directory
        tracker.start()

        # Parameters may or may not be passed
        input_ids = tokenizer(
            text, truncation=True, padding="longest", return_tensors="pt"
        ).input_ids.to(device)

        predictions = []
        if parameters_list:
            for parameters in parameters_list:
                output = model.generate(input_ids, **parameters)
                predictions.append(tokenizer.batch_decode(output, skip_special_tokens=True))
        else:
            output = model.generate(input_ids)
            predictions = tokenizer.batch_decode(output, skip_special_tokens=True)

        # Stop the tracker and upload the emissions data to S3
        tracker.stop()
        emissions_data_path = "/emissions_data/emissions.csv"
        try:
            with open(emissions_data_path, "r") as file:
                # Example: Read the last line and parse it to get the emissions value
                # This is a simplification; you'll need to adjust based on the actual CSV format
                last_line = list(file)[-1]
                emissions = last_line.split(",")[4]  # Adjust 'some_index' based on the CSV structure
        except Exception as e:
            emissions = f"Error reading emissions data: {str(e)}"
        

        upload_to_s3("my-emissions-bucket", "/emissions_data/emissions.csv")
        response_data = {"english2german": predictions, "emissions": emissions}
        return jsonify(response_data)

        

    except Exception as e:
        return jsonify({"error": str(e)}), 500
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


