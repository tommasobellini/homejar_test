import uuid



# Custom Pydantic field to handle UUID representation
class UUIDField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return cls(str(uuid.UUID(value)))
        except ValueError:
            raise ValueError("Invalid UUID format")
