import boto3
import json
import base64
import os

prompt_data=""""
generate a highest pixel quality desktop wallpaper of a calm night at beach, also use a starry sky and cinematic display

"""
prompt_template=[{"text": prompt_data}]
bedrock=boto3.client(service_name="bedrock-runtime")

payload={
    "textToImageParams":{
        "text": prompt_data,
        #"negativeText": "no people, no buildings"
        } ,
    
    "taskType": "TEXT_IMAGE",
    "imageGenerationConfig":{
        "cfgScale":8,
        "seed":0,
        "quality":"standard",
        "width":1024,
        "height":1024,
        "numberOfImages":4}
 
}

body=json.dumps(payload)
model_id="amazon.titan-image-generator-v1"
response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
    )

response_body = json.loads(response.get("body").read())

base64_image = response_body.get("images")[0]
base64_bytes = base64_image.encode('ascii')
image_bytes = base64.b64decode(base64_bytes)

finish_reason = response_body.get("error")

if finish_reason is not None:
    print(f"Image generation error. Error is {finish_reason}")

else: 
    print("Successfully generated image with model:", model_id)


#save image to a file in the output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
file_name = f"{output_dir}/generated-img.png"
with open(file_name, "wb") as f:    
     f.write(image_bytes)