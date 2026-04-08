from rest_framework.throttling import ScopedRateThrottle


class BurstRateThrottle(ScopedRateThrottle):
    scope = "burst"


class SustainedRateThrottle(ScopedRateThrottle):
    scope = "sustained"
