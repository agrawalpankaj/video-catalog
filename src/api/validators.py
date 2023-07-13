class FromValidator:
    @staticmethod
    def from_validator(payload, db):
        result, message = True, "failed"
        if payload["title"] == "":
            result, message = False, "Video Title is required"
        if payload["video"] == "":
            result, message = False, "Video Content is required"
        if payload["description"] == "":
            result, message = False, "Video Description is required"
        return result, message
