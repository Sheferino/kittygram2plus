from datetime import datetime
from rest_framework import throttling


class WorkingHouseRateThrottle(throttling.BaseThrottle):
    # переопределяем метод, который решает, принять запрос или отклонить
    def allow_request(self, request, view):
        now = datetime.now().hour
        if now > 18:
            return False
        return True
