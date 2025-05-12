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
  3. workflow design
     * focus on happy path E2E flow
     * identify major components, ie services
  4. architecture diagraming
     * wire components together
     * also identify minor components like database schema
     * talk about implement choices with reason and trade-offs against alternatives
     * database schema
     * most importantly, ensure API→workflows→diagram is functionally complete
  5. optimization against nonfunctional requirements, e.g.:
     * consideration of CAP theorem
     * scalability
     * efficiency
     * resilience
       * single point of failures
     * user experience: responsiveness, feedback, lazyload, caching, etc
     * for each choice, talk about implement choices with reason and trade-offs against alternatives
  6. edge cases & failure handling (adding depths)
     * edge cases
     * small scale failures
       * memory leak
       * cache misses
       * message loss
       * race condition, deadlock
       * cascading failure       
     * large scale failures
       * 3P API down
       * service overwhelmed
       * DDoS
       * node goes down
       * cluster goes down
       * deployment failure
- use a timer to record total duration, factored into final output for grading
- use a templated approach, ie prompting for workflows and components, prompting for considerations, options, and trade-offs
- based on workflows and components, generate a mermaid diagram (exportable to excalidraw)
- generate a final MD file in the end, for pasting into an external LLM for grading

## Usage

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd distributed-system-design
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Tool

1. Start the system design practice tool:
```bash
python system_design_practice.py
```

2. Follow the interactive prompts:
   - Select a design question from the available options
   - Add functional and non-functional requirements
   - Design internal and external APIs
   - Define workflows (using the format: `ComponentA -> ComponentB: action`)
   - Identify system components
   - Add design optimizations
   - Identify edge cases (both small and big)

3. The tool will generate a markdown report with:
   - All your inputs organized by category
   - A mermaid diagram showing component relationships
   - Total time taken for the design session
   - The report will be saved as `design_reports/design_report_{question_name}_{timestamp}.md`

### Advanced Usage

#### Resuming Partial Designs
The tool automatically saves your progress after each step. You can resume from any saved point:

1. List available partial designs:
```bash
ls design_reports/partial_design_*
```

2. Resume from a partial design:
```bash
python system_design_practice.py --load-partial design_reports/partial_design_facebook_newsfeed_step2_20240321_143022.json
```

#### Using Stub Data
To practice specific steps using pre-defined data:
```bash
python system_design_practice.py --start-step 3
```
Note: When using stub data, partial designs are not saved.

### Workflow Format

When adding workflows, use the following format:
```
ComponentA -> ComponentB: action
```

Examples:
```
Client -> LoadBalancer: HTTP request
LoadBalancer -> WebServer: Forward request
Database -> Cache: Update cache
```

### Viewing the Report

The generated markdown report can be viewed in any markdown viewer that supports mermaid diagrams, such as:
- GitHub
- VS Code with Markdown Preview Enhanced extension
- Any other markdown viewer with mermaid support

## Interface
simple terminal input and output

## Flow
1. select a preset of design questions, eg design facebook newsfeed, design airbnb (P0)
2. prompt user for text inputs, allow multi-line input (P0)
3. incorporate previous input to formulate or add fidelity of the next step's prompt (P0)
4. based on mermaid generate visual graph (P1)
5. when all steps are complete, generate a MD report of original question, steps, diagram, and elapsed time
