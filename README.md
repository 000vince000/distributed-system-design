# distributed-system-design
## goal
To practice a structured approach to solving system design problems, as such:
- use a step-by-step process to guide the flow
  1. requirement gathering
    1.1 functional
    1.2 nonfunctional
  2. api design
  3. workflow design 
    3.1 focus on happy path E2E flow
    3.2 identify major components, ie services
  4. architecture diagraming
    4.1 wire components together
    4.2 also identify minor components like database schema
    4.3 talk about implement choices with reason and trade-offs against alternatives
    4.4 database schema
    4.5 most importantly, ensure API→workflows→diagram is functionally complete
  5. optimization against nonfunctional requirements, e.g.:
    5.1 consideration of CAP theorem
    5.2 scalability
    5.3 efficiency
    5.4 resilience
        5.4.1 single point of failures
    5.5 user experience: responsiveness, feedback, lazyload, caching, etc
  6. edge cases & failure handling (adding depths)
    6.1 small 
        6.1.1 memory leak
        6.1.2 cache misses
        6.1.3 message loss
        6.1.4 race condition, deadlock
        6.1.5 cascading failure
        6.1.6 etc
    6.2 big
        6.2.1 3P API retries
        6.2.2 DDoS
        6.2.3 node goes down
        6.2.4 cluster goes down
        6.2.5 etc
- use a timer to record total duration, factored into final output for grading
- use a templated approach, ie prompting for workflows and components, prompting for considerations, options, and trade-offs
- based on workflows and components, generate a mermaid diagram (exportable to excalidraw)
- generate a final MD file in the end, for pasting into an external LLM for grading
