from pydantic import BaseModel, Field


class OrderLineItem(BaseModel):
    company: str = Field(default="Unknown", description="Name of the company")
    article_number: str = Field(default="", description="Article number of the item")
    name: str = Field(default="", description="Name of the item")
    description: str = Field(default="", description="Description of the item")
    quantity: int = Field(default=1, description="Number of items ordered")
    unit_of_measure: str = Field(default="", description="Unit of measure of the item")
    unit_price: float = Field(default=0.0, description="Price per unit of the item")
    discount: float = Field(default=0.0, description="Discount percentage on the item")
    price: float = Field(default=0.0, description="Total price of the item")
    currency: str = Field(default="EUR", description="Currency of the item")





