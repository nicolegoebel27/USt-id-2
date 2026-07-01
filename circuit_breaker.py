import time


class CircuitBreaker:

    def __init__(self):
        self.failures = 0
        self.open_until = 0

    def allow(self):
        return time.time() > self.open_until

    def fail(self):
        self.failures += 1
        if self.failures > 3:
            self.open_until = time.time() + 60
            self.failures = 0
