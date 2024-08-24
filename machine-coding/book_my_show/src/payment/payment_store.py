from typing import Dict, final, List, Optional
from uuid import UUID

from session.session import Session


class PaymentStore:

    __payments: Dict[UUID, Session] = dict()

    @classmethod
    def add_session(cls, session: Session) -> None:
        cls.__payments[session.get_session_id()] = session

    @classmethod
    def get_session(cls, session_id: UUID) -> Optional[Session]:
        print(cls.__payments)
        return cls.__payments.get(session_id, None)

    @classmethod
    def get_all_sessions(cls) -> List[Session]:
        return list(cls.__payments.values())

    @classmethod
    def pay(cls, session_id: UUID) -> bool:
        if cls.__payments.get(session_id, None) is None:
            raise Exception(f'Invalid Session Id: {session_id}')
        elif cls.__payments.get(session_id).is_expired():
            print(f'Session {session_id} Expired')
            return False
        else:
            cls.__payments.get(session_id).set_session_payload(session_payload={
                **cls.__payments.get(session_id).get_session_payload(),
                'payment': 'complete'
            })
            return True
