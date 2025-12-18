import uuid
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from apps.core.dtos.platform.v1 import events_pb2

def publish_application_created(application):
    event = events_pb2.ApplicationCreatedEvent(
        base=events_pb2.BaseEvent(
            event_id=str(uuid.uuid4()),
            type=events_pb2.EventType.APPLICATION_CREATED,
            occurred_at=Timestamp(seconds=int(datetime.utcnow().timestamp()))
        ),
        application_id=application.id,
        student_id=application.student_id,
        vacancy_id=application.vacancy_id
    )
    
    print(event)
