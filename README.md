
======================================================================================================
# Build a REST API with FastAPI, PostgreSQL and SQLAlchemy
FastAPI is a Python framework and set of tools that allow developers to invoke commonly used functions using a REST interface.

SQLAlchemy isMost of the time, this library is used as an Object Relational Mapper (ORM) tool, which automatically converts function calls to SQL queries and translates Python classes to tables on relational databases.


## Getting Started
### Prerequisites
* Python 3.8 or higher
* python3-venv package

### Installing
* Clone the repository
* Install the python3-venv package if it's not already installed.

```
sudo apt-get update
```
```
sudo apt-get install python3-venv
```

* Create a virtual environment using python3 -m venv env command.

```
python3 -m venv env
```
* Activate the virtual environment using . env/bin/activate command.
```
source env/bin/activate
```
* Install the required dependencies using pip install -r requirements.txt.

```
pip install -r requirements
```

## Environment Variables
Make sure to set the following environment variables in your local environment or in your deployment environment (.env):

- `ENVIRONMENT`: Environment identifier (e.g., local, staging, production).
- `POSTGRES_HOST`: PostgreSQL database host.
- `POSTGRES_PORT`: PostgreSQL database port.
- `POSTGRES_USER`: PostgreSQL database username.
- `POSTGRES_PASS`: PostgreSQL database password.
- `POSTGRES_DB`: PostgreSQL database name.
- `DB_TYPE`: Database type (e.g., postgresql, mysql, sqlite).

- `VIDEO_CONTENT_PATH`: Path for storing video content.
- `MEDIA_HOST`: Base URL for serving media files.


## Migrations
* Initialize the migration using alembic init alembic command. This is a one-time run.
```
alembic init alembic
```
* Create new migrations using alembic revision --autogenerate -m "New Migration" command.
```
alembic revision --autogenerate -m "New Migration"
```
* Apply the migrations using alembic upgrade head command.
```
alembic upgrade head
```

* Downgrade migrations
```
alembic downgrade -1
```

* Check current version
```
alembic current
```

## API Endpoints

### `POST /videocatalog/create/`

Create a new video in the video catalog.

**Request Payload:**

Form Data:
- `title`: The title of the video.
- `description`: The description of the video.
- `video`: The video file.

**Response:**

```json
{
    "data": {
        "id": 1,
        "title": "Video Title",
        "description": "Video Description",
        "duration": 120
    },
    "status_code": 200,
    "message": "Success",
    "error": null
}
```

### `GET /videocatalog/detail/{id}/`

Detail video by ID in the video catalog.

**Response:**

```json
{
    "data": {
        "id": 1,
        "title": "Video Title",
        "description": "Video Description",
        "duration": 120
    },
    "status_code": 200,
    "message": "Success",
    "error": null
}
```

### `GET /videocatalog/list/`

list of video including pagination in the video catalog.

Params:
- `page`: Page Number .

**Response:**

```json
[
    {
        "data": {
            "id": 1,
            "title": "Video Title",
            "description": "Video Description",
            "duration": 120
        },
        "status_code": 200,
        "message": "Success",
        "error": null
    },
    {
        "data": {
            "id": 2,
            "title": "Video Title",
            "description": "Video Description",
            "duration": 120
        },
        "status_code": 200,
        "message": "Success",
        "error": null
    }
]
```
### `POST /videocatalog/delete/{id}/`

Delete video by ID in the video catalog.

**Response:**

```json
{
    "data": {
        "id": 1,
        "title": "Video Title",
        "description": "Video Description",
        "duration": 120
    },
    "status_code": 200,
    "message": "Success",
    "error": null
}
```

### `POST /videocatalog/edit/{id}/`
Update video form by ID in the video catalog.

Form Data:
- `title`: The title of the video.
- `description`: The description of the video.
- `video`: The video file.

**Response:**

```json
{
    "data": {
        "id": 1,
        "title": "Video Title",
        "description": "Video Description",
        "duration": 120
    },
    "status_code": 200,
    "message": "Success",
    "error": null
}
```


## Running
* Run the server using uvicorn main:app --reload command.
```
uvicorn main:app --reload
```

## Running Test Case
* Run tests using pytest tests/ command.
```
pytest tests/
```
## Running Coverage Report
* Run tests coverage.
```
coverage run -m pytest
```
```
coverage report
```
```
coverage html
```
## Built With
* FastAPI
* Alembic
* SQLAlchemy
