# Small scale failure scenarios
SMALL_SCALE_FAILURES = {
    "1": "Cache misses",
    "2": "Cache stampede / thundering herd",
    "3": "Message loss",
    "4": "Duplicate message delivery",
    "5": "Race condition",
    "6": "Deadlock",
    "7": "Cascading failure",
    "8": "Retry storm",
    "9": "Connection pool exhaustion",
    "10": "Hot key / hot partition",
    "11": "Other"
}

# Large scale failure scenarios
LARGE_SCALE_FAILURES = {
    "1": "3P API down",
    "2": "Service overwhelmed",
    "3": "Node down",
    "4": "Cluster down",
    "5": "Region/AZ outage",
    "6": "Network partition (split-brain)",
    "7": "Database failover",
    "8": "Deployment failure",
    "9": "Load balancer failure",
    "10": "Other"
}
