import itertools
import random
import time
import csv
from llama_cpp import Llama

# Define the range of values for each parameter
n_threads_options = [None, 4, 6, 8]
max_tokens_options = [16]
echo_options = [True]
use_mmap_options = [True, False]
numa_options = [True, False]

# Generate all possible combinations
all_combinations = list(itertools.product(
    n_threads_options, max_tokens_options, echo_options, use_mmap_options, numa_options
))

# Randomize the order of trials
random.shuffle(all_combinations)

# Model path (constant parameter)
model_path = "/home/siddh/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# Run trials and record results
results = []

for combination in all_combinations:
    n_threads, max_tokens, echo, use_mmap, numa = combination

    # Initialize the model
    try:
        llm = Llama(model_path=model_path, n_threads=n_threads, use_mmap=use_mmap, numa=numa)
        start_time = time.time()

        # Execute the model with the given parameters
        output = llm("Q: Name the planets in the solar system? A: ", max_tokens=max_tokens, echo=echo)

        end_time = time.time()
        time_taken = end_time - start_time
        tokens_per_second = max_tokens / time_taken if time_taken > 0 else 'inf'
        response_text = output['choices'][0]['text']

        results.append([n_threads, max_tokens, echo, use_mmap, numa, time_taken, tokens_per_second, response_text])
    except Exception as e:
        results.append([n_threads, max_tokens, echo, use_mmap, numa, None, None, f"Error: {e}"])
    finally:
        # Properly close the model instance
        del llm

# Save results to a CSV file
csv_filename = 'llama_trials_results.csv'
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['n_threads', 'max_tokens', 'echo', 'use_mmap', 'numa', 'time_taken', 'tokens_per_second', 'response'])
    writer.writerows(results)

print(f"Trials completed. Results saved to {csv_filename}")
