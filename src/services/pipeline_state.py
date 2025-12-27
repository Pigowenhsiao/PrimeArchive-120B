from dataclasses import dataclass, field
from typing import List

from src.models.failure_report import FailureReport


@dataclass
class PipelineState:
    book_id: str
    failures: List[FailureReport] = field(default_factory=list)

    def record_failure(
        self,
        report_id: str,
        stage: str,
        error_type: str,
        retries: int,
        status: str,
        sample_reference: str,
    ) -> None:
        report = FailureReport(
            report_id=report_id,
            book_id=self.book_id,
            stage=stage,
            error_type=error_type,
            retries=retries,
            status=status,
            sample_reference=sample_reference,
        )
        self.failures.append(report)


def should_retry(error_type: str) -> bool:
    return error_type in {"timeout", "transient"}
