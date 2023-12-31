# FastAPI API Documentation

This document provides instructions on setting up and using the FastAPI-based API endpoints for processing CSV files and performing question answering.

## Data Engineering

### Raw Data
The raw data is sourced from the `text_segments.csv` file, containing information about document segments including `pagenum`, `docname`, and `text`.

### Data Engineering Process
1. **Text Aggregation:** Combine text segments from the same page of the same document to enhance document coherency.
2. **JSON Serialization:** Serialize aggregated text segments into JSON files, one for each unique document, to preserve metadata.

## Challenges Faced

1. **Consistency in Document Processing:** Ensuring uniformity in document structure to facilitate effective embedding for question-answering.
2. **Document File Format Selection:** Choosing between file formats; JSON was selected for metadata retention.

## Proposed Improvements

1. **Custom Prompts for QA:** Enhance question-answering with custom prompts for more polite and nuanced responses.

2. **Guardrails Implementation:** Strengthen input validation and error handling mechanisms.

3. **Chat History Integration:** Enable continuous conversations by adding support for chat history.

4. **User-Specific Document Support:** Allow users to upload and analyze their own documents.

## Project Structure

- `app/`: Contains the FastAPI application code.
- `data/`: Holds processed data, including serialized JSON files.


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

5. **Create .env file:**
   - Create a `.env` file in the project root based on the provided `env.example` file. This file should contain any necessary environment variables.

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

## Running the API Server with Docker Compose

1. **Build and Run Docker Containers:**
   - Execute the following command to build the Docker image and start the FastAPI server along with any required services defined in the `docker-compose.yml` file.
     ```bash
     docker-compose up --build -d
     ```
   - The `--build` flag ensures that the Docker images are rebuilt, and the `-d` flag runs the services in the background.

2. **Access API Documentation:**
   - Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
   - This will open the FastAPI Swagger UI, providing an interactive interface for exploring and testing the API endpoints.

3. **Stopping Docker Compose:**
   - To stop the running containers, use the following command:
     ```bash
     docker-compose down
     ```
   - This will stop and remove the containers defined in the `docker-compose.yml` file.


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
