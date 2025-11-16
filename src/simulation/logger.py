class Logger:
    def __init__(self):
        self.time = []
        self.values = []

    def log_data(self, time: float, value: float):
        self.time.append(time)
        self.values.append(value)

    def get_results(self) -> dict:
        return {"time_s": self.time, "temperature": self.values}
