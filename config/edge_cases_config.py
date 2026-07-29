# Small scale failure scenarios
SMALL_SCALE_FAILURES = {
    "1": "Memory leak",
    "2": "Cache misses",
    "3": "Cache stampede / thundering herd",
    "4": "Message loss",
    "5": "Duplicate message delivery",
    "6": "Race condition",
    "7": "Deadlock",
    "8": "Cascading failure",
    "9": "Retry storm",
    "10": "Connection pool exhaustion",
    "11": "Hot key / hot partition",
    "12": "Other"
}

# Large scale failure scenarios
LARGE_SCALE_FAILURES = {
    "1": "3P API down",
    "2": "Service overwhelmed",
    "3": "DDoS",
    "4": "Node down",
    "5": "Cluster down",
    "6": "Region/AZ outage",
    "7": "Network partition (split-brain)",
    "8": "Database failover",
    "9": "Deployment failure",
    "10": "Certificate/credential expiry",
    "11": "Load balancer failure",
    "12": "Other"
} 