from app.extensions import ma
from app.models import ServiceTickets

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        include_fk = True

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)