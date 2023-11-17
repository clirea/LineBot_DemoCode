class GptMessageModel:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def __str__(self):
        return f"role: {self.role}, content: {self.content}"

    def __repr__(self):
        return f"role: {self.role}, content: {self.content}"

    def to_json(self):
        return {
            "role": self.role,
            "content": self.content
        }