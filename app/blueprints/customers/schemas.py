from app.extensions import ma
from app.models import Customers

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers
        # Creates a schema that validates the data as defined by Customer Model

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)