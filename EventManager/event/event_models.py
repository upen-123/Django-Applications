from django.db import models
from EventManager.event.models import EventInfo, Users, BaseModel


class UserEventMapping(BaseModel):
    event_info = models.ForeignKey(EventInfo, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_index=True)
