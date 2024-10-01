# Medical_Report_summarizer API

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Obtain JWT Token](#obtain-jwt-token)
  - [Summarizer API Endpoints]()
  - [Status Checker]()

## Installation and Setup
1. Clone the repository:

```git clone https://github.com/hamzasand/Medical_Report_summarizer.git```

2. Sghould have python version is 3.8.19:

3. Install required packages:

``` pip install -r requirements.txt ```

4. Start the development server:

``` uvicorn main:app --reload ```

5. Activate celery worker

``` celery -A celery_config worker --loglevel=info ```

## API Documentation
## Authentication

Most of the endpoints in this API require authentication using JWT (JSON Web Token). To obtain a token, use the following endpoint:

### Obtain JWT Token

- **Endpoint:** `http://35.192.167.106:8000/token`
- **Method:** POST
- **Description:** This endpoint is used to obtain an access token. The token is used to authenticate subsequent requests to the API.

- **Response:**
  - Example:
    ```json
    {
      "access": "your_access_token",
      "refresh": "your_refresh_token"
    }
    ```

- **Notes:** Use the `access` token for authentication in subsequent requests.

## Endpoints

### summarizer API Endpoints

- **Endpoint:** `http://35.192.167.106:8000/summarize/`
- **Method:** POST
- **Description:** This endpoint is used to upload a medical report in PDF format and initiate a background task to summarize the report. The user must be authenticated to use this endpoint.
- **Authorization:** Bearer token for user authentication.
- **Request:**
  - Body:
    ```form-data
    {
      "file": "PDF file for summary"
    }
    ```
- **Response:**
  - Example:
    ```json
    {
      "task_id": "string",
      "status": "Task started"
    }

    ```

### Status Checker

- **Endpoint:** `GET /tasks/{task_id}`
- **Method:** GET
- **Description:** This endpoint is used to check the status of a background task by providing the task_id returned from the /summarize/ endpoint.
- **Response:**
  - Example:
    ```json
    {
      "task_id": "string",
      "task_status": "string",
      "task_result": "object or null"
    }

    ```
