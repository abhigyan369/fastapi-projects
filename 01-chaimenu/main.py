from fastapi import FastAPI, Query, HTTPException
from models import MenuItem, MenuResponse
from data import menu_items


app = FastAPI(
    title="Chai Point Menu API",
    description="Read only menu API for kiosk and mobile devices",
)

@app.get("/")
def root():
    return {"message": "welcome to chai point menu api"}

# /menu -> path
# /menu/category=chai&available=true

@app.get("/menu", response_model=MenuResponse)
def get_menu(
    category: str | None = Query(None, description="filter by chai, coffee, snacks, main course"),
    available: bool | None = Query(None, description="filter by availability"),
):
    items = menu_items
    if category:
        items = [item for item in items if item["category"] == category.strip().lower()]
        if not items:
            raise HTTPException(status_code=404, detail=f"No items found for category: {category}")
    if available is not None:
        items = [item for item in items if item["available"] is available]
    return MenuResponse(count=len(items), items=[MenuItem.model_validate(item) for item in items])


@app.get("/menu/{item_id}", response_model=MenuItem)
def get_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return MenuItem.model_validate(item)
    raise HTTPException(status_code=404, detail=f"No item found with id: {item_id}")
