from typing import List
from datetime import datetime


class MembershipApplication:
    def __init__(self, applicant_id: int,
                 applicant_info: str | None = None,
                 acted_by: int | None = None,
                 decision_date: datetime | None = None,
                 admin_ids: List[int] | None = None) -> None:
        self.applicant_id = applicant_id
        self.applicant_info = applicant_info
        self.acted_by = acted_by
        self.decision_date = decision_date
        self.admin_ids = admin_ids if admin_ids is not None else []
