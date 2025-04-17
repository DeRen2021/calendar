from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time
from typing import List, Tuple, Any

class front_end_booking_request_type(BaseModel):
    msg:str

class booking_request_type(BaseModel):
    date: str
    start_time: str
    end_time: str
    name: str
    user_email: str
    reason: str
    format: str

class insert_avaliable_time_slot_type(BaseModel):
    date: str = Field(..., description="The date of the appointment in 'YYYY-MM-DD' format")
    slots: List = Field(
        ..., 
        description="List of time slots, each containing [start_time, end_time]",
        type="array",
        items={
            "type": "array",
            "items": {"type": "string"}
        }
    )

    @field_validator('date')
    def validate_date(cls, v):
        # 验证日期格式
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in 'YYYY-MM-DD' format")
        return v

    @field_validator('slots')
    def validate_slots(cls, v):
        if not isinstance(v, list):
            raise ValueError("Slots must be a list")
            
        
        for i, slot in enumerate(v):
            # 验证每个元素是否为包含两个元素的列表或元组
            if not (isinstance(slot, (list, tuple)) and len(slot) == 2):
                raise ValueError(f"Slot at index {i} must contain exactly 2 elements [start_time, end_time]")
            
            start_time, end_time = slot
            
            # 验证时间格式 (假设格式为 "HH:MM")
            try:
                start = datetime.strptime(start_time, "%H:%M").time()
                end = datetime.strptime(end_time, "%H:%M").time()
            except ValueError:
                raise ValueError(f"Slot at index {i} contains invalid time format. Use 'HH:MM' format")
            
            # 验证开始时间是否早于结束时间
            if start >= end:
                raise ValueError(f"Slot at index {i}: start time ({start_time}) must be earlier than end time ({end_time})")
                
        return v
    
    