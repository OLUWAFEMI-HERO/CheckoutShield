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