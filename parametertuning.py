import itertools
import random
import time
import csv
from llama_cpp import Llama

# Define the range of values for each parameter
n_gpu_layers_options = [-1, 0]
n_threads_options = [4, 8, 16, 32]
max_tokens_options = [16, 32, 64]
stop_options = [["Q:"], ["Q:", "\n"]]
echo_options = [True]
use_mmap_options = [True, False]
numa_options = [True, False]
# Generate all possible combinations
all_combinations = list(itertools.product(
    n_gpu_layers_options, n_threads_options, max_tokens_options, stop_options, echo_options
))

# Randomize the order of trials
random.shuffle(all_combinations)

# Initialize the model
llm = Llama(model_path="/home/siddh/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

# Run trials and record results
results = []

for combination in all_combinations:
    n_gpu_layers, n_threads, max_tokens, stop, echo = combination
    start_time = time.time()
    
    # Assuming these parameters are passed in the correct way to the model
    output = llm("Q: Name the planets in the solar system? A: ", max_tokens=max_tokens, stop=stop, echo=echo)
    
    end_time = time.time()
    time_taken = end_time - start_time

    # Extract the response text
    response_text = output['choices'][0]['text']

    # Save the results
    results.append([n_gpu_layers, n_threads, max_tokens, stop, echo, time_taken, response_text])

# Save results to a CSV file
with open('llama_trials_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['n_gpu_layers', 'n_threads', 'max_tokens', 'stop', 'echo', 'time_taken', 'response'])
    writer.writerows(results)
