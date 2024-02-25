curl -X POST -H "Content-Type: application/json" -d '{"inputs": "I love  you .", "parameters_list": null}' http://localhost:8080/invocations

Output - {"emissions":"2.7711033091126124e-07","english2german":["Ich liebe Sie."]}
