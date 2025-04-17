from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time
from typing import List, Tuple, Any



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
            if not (isinstance(slot, (list, tuple)) and len(slot) == 2):
                raise ValueError(f"Slot at index {i} must contain exactly 2 elements [start_time, end_time]")
            
            start_time, end_time = slot
            
            try:
                start = datetime.strptime(start_time, "%H:%M").time()
                end = datetime.strptime(end_time, "%H:%M").time()
            except ValueError:
                raise ValueError(f"Slot at index {i} contains invalid time format. Use 'HH:MM' format")
            
            if start >= end:
                raise ValueError(f"Slot at index {i}: start time ({start_time}) must be earlier than end time ({end_time})")
                
        return v
    