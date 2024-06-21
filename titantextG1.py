import boto3
import json

inputText_data=""""
write a poem in style of best English poet where subject is beauty of nature

"""

bedrock=boto3.client(service_name="bedrock-runtime")

payload={
    "inputText": inputText_data ,
    "textGenerationConfig":{
        "maxTokenCount":3072,
        "stopSequences":[],
        "temperature":0.7,
        "topP":0.9}
   
}

body=json.dumps(payload)
model_id="amazon.titan-text-premier-v1:0"
response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
    )


response_body=json.loads(response.get("body").read())  # here is a key called body inside that body u will find entire information of the response u r able to get

if 'results' in response_body:
        results = response_body['results']
        for result in results:
            if 'outputText' in result:
                response_text = result['outputText']
                # Decode bytes to UTF-8 string
                # response_text =result['outputText'].encode('latin1').decode('utf-8')
                print("Generated Text:")
                print(f"'''\n{response_text}\n'''")
            else:
                print("Error: 'outputText' key not found in result")
else:
        print("Error: 'results' key not found in response")
