from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.orm import Session

from database import get_db
from src.api.sevice import VideoCatalogService

router = APIRouter(
    prefix="/videocatalog",
    tags=["Video"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create/")
async def create_video(
    response: Response = None,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Create a new video in the video catalog.

    It extracts the video file from the request form, instantiates the VideoCatalogService,
    and calls the create_new_video method.

    """
    try:
        # Extract the video file from the request form
        video_form = await request.form()
        video = video_form.get("video")
        video_contents = None
        if video:
            video_contents = await video.read()

        # Instantiate the VideoCatalogService and call the create_new_video method
        video_service = VideoCatalogService(request, response, db)
        return video_service.create_new_video(video_form, video_contents)

    except Exception as e:
        # Return an error response if an exception occurs
        return {
            "data": None,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "failed",
            "error": str(e),
        }


@router.get("/list/")
async def get_video_list(
    response: Response = None,
    request: Request = None,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),  # Added a query parameter for the page number
    limit: int = Query(10, ge=1, le=100),  # Added a query parameter for the limit
):
    """
    Get a list of videos from the video catalog with pagination.
    """
    
    offset = (page - 1) * limit  # Calculate the offset based on the page number

    video_service = VideoCatalogService(response, request, db)
    return video_service.video_list(limit=limit, offset=offset)


@router.get("/detail/{id}")
async def get_video_detail(
    id: int,
    response: Response = None,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Get the details of a specific video from the video catalog.
    """
    video_service = VideoCatalogService(response, request, db)
    return video_service.video_detail(id)


@router.post("/delete/{id}/")
async def delete_video(
    id: int,
    response: Response = None,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Delete a video from the video catalog.
    """
    video_service = VideoCatalogService(response, request, db)
    return video_service.delete_video(id)


@router.post("/edit/{id}/")
async def update_video(
    id: int,
    response: Response = None,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Update a video in the video catalog.

    It extracts the video file from the request form, instantiates the VideoCatalogService,
    and calls the edit_video method.
    """
    # Extract the video file from the request form
    video_form = await request.form()
    video_contents = None
    if video_form.get("video"):
        video_content = video_form.get("video")
        video_contents = await video_content.read()

    # Instantiate the VideoCatalogService and call the edit_video method
    video_service = VideoCatalogService(response, request, db)
    return video_service.edit_video(id, video_form, video_contents)
