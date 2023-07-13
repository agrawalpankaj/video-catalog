import base64
import io

import pytest
from faker import Faker

fake = Faker()


class TestCaseHelper:
    @staticmethod
    def create_catalog_object(client):
        # Prepare the fake video data
        fake_video_data = fake.image()  # Replace with actual video data

        # Convert video data to base64-encoded string
        video_base64 = base64.b64encode(fake_video_data).decode("utf-8")

        # Prepare the request data as form data
        data = {
            "title": "test",
            "description": "This is a test video",
            "duration": 15,
        }

        # Create a BytesIO object from base64-encoded video data
        video_data = io.BytesIO(base64.b64decode(video_base64))

        # Send the request with form data
        response = client.post(
            "/videocatalog/create/",
            data=data,
            files={"video": ("fake_video.mp4", video_data, "video/mp4")},
        )
        return response


class TestVideoCatalog:
    def test_01_videocatalog_create(self, client):
        """
        Test case for creating a video in the video catalog.

        It prepares the fake video data, converts it to base64, and sends a POST request
        with the form data and video file. It asserts the response status code, message,
        and data.

        """
        # Helper function to create new video catalog object
        response = TestCaseHelper.create_catalog_object(client)

        # Perform assertions
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"] is not None

    def test_02_videocatalog_create_failed_title(self, client):
        """
        Test case for creating a video with an empty title in the video catalog.

        It prepares the fake video data, converts it to base64, and sends a POST request
        with the form data and video file. The title is intentionally left empty. It asserts
        the response status code and message.

        """
        # Prepare the fake video data
        fake_video_data = fake.image()  # Replace with actual video data

        # Convert video data to base64-encoded string
        video_base64 = base64.b64encode(fake_video_data).decode("utf-8")

        # Prepare the request data as form data with empty title
        data = {
            "title": "",
            "description": "This is a test video",
            "duration": 15,
        }

        # Create a BytesIO object from base64-encoded video data
        video_data = io.BytesIO(base64.b64decode(video_base64))

        # Send the request with form data
        response = client.post(
            "/videocatalog/create/",
            data=data,
            files={"video": ("fake_video.mp4", video_data, "video/mp4")},
        )

        # Perform assertions
        assert response.json()["status_code"] == 400
        assert response.json()["message"] == "Video Title is required"

    def test_03_videocatalog_create_failed_video(self, client):
        """
        Test case for creating a video with an empty video file in the video catalog.

        It prepares an empty video data and sends a POST request with the form data
        and empty video file. It asserts the response status code and message.

        """
        # Prepare the empty video data
        fake_video_data = b""  # Empty video data

        # Prepare the request data as form data
        data = {
            "title": "test",
            "description": "This is a test video",
            "duration": 15,
        }

        # Create a BytesIO object from the empty video data
        video_data = io.BytesIO(fake_video_data)

        # Send the request with form data
        response = client.post(
            "/videocatalog/create/",
            data=data,
            files={"video": ("", video_data, "video/mp4")},
        )

        # Perform assertions
        assert response.json()["status_code"] == 400
        assert response.json()["message"] == "Video Content is required"

    def test_04_videocatalog_create_failed_description(self, client):
        """
        Test case for creating a video with an empty description in the video catalog.

        It prepares the fake video data, converts it to base64, and sends a POST request
        with the form data and video file. The description is intentionally left empty.
        It asserts the response status code and message.

        """
        # Prepare the fake video data
        fake_video_data = fake.image()  # Replace with actual video data

        # Convert video data to base64-encoded string
        video_base64 = base64.b64encode(fake_video_data).decode("utf-8")

        # Prepare the request data as form data with empty description
        data = {
            "title": "test",
            "description": "",
            "duration": 15,
        }

        # Create a BytesIO object from base64-encoded video data
        video_data = io.BytesIO(base64.b64decode(video_base64))

        # Send the request with form data
        response = client.post(
            "/videocatalog/create/",
            data=data,
            files={"video": ("fake_video.mp4", video_data, "video/mp4")},
        )

        # Perform assertions
        assert response.json()["status_code"] == 400
        assert response.json()["message"] == "Video Description is required"

    def test_05_videocatalog_list(self, client):
        """
        Test case for retrieving the list of videos from the video catalog.

        It sends a GET request to the list endpoint and asserts the response status code
        and message.

        """
        response = client.get("/videocatalog/list/")
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"

    def test_get_video_list_with_pagination(self, client):
        """
        Test case for retrieving the list of videos from the video catalog with pagination.

        It sends a GET request to the list endpoint with a specific page number and asserts
        the response status code and message.

        """
        # Make a request to the API with page number 1
        response = client.get("/videocatalog/list/?page=1")

        # Assert the response
        assert response.status_code == 200
        assert response.json()["message"] == "success"

    def test_06_videocatalog_detail(self, client):
        """
        Test case for retrieving the details of a video from the video catalog.

        It sends a GET request to the detail endpoint with a valid video ID and asserts
        the response status code and message.

        """
        # Helper function to create new video catalog object
        res = TestCaseHelper.create_catalog_object(client)
        res.json()["status_code"] == 200
        res.json()["message"] == "success"

        video_catalog_id = res.json()["data"]["id"]
        response = client.get(f"/videocatalog/detail/{video_catalog_id}/")
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"

    def test_07_videocatalog_detail_failed(self, client):
        """
        Test case for retrieving the details of a video that does not exist in the video catalog.

        It sends a GET request to the detail endpoint with an invalid video ID and asserts
        the response status code and message.

        """
        response = client.get("/videocatalog/detail/66/")
        assert response.json()["status_code"] == 400
        assert response.json()["message"] == "obj not found"

    def test_08_videocatalog_delete(self, client):
        """
        Test case for deleting a video from the video catalog.

        It sends a POST request to the delete endpoint with a valid video ID and asserts
        the response status code and message.

        """
        # Helper function to create new video catalog object
        res = TestCaseHelper.create_catalog_object(client)
        res.json()["status_code"] == 200
        res.json()["message"] == "success"

        video_catalog_id = res.json()["data"]["id"]

        response = client.post(f"/videocatalog/delete/{video_catalog_id}/")

        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"

    def test_09_videocatalog_delete_failed(self, client):
        """
        Test case for deleting a video that does not exist in the video catalog.

        It sends a POST request to the delete endpoint with an invalid video ID and asserts
        the response status code and message.

        """
        response = client.post("/videocatalog/delete/66/")
        assert response.json()["status_code"] == 400
        assert response.json()["message"] == "obj not found"

    def test_10_videocatalog_update(self, client):
        """
        Test case for updating a video in the video catalog.

        It prepares the fake video data, converts it to base64, and sends a POST request
        with the form data and video file. It asserts the response status code, message,
        and data.

        """
        # Helper function to create new video catalog object
        res = TestCaseHelper.create_catalog_object(client)
        res.json()["status_code"] == 200
        res.json()["message"] == "success"

        video_catalog_id = res.json()["data"]["id"]

        # Prepare the request data as form data
        data = {
            "title": "test",
            "description": "This is a test video",
            "duration": 15,
        }

        fake_video_data = fake.image()

        # Convert video data to base64-encoded string
        video_base64 = base64.b64encode(fake_video_data).decode("utf-8")

        # Create a BytesIO object from base64-encoded video data
        video_data = io.BytesIO(base64.b64decode(video_base64))

        # Send the request with form data
        response = client.post(
            f"/videocatalog/edit/{video_catalog_id}/",
            data=data,
            files={"video": ("fake_video.mp4", video_data, "video/mp4")},
        )

        # Perform assertions
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"] is not None

    def test_11_videocatalog_update_failed(self, client):
        """
        Test case for updating a video that does not exist in the video catalog.

        It prepares the fake video data, converts it to base64, and sends a POST request
        with the form data and video file. The video ID is intentionally set to an invalid ID.
        It asserts the response status code and message.

        """
        # Prepare the fake video data
        fake_video_data = fake.image()  # Replace with actual video data

        # Convert video data to base64-encoded string
        video_base64 = base64.b64encode(fake_video_data).decode("utf-8")

        # Prepare the request data as form data
        data = {
            "title": "test",
            "description": "This is a test video",
            "duration": 15,
        }

        # Create a BytesIO object from base64-encoded video data
        video_data = io.BytesIO(base64.b64decode(video_base64))

        # Send the request with form data
        response = client.post(
            "/videocatalog/edit/66/",
            data=data,
            files={"video": ("fake_video.mp4", video_data, "video/mp4")},
        )

        # Perform assertions
        assert response.json()["status_code"] == 400
        assert response.json()["message"] == "Video ID not found"

    def test_12_update_video_without_new_video(self, client):
        """
        Test case for updating a video without providing a new video file.

        It prepares the request data with updated title and description, but without a new video file.
        It sends a POST request to the edit endpoint with a valid video ID and asserts the response
        status code and message.

        """
        # Helper function to create new video catalog object
        res = TestCaseHelper.create_catalog_object(client)
        res.json()["status_code"] == 200
        res.json()["message"] == "success"

        video_catalog_id = res.json()["data"]["id"]

        # Provide the necessary input data
        video_form = {
            "title": "Updated Title",
            "description": "Updated Description"
        }

        # Make the request to the API endpoint
        response = client.post(f"/videocatalog/edit/{video_catalog_id}/", data=video_form)

        # Assert the response
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"

    def test_13_update_video_without_new_title(self, client):
        """
        Test case for updating a video without providing a new title.

        It prepares the request data with updated description, but without a new title.
        It sends a POST request to the edit endpoint with a valid video ID and asserts the response
        status code and message.

        """
        # Helper function to create new video catalog object
        res = TestCaseHelper.create_catalog_object(client)
        res.json()["status_code"] == 200
        res.json()["message"] == "success"

        video_catalog_id = res.json()["data"]["id"]

        # Provide the necessary input data
        video_form = {
            "title": "",
            "description": "Updated Description"
        }

        # Make the request to the API endpoint
        response = client.post(f"/videocatalog/edit/{video_catalog_id}/", data=video_form)

        # Assert the response
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"

    def test_14_update_video_without_new_description(self, client):
        """
        Test case for updating a video without providing a new description.

        It prepares the request data with updated title, but without a new description.
        It sends a POST request to the edit endpoint with a valid video ID and asserts the response
        status code and message.

        """
        # Helper function to create new video catalog object
        res = TestCaseHelper.create_catalog_object(client)
        res.json()["status_code"] == 200
        res.json()["message"] == "success"

        video_catalog_id = res.json()["data"]["id"]

        # Provide the necessary input data
        video_form = {
            "title": "Updated Title",
            "description": ""
        }

        # Make the request to the API endpoint
        response = client.post(f"/videocatalog/edit/{video_catalog_id}/", data=video_form)

        # Assert the response
        assert response.json()["status_code"] == 200
        assert response.json()["message"] == "success"

