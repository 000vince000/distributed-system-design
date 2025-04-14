# distributed-system-design
## goal
To practice a structured approach to solving system design problems, as such:
- use a step-by-step process to guide the flow
  1. requirement gathering
     * functional
     * nonfunctional
  2. api design
     * internal
     * external
  4. workflow design
     * focus on happy path E2E flow
     * identify major components, ie services
  5. architecture diagraming
     * wire components together
     * also identify minor components like database schema
     * talk about implement choices with reason and trade-offs against alternatives
     * database schema
     * most importantly, ensure API→workflows→diagram is functionally complete
  6. optimization against nonfunctional requirements, e.g.:
     * consideration of CAP theorem
     * scalability
     * efficiency
     * resilience
       * single point of failures
     * user experience: responsiveness, feedback, lazyload, caching, etc
  7. edge cases & failure handling (adding depths)
     * small 
       * memory leak
       * cache misses
       * message loss
       * race condition, deadlock
       * cascading failure
       * etc
     * big
       * 3P API retries
       * DDoS
       * node goes down
       * cluster goes down
       * etc
- use a timer to record total duration, factored into final output for grading
- use a templated approach, ie prompting for workflows and components, prompting for considerations, options, and trade-offs
- based on workflows and components, generate a mermaid diagram (exportable to excalidraw)
- generate a final MD file in the end, for pasting into an external LLM for grading
## Interface
simple terminal input and output
