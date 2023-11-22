# llama-on-aws-lambda

This guide is crafted to assist in deploying serverless AWS Lambda functions using the Llama-CPP library and GGUF quantized model, optimized for both ARM and x86 architectures with AWS S3 integration for model storage.

## Overview

- **Objective**: Implement serverless functions on AWS Lambda utilizing Llama-CPP with a GGUF quantized model.
- **Platforms**: Deployment is configured for ARM and x86 architectures.
- **Storage**: AWS S3 is used for storing models and Docker images.
- **Containerization**: Docker facilitates the packaging and deployment process.
- **ECR**: Streamlines the process of pushing Docker images to the Amazon Elastic Container Registry.

## Prerequisites

- An AWS account with the necessary permissions for Lambda, S3, and ECR services.
- Docker environment set up on your local machine.
- Proficiency in AWS service management, Docker operations, and Python scripting.

## Repository Structure

The repository includes the following directories and a README file:

- `serverless_amd`: Contains configurations for deploying the serverless function on AMD architecture.
- `serverless_arm`: Houses configurations for the ARM architecture deployment.
- `serverless_s3`: Maintains scripts and configurations for integrating AWS S3 within the serverless solution.
- `README.md`: Provides an overall guide to the repository, including setup procedures and project details.

### Inside Each Directory

Each of the `serverless_amd`, `serverless_arm`, and `serverless_s3` directories should ideally contain:

- A Dockerfile tailored to the specific architecture or storage service requirements.
- Scripts and any additional dependencies required for deployment.
- A dedicated README.md file explaining the unique aspects, setup steps, and environment variables pertinent to that directory.

## Dockerfile Details

### For x86 Architecture

1. **Foundation Image**: `python:3.11` targeted for `linux/amd64`.
2. **Setup**:
    - Directory `${FUNCTION_DIR}` is established as the workspace.
    - `libopenblas-dev` is installed to enhance numerical computation.
3. **Llama-CPP**: Installed with `pip` using specific CMAKE_ARGS.
4. **Dependencies**: Installed from the `requirements.txt`.
5. **Lambda Code**: Incorporates `lambda_function.py` into the image.
6. **Execution**: Sets up AWS Lambda Runtime Interface Client as the entry point.

### For ARM Architecture

Follows the x86 Dockerfile with the base image switched to `python:3.11-slim-bookworm` for `linux/arm64`, and the inclusion of `gcc`, `g++`, and `pkg-config`.

## Lambda Function Logic

- **Model Bootstrapping**: Delays the loading of the GGUF model to the first invocation.
- **Request Handling**: Manages incoming `instruction` and `max_tokens` from the event.
- **Response Output**: Engages the Llama model to generate responses.

## Docker Build and Push Commands

1. **Build Docker Image**:

`docker buildx build --no-cache --platform linux/<amd64 or arm64> -t <account>.dkr.ecr.<region>.amazonaws.com/<repository-name>:<tag> --push .`

2. **Authenticate Docker with ECR**:

`sudo aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com`

## Performance Insights

- The Llama-CPP library yields 10 tokens per second with threads set to 4 or 6.
- AWS Lambda functions are optimized with 6 vCPUs to align with Llama-CPP's performance.

## Deployment Steps

1. **Build Docker Images**: Execute the build commands with appropriate parameters.
2. **Push to ECR**: Authenticate with ECR to push the Docker images.
3. **Lambda Function Setup**: Configure Lambda functions with the Docker images for ARM and x86, and adjust memory and timeout settings.
4. **S3 Configuration**: Verify the GGUF model's presence in the S3 bucket.
5. **Testing**: Invoke Lambda functions with test events to confirm expected functionality.

## Conclusion

This guide delineates a structured approach to deploying serverless functions on AWS Lambda using Docker with the Llama-CPP library and GGUF quantized model, supporting both ARM and x86 architectures, and detailing AWS S3 integration for efficient model management.

## References

- Penkow, [How to Deploy Llama 2 as an AWS Lambda Function for Scalable Serverless Inference](https://medium.com/@penkow/how-to-deploy-llama-2-as-an-aws-lambda-function-for-scalable-serverless-inference-e9f5476c7d1e). Medium, Accessed on November 20, 2023.

- [Serverless Compute for LLM with a Step-by-Step Guide for Hosting Mistral 7B on AWS Lambda](https://aws.plainenglish.io/serverless-compute-for-llm-with-a-step-by-step-guide-for-hosting-mistral-7b-on-aws-lambda-0a267e153cae). AWS Plain English, Accessed on November 20, 2023.

- [How We Serve 25M API Calls from 10 Scalable Global Endpoints for $150 a Month](https://www.freecodecamp.org/news/how-we-serve-25m-api-calls-from-10-scalable-global-endpoints-for-150-a-month-911002703280/). freeCodeCamp, Accessed on November 20, 2023.


