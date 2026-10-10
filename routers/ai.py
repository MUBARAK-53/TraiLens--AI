from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from services.gemma import analyze_image, verify_mission_discovery

router = APIRouter(prefix="/ai", tags=["AI Vision (Gemma)"])

@router.post("/analyze", status_code=status.HTTP_200_OK, summary="Analyze a trail photo with Gemma 2.5 Flash")
async def analyze_outdoor_image(
    latitude: float | None = Form(None),
    longitude: float | None = Form(None),
    image: UploadFile = File(...)
):
    """
    Upload an outdoor photo (plant, insect, or landmark) alongside GPS coordinates. 
    Gemma will check local weather, analyze the visual, and return observation details, 
    interesting facts, and a custom 5-minute screen-off mission.
    """
    try:
        image_bytes = await image.read()
        mime_type = image.content_type or "image/jpeg"
        
        # Call core gemma service with location support
        ai_response = await analyze_image(
            image_bytes=image_bytes, 
            mime_type=mime_type, 
            latitude=latitude, 
            longitude=longitude
        )
        return ai_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Vision Analysis Failed: {str(e)}"
        )


@router.post("/verify-mission", status_code=status.HTTP_200_OK, summary="Verify user's mission discovery photo")
async def verify_discovery(
    mission_title: str = Form(...),
    mission_instruction: str = Form(...),
    image: UploadFile = File(...)
):
    """
    After a 5-minute screen-off mission, the user can optionally upload a photo 
    of their discovery. Gemma will grade it, provide encouraging witty feedback, 
    and award gamified points.
    """
    try:
        image_bytes = await image.read()
        mime_type = image.content_type or "image/jpeg"

        verification_result = await verify_mission_discovery(
            mission_title=mission_title,
            mission_instruction=mission_instruction,
            image_bytes=image_bytes,
            mime_type=mime_type
        )
        return verification_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Mission Verification Failed: {str(e)}"
        )