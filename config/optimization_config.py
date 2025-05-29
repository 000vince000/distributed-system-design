# Optimization categories and their subcategories
OPTIMIZATION_OPTIONS = {
    "1": {
        "name": "Scalability",
        "options": {
            "1": "Vertical scaling",
            "2": "Horizontal scaling",
            "3": "Sharding",
            "4": "Async processing",
            "5": "Read replica",
            "6": "Loose coupling",
            "7": "Load shedding",
            "8": "Request coalescing",
            "9": "Other"
        }
    },
    "2": {
        "name": "Consistency",
        "options": {
            "1": "Quorum",
            "2": "Write-through cache",
            "3": "Distributed lock",
            "4": "ACID compliant storage",
            "5": "FIFO queue",
            "6": "Token leasing",
            "7": "Idempotent operations",
            "8": "Other"
        }
    },
    "3": {
        "name": "Efficiency",
        "options": {
            "1": "Transport data compression",
            "2": "Pre-upload transport data",
            "3": "CDN",
            "4": "Use UDP instead of TCP",
            "5": "Load balancing",
            "6": "Caching",
            "7": "Worker parallelism",
            "8": "DB indexing",
            "9": "NoSQL DB",
            "10": "DB read replica",
            "11": "DB connection pooler",
            "12": "DB materialized view",
            "13": "Other"
        }
    },
    "4": {
        "name": "User Experience",
        "options": {
            "1": "Client browser caching",
            "2": "Cookies",
            "3": "Lazy load",
            "4": "Realtime notification",
            "5": "Other"
        }
    },
    "5": {
        "name": "Reliability",
        "options": {
            "1": "Rate limits with backoff",
            "2": "Multiple availability zones",
            "3": "Service failure detection & auto failover",
            "4": "Circuit breaker",
            "5": "Message delivery failure recovery",
            "6": "Use different hash keys for cache and db",
            "7": "Use safe deployment practice",
            "8": "Replicate storage",
            "9": "Use bulkheads for resource isolation",
            "10": "Other"
        }
    }
}

# Mapping of non-functional requirements to categories
NFR_TO_CATEGORY = {
    # Scalability/Availability
    "scalability": "1",
    "high availability": "1",
    "availability": "1",
    "fault tolerance": "1",
    "resilience": "1",
    "reliability": "5",
    "disaster recovery": "5",
    "fault tolerance": "5",
    "resilience": "5",
    # Consistency
    "consistency": "2",
    "consistent": "2",
    "data consistency": "2",
    "strong consistency": "2",
    "eventual consistency": "2",
    "read-after-write consistency": "2",
    # Efficiency/Performance
    "efficiency": "3",
    "performance": "3",
    "low latency": "3",
    "throughput": "3",
    "resource utilization": "3",
    "cost efficiency": "3",
    # User Experience
    "user experience": "4",
    "ux": "4",
    "responsiveness": "4",
    "usability": "4",
    "realtime": "4"
} 