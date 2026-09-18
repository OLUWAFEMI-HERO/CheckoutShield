import hashlib
import json


class IdempotencyService:

    @staticmethod
    def fingerprint(request: object) -> str:

        payload = json.dumps(
            request,
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()

import hashlib
import json
import time

from dataclasses import dataclass
from threading import Lock
from typing import Any


@dataclass(frozen=True, slots=True)
class IdempotentResult:
    fingerprint: str
    response: Any
    created_at: float