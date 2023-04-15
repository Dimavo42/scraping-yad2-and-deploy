from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import app_functions as local_db

app = FastAPI()


class ItemResponse(BaseModel):
    number_of_items: dict
    method: str


class ItemMaxMinResponse(BaseModel):
    item: dict
    method: str


@app.get("/")
async def get_root():
    return {"message": "Yad2 Json ", "method": "GET"}


@app.post("/")
async def post_root():
    return {"message": "Yad2 Json", "method": "POST"}


@app.get("/item")
async def get_item(
    number_items: Optional[int] = None,
    room_start: Optional[int] = None,
    room_end: Optional[int] = None,
    price_start: Optional[int] = None,
    price_end: Optional[int] = None,
    max_item: Optional[bool] = False,
    min_item: Optional[bool] = False,
):
    if number_items is not None:
        if not local_db.find_item(number_items):
            return {"message": "Item not found"}
        all_items = local_db.get_number_of_items(number_items)
        item_response = ItemResponse(number_of_items=all_items, method="GET")
        return item_response

    if room_start is not None and room_end is not None:
        items = local_db.get_between_start_end(room_start, room_end, "rooms")
        item_response = ItemResponse(number_of_items=items, method="GET")
        return item_response

    if price_start is not None and price_end is not None:
        items = local_db.get_between_start_end(price_start, price_end, "price")
        item_response = ItemResponse(number_of_items=items, method="GET")
        return item_response

    if max_item:
        item = local_db.get_maxuim_minium_price("max")
        item_response = ItemMaxMinResponse(item=item, method="GET")
        return item_response

    if min_item:
        item = local_db.get_maxuim_minium_price("min")
        item_response = ItemMaxMinResponse(item=item, method="GET")
        return item_response

    return {"message": "Invalid request", "method": "GET"}


@app.get("/item/{item_id}")
async def get_item(item_id: int):
    if not local_db.find_item(item_id):
        return {"message": "Item not found"}
    item = local_db.get_item(item_id)
    return {"item": item}


@app.post("/item/{item_id}")
async def update_item(item_id: int, updated_item: dict):
    if not local_db.find_item(item_id):
        return {"message": "Item not found"}
    local_db.update_item(item_id, updated_item)
    return {"message": "Updated"}