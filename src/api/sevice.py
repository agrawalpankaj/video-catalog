import os
import uuid
from math import ceil

from fastapi import status
from moviepy.editor import VideoFileClip
from starlette.config import Config

from src.api.model import Video
from src.api.validators import FromValidator

config = Config(".env")
MEDIA_HOST = config("MEDIA_HOST")
VIDEO_CONTENT_PATH = config("VIDEO_CONTENT_PATH")


class VideoCatalogService:
    def __init__(self, request, response, db):
        self.request = request
        self.response = response
        self.db = db

    def create_new_video(self, video_form, video_contents):
        try:
            # Validate the form data
            result, message = FromValidator.from_validator(video_form, self.db)
            if not result:
                return {
                    "data": None,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": message,
                    "error": None,
                }

            if result:
                # Get video title and path
                title = video_form.get("title")
                video_path = video_form.get("video").filename
                video_path = os.path.join(VIDEO_CONTENT_PATH, video_path)

                # Check if video file exists
                if not os.path.exists(video_path):
                    duration = 0  # Set default duration if video file doesn't exist
                else:
                    # Save video file
                    with open(video_path, "wb") as vid:
                        vid.write(video_contents)
                    try:
                        # Calculate video duration using VideoFileClip
                        clip = VideoFileClip(video_path)
                        duration = int(clip.duration)
                        clip.close()
                    except Exception as e:
                        duration = 0  # Set default duration if an error occurs

                # Create and save video object
                organizer = Video(
                    title=title,
                    video_file=video_path,
                    description=video_form.get("description"),
                    duration=duration,
                )
                self.db.add(organizer)
                self.db.commit()
                self.db.refresh(organizer)

                # Update video file path with media host
                organizer.video_file = MEDIA_HOST + organizer.video_file

                return {
                    "data": organizer,
                    "status_code": status.HTTP_200_OK,
                    "message": "success",
                    "error": None,
                }

            return {
                "data": None,
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": message,
                "error": None,
            }
        except Exception as e:
            return {
                "data": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "failed",
                "error": str(e),
            }

    def video_list(self, limit, offset):
        try:
            # Get the total count of videos
            total_videos = self.db.query(Video).count()

            # Calculate the total number of pages
            total_pages = ceil(total_videos / limit)

            # Query the videos with pagination
            videos = self.db.query(Video).limit(limit).offset(offset).all()

            return {
                "data": videos,
                "status_code": status.HTTP_200_OK,
                "message": "success",
                "error": None,
                "total_pages": total_pages,
                "current_page": offset // limit + 1,
            }
        except Exception as e:
            return {
                "data": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "failed",
                "error": str(e),
            }

    def video_detail(self, id):
        try:
            # Query the video object by id
            obj = self.db.query(Video).filter(Video.id == id).first()
            if not obj:
                # Return error response if video object is not found
                return {
                    "data": None,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "obj not found",
                    "error": None,
                }
            else:
                # Return success response with the video object
                return {
                    "data": obj,
                    "status_code": status.HTTP_200_OK,
                    "message": "success",
                    "error": None,
                }
        except Exception as e:
            # Return error response if an exception occurs
            return {
                "data": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "failed",
                "error": str(e),
            }

    def delete_video(self, id):
        try:
            # Query the video object by id
            obj = self.db.query(Video).filter_by(id=id).first()
            if not obj:
                # Return error response if video object is not found
                return {
                    "data": None,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "obj not found",
                    "error": None,
                }

            # Delete the video object from the database
            self.db.delete(obj)
            self.db.commit()

            # Return success response with the deleted video object
            return {
                "data": obj,
                "status_code": status.HTTP_200_OK,
                "message": "success",
                "error": None,
            }
        except Exception as e:
            # Return error response if an exception occurs
            return {
                "data": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "failed",
                "error": str(e),
            }

    def edit_video(self, id, video_form, video_contents):
        try:
            # Query the video object by id
            obj = self.db.query(Video).filter_by(id=id).first()
            if not obj:
                # Return error response if video object is not found
                return {
                    "data": None,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Video ID not found",
                    "error": None,
                }

            if video_contents:
                file_path = video_form["video"].filename
                video_path = os.path.join(VIDEO_CONTENT_PATH, file_path)

                if video_form["video"]:
                    # Save the new video file
                    with open(video_path, "wb") as vid:
                        vid.write(video_contents)
                    try:
                        # Calculate the new video duration using VideoFileClip
                        clip = VideoFileClip(video_path)
                        duration = int(clip.duration)
                        clip.close()
                    except Exception as e:
                        duration = 0  # Set default duration if an error occurs

                    # Update video_path and duration if video file is provided
                    obj.video_file = video_path
                    obj.duration = duration
                else:
                    # No new video file provided, retain the existing video file and duration
                    video_path = obj.video_file
                    duration = obj.duration

            # Update the video object with new values
            if video_form.get("title"):
                obj.title = video_form.get("title").lower()
            if video_form.get("description"):
                obj.description = video_form.get("description")

            self.db.commit()
            self.db.refresh(obj)

            # Return success response with the updated video object
            return {
                "data": obj,
                "status_code": status.HTTP_200_OK,
                "message": "success",
                "error": None,
            }
        except Exception as e:
            # Return error response if an exception occurs
            return {
                "data": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "failed",
                "error": str(e),
            }
