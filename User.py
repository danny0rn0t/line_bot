class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.past_user_inputs = []
        self.generated_responses = []
        self.max_record_len = 5
    def record_user_input(self, message: str):
        if len(self.past_user_inputs) >= self.max_record_len:
            self.past_user_inputs.pop(0)
        self.past_user_inputs.append(message)
    def record_responses(self, message: str):
        if len(self.generated_responses) >= self.max_record_len:
            self.generated_responses.pop(0)
        self.generated_responses.append(message)
    