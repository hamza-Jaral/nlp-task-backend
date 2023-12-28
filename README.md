# FastAPI API Documentation

This document provides instructions on setting up and using the FastAPI-based API endpoints for processing CSV files and performing question answering.

## Prerequisites

1. **Python Environment:**
   - Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

2. **Virtual Environment:**
   - Create a virtual environment to isolate dependencies.
     ```bash
     python -m venv venv
     ```

3. **Activate Virtual Environment:**
   - Activate the virtual environment.
     - On Windows:
       ```bash
       .\venv\Scripts\activate
       ```
     - On Unix or MacOS:
       ```bash
       source venv/bin/activate
       ```

4. **Install Requirements:**
   - Install the required Python packages.
     ```bash
     pip install -r requirements.txt
     ```

## Running the API Server

1. **Run the FastAPI Server:**
   - Execute the following command to start the FastAPI server.
     ```bash
     uvicorn app.main:app --reload
     ```
   - The `--reload` flag enables automatic reloading of the server when code changes are detected.

2. **Access API Documentation:**
   - Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
   - This will open the FastAPI Swagger UI, providing an interactive interface for exploring and testing the API endpoints.

## API Endpoints

### 1. Process CSV File

- **Endpoint:** `/process_csv`
- **Method:** `POST`
- **Request Payload:**
  - Upload a CSV file using the provided form.
- **Response:**
  - Successful response: `{"message": "File processed and stored"}`
  - In case of an error, an appropriate error message will be returned.

### 2. Question Answering

- **Endpoint:** `/qa`
- **Method:** `POST`
- **Request Payload:**
  - Provide a JSON object with the question using the key `query`.
    ```json
    {"query": "Your question goes here"}
    ```
- **Response:**
  - Successful response: `{"response": "Answer to the question"}`
  - In case of an error, an appropriate error message will be returned.
