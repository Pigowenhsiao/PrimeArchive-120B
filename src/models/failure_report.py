from dataclasses import dataclass


ALLOWED_ERROR_TYPES = {"timeout", "transient", "format", "unknown"}


@dataclass(frozen=True)
class FailureReport:
    report_id: str
    book_id: str
    stage: str
    error_type: str
    retries: int
    status: str
    sample_reference: str

    def __post_init__(self) -> None:
        if self.error_type not in ALLOWED_ERROR_TYPES:
            raise ValueError(f"Invalid error type: {self.error_type}")
