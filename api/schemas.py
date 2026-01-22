from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int
    avg_views: float

    class Config:
        from_attributes = True

class TopProduct(BaseModel):
    product_name: str
    mention_count: int

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message_id: int
    channel_name: str
    date: datetime
    text: str
    views: int
    
    class Config:
        from_attributes = True

class VisualContentStats(BaseModel):
    channel_name: str
    image_count: int
    
    class Config:
        from_attributes = True

class DetectionResult(BaseModel):
    message_id: int
    image_path: str
    detected_objects: str
    
    class Config:
        from_attributes = True
