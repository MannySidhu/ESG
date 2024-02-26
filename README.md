This application translates text from English to German and estimates the energy consumed during the translation process. It incorporates a Code Carbon tracker that measures emissions throughout the inference job (from start to finish).
Functionality: English-to-German translation with energy consumption estimation.
 Technical details:
     Inference job runs on a Flask webserver using an AI model from Hugging Face.
     Model containerized in a Docker instance on an EC2 T5-Small instance.
     Emissions tracked by Code Carbon tracker and stored in an S3 bucket ("emissions.csv").

This command is used for issuing an inference request - curl -X POST -H "Content-Type: application/json" -d '{"inputs": "I love  you .", "parameters_list": null}' http://localhost:8080/invocations
Output - {"emissions":"2.7711033091126124e-07","english2german":["Ich liebe Sie."]}
