"""
Stub data for testing individual steps of the system design practice tool.
Each step's stub data is a function that returns the minimum required data for that step.
"""

def get_step1_stub():
    """Stub data for Requirements Step (Step 1)"""
    return {
        "question": "Design a distributed system",
        "requirements": {
            "functional": [
                "User authentication",
                "Data storage",
                "Real-time updates"
            ],
            "nonfunctional": [
                "High availability",
                "Low latency",
                "Data consistency"
            ]
        }
    }

def get_step2_stub():
    """Stub data for API Design Step (Step 2)"""
    return {
        **get_step1_stub(),
        "apis": {
            "internal": [
                {
                    "endpoint": "POST /auth",
                    "request": ["username", "password"],
                    "response": ["token"]
                }
            ],
            "external": [
                {
                    "endpoint": "GET /data",
                    "request": ["id"],
                    "response": ["data"]
                }
            ]
        }
    }

def get_step3_stub():
    """Stub data for Workflow Design Step (Step 3)"""
    return {
        **get_step2_stub(),
        "workflows": [
            {
                "api": "POST /auth",
                "requirement": "User authentication",
                "steps": [
                    {
                        "step": "Auth Service",
                        "substeps": ["Validate credentials", "Generate token"]
                    },
                    {
                        "step": "Database",
                        "substeps": ["Store session", "Update last login"]
                    }
                ]
            },
            {
                "api": "GET /data",
                "requirement": "Data storage",
                "steps": [
                    {
                        "step": "Load Balancer",
                        "substeps": ["Route request", "Check health"]
                    },
                    {
                        "step": "Application Server",
                        "substeps": ["Process request", "Format response"]
                    },
                    {
                        "step": "Cache",
                        "substeps": ["Check cache", "Update cache"]
                    },
                    {
                        "step": "Database",
                        "substeps": ["Query data", "Return results"]
                    }
                ]
            }
        ]
    }

def get_step4_stub():
    """Stub data for Architecture Diagramming Step (Step 4)"""
    return {
        **get_step3_stub(),
        "architecture": {
            "component_types": {
                "Auth Service": "Service",
                "Database": "Database",
                "Load Balancer": "Service",
                "Application Server": "Service",
                "Cache": "Cache"
            },
            "relationships": [
                {
                    "relationship": "Load Balancer -> Application Server",
                    "description": "HTTP request forwarding",
                    "protocol": "HTTP"
                },
                {
                    "relationship": "Application Server -> Cache",
                    "description": "Cache data access",
                    "protocol": "HTTP"
                },
                {
                    "relationship": "Application Server -> Database",
                    "description": "Data persistence",
                    "protocol": "HTTP"
                }
            ],
            "database_schema": [
                "Users: id:int, username:string, password_hash:string, last_login:timestamp",
                "Sessions: id:int, user_id:int, token:string, expires_at:timestamp"
            ]
        }
    }

def get_step5_stub():
    """Stub data for Optimization Step (Step 5)"""
    return {
        **get_step4_stub(),
        "optimizations": [
            "Component: Load Balancer",
            "  - Scalability: Horizontal scaling",
            "  - Efficiency: Load balancing",
            "Component: Application Server",
            "  - Scalability: Horizontal scaling",
            "  - Efficiency: Worker parallelism",
            "  - User Experience: Lazy load",
            "Component: Cache",
            "  - Consistency: Write-through cache",
            "  - Efficiency: Caching",
            "Component: Database",
            "  - Scalability: Read replica",
            "  - Efficiency: DB indexing",
            "  - Efficiency: DB connection pooler"
        ]
    }

def get_step6_stub():
    """Stub data for Edge Cases Step (Step 6)"""
    return {
        **get_step5_stub(),
        "optimizations": [
            "Component: Load Balancer",
            "  - Scalability: Horizontal scaling",
            "  - Efficiency: Load balancing",
            "Component: Cache",
            "  - Consistency: Write-through cache",
            "  - Efficiency: Caching"
        ]
    }

def get_complete_stub():
    """Complete stub data for all steps"""
    return get_step6_stub()

# Example usage:
if __name__ == "__main__":
    # Test a specific step
    from rich.console import Console
    console = Console()
    
    # Example: Test step 5
    from steps.optimization_step import OptimizationStep
    step5_data = get_step5_stub()
    step = OptimizationStep(console)
    result = step.execute(step5_data)
    
    # Print the result
    console.print("\n[bold]Result:[/bold]")
    console.print(result) 