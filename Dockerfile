# Use the official AWS Python 3.11 Lambda base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR /var/task

# Copy application files
COPY app.py .
COPY requirements.txt .
COPY firebase-creds.json .

# Install dependencies
RUN pip install -r requirements.txt -t .

# Command to run the Lambda handler
CMD ["app.lambda_handler"]
