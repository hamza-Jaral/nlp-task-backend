import csv
import io
import json
import os
import traceback

import dotenv
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .qa_manager import DataIndexer, QAManager


dotenv.load_dotenv()

app = FastAPI(title="nlp-task")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    query: str


def process_csv_data(contents: str):
    doc_dict = {}
    data_folder = "data"
    file_paths = []

    # Using CSV reader to parse the input contents
    reader = csv.DictReader(io.StringIO(contents))

    required_columns = ['pagenum', 'doc_name', 'text']
    if not all(col in reader.fieldnames for col in required_columns):
        raise ValueError("CSV file has the wrong format. Missing required columns.")

    for row in reader:
        pagenum = int(row['pagenum'])
        doc_name = row['doc_name']
        text = row['text']

        if doc_name not in doc_dict:
            doc_dict[doc_name] = []

        # Check if there's already an entry for the given page number
        existing_entry = next((entry for entry in doc_dict[doc_name] if entry['pagenum'] == pagenum), None)

        if existing_entry:
            # If the entry exists, concatenate the text
            existing_entry['text'] += ' ' + text
        else:
            # If the entry doesn't exist, add a new entry to the list
            doc_dict[doc_name].append({"doc_name": doc_name, 'pagenum': pagenum, 'text': text})

    os.makedirs(data_folder, exist_ok=True)
    for doc_name, content in doc_dict.items():
        file_path = os.path.join(data_folder, f"{doc_name}.json")
        with open(file_path, 'w') as f:
            doc_dict = {"document": content}
            json.dump(doc_dict, f, indent=4)
            file_paths.append(file_path)

    return file_paths


@app.get("/")
def read_root():
    return {"response": "world"}


@app.post("/process_csv")
async def process_csv(file: UploadFile):
    """
        Process CSV File and Create Embeddings

        Parameters:
        - file (UploadFile): CSV file containing data to be processed.

        Returns:
        - str: a message indicating the success or error description in case of server side error

        This endpoint takes an uploaded CSV file, processes the data within, and generates embeddings.
        The CSV file should have the required columns (e.g., 'pagenum', 'doc_name', 'text').
        """

    try:
        # Read the CSV file
        contents = await file.read()

        # Process the CSV data
        file_paths = process_csv_data(contents.decode('utf-8'))

        indexer = DataIndexer()
        indexer.create_chroma_db_embedding(file_paths=file_paths)

        return {"message": "File processed and stored"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing the CSV file: {str(e)}")


@app.post("/qa")
def question_answering(query: Query):
    """
        Question Answering Endpoint

        Parameters:
        - query (Query): An object containing the user's query.

        Returns:
        - dict: A dictionary containing the response to the user's query.

        This endpoint takes a user's question, processes it using a Question Answering Manager,
        and returns the response. It utilizes a QAManager class to handle the question and generate an answer.

        Example Usage:
        ```
        import httpx

        query = {"query": "What is the capital of France?"}
        response = httpx.post("http://your-api-endpoint/qa", json=query)
        print(response.json())
        ```
        """
    try:
        question = query.query
        qa_chain = QAManager()
        response = qa_chain.ask(question)

        return {"response": response}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
