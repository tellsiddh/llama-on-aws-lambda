import boto3
from llama_cpp import Llama
import os

MODEL_SESSION = None

def handler(event, context):
    global MODEL_SESSION

    if MODEL_SESSION is None:
        bucket_name = "mistral7b8bit"
        object_key = "mistral-7b-instruct-v0.1.Q8_0.gguf"
        s3 = boto3.client('s3')
        local_model_path = "/tmp/mistral-7b-instruct-v0.1.Q8_0.gguf"
        s3.download_file(bucket_name, object_key, local_model_path)

        MODEL_SESSION = Llama(model_path=local_model_path, n_threads=6)

    instruction = event.get("instruction", "What is the capital of Spain?")
    max_tokens = event.get("max_tokens", 32)  # Default value for max_tokens

    max_tokens = int(max_tokens)

    system_message = "You are a helpful assistant Chatbot who only answers based on your own knowledge based. Do not assume any answer and always give coherent responses. Your name is JARVIS."
    user_message = instruction
    response = MODEL_SESSION(user_message, max_tokens=max_tokens, temperature=0.6, stop=["Q:"], echo=True)

    return {"result": response}
