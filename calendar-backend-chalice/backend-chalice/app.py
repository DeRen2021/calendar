from chalice import Chalice, CORSConfig,NotFoundError,ConflictError,BadRequestError
from db_config import collection


# cors_config = CORSConfig(
#     allow_origin='https://example.com',
#     allow_headers=['Content-Type', 'Authorization'],
#     expose_headers=['X-Custom-Header'],
#     max_age=600,
#     allow_credentials=True
# )

# app.api.cors = cors_config

app = Chalice(app_name='backend-chalice')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/v1/get_available_slots/{date}', methods=['GET'])
def get_items(date):
    items = collection.find_one({"date": date})
    if items is None:
        raise NotFoundError("date is not valid")
    return {"available_slots": items["slots"]}

def time_to_int(time):
    try:
        return int(time.replace(":", ""))
    except:
        raise BadRequestError("time is not valid")

@app.route('/v1/book_slot', methods=['POST'])
def add_item():
    item = app.current_request.json_body
    date = item["date"]
    slot = item["slot"]
    #maybe add a check to see if date and slot is valid and if not rasie 400
    items = collection.find_one({"date": date})
    if items is None:
        raise NotFoundError("date is not valid")
    elif not items["slots"]:
        raise ConflictError("no available slots on this date")
    else:
        appointment_start = time_to_int(slot[0])
        appointment_end = time_to_int(slot[1])
        #check if the slot is available
        booked = False
        new_slots =[]
        for available_slot in items["slots"]:
            slot_start = time_to_int(available_slot[0])
            slot_end = time_to_int(available_slot[1])
            if appointment_start >= slot_start and appointment_end <= slot_end:
                booked = True
                if appointment_start == slot_start and appointment_end == slot_end:
                    continue
                elif appointment_start == slot_start:
                    new_slots.append([slot[1],available_slot[1]])
                elif appointment_end == slot_end:
                    new_slots.append([available_slot[0],slot[0]])
                else:
                    new_slots.append([available_slot[0],slot[0]])
                    new_slots.append([slot[1],available_slot[1]])
            else:
                new_slots.append(available_slot)
        
        if not booked:
            raise ConflictError("slot is not available")
        else:
            result = collection.update_one({"date": date}, {"$set": {"slots": new_slots}})
        

    return {'inserted_id': str(result.inserted_id)}


