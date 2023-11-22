ARG FUNCTION_DIR="/function"

# Use the slim version of the Python image
FROM --platform=linux/arm64 python:3.11-slim-bookworm

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

# Copy and install dependencies
COPY model/ model/
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc g++ pkg-config
RUN apt-get update && apt-get -y install libopenblas-dev
RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install --target /function --no-cache-dir llama-cpp-python
RUN pip install --target ${FUNCTION_DIR} --no-cache-dir -r requirements.txt

# Copy the lambda function
COPY lambda_function.py .

# Set the entry point and command
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "lambda_function.handler" ]
