import boto3
import json
import os
import re

prompt_data="""<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

write a very short blog on healthy food in today's world[/INST]"""


bedrock=boto3.client(service_name="bedrock-runtime")

payload={      
    "prompt":prompt_data,
    "max_gen_len":1024,
    "temperature":0.5,
    "top_p":0.9,   
}

body=json.dumps(payload)
model_id="meta.llama3-8b-instruct-v1:0"
response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
    )

response_body=json.loads(response.get('body').read()) # here is a key called body inside that body, u will find entire information of the response u r able to get

generated_text = response_body['generation']
prompt_token_count = response_body['prompt_token_count']
generation_token_count = response_body['generation_token_count']
stop_reason = response_body['stop_reason']


if generated_text:
        print(f"Generated Text: {generated_text}")
        print(f"Prompt Token count:  {prompt_token_count}")
        print(f"Generation Token count:  {generation_token_count}")
        print(f"Stop Reason: {stop_reason}")
        
        # Check if the stop reason indicates the instruction was followed and finished
        #         if stop_reason == 'instruction_followed':            
else:
    print("No generated text found in the response.")

#save blog to a file in the output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
file_name = f"{output_dir}/generated-blog.txt"
with open(file_name, "w") as f:    
     f.write(generated_text)
