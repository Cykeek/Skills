# Design Thinking & Process — Deep Reference

This is the deep reference for design methodologies, frameworks, innovation techniques, and design process. Read this when working on strategy, problem definition, framing, process selection, or design methodology.

---

## 1. The Double Diamond (Design Council, 2005/2019)

The Double Diamond maps the design process as alternating divergent (broadening) and convergent (narrowing) phases.

### Phase 1: Discover (Divergent)
Research and understand. Explore the problem space widely without premature judgment.

**Methods**: User interviews, contextual inquiry, diary studies, competitive analysis, market research, trend analysis, stakeholder interviews.

**Output**: Research findings, user needs, pain points, opportunities, design principles.

**Mindset**: Curiosity, openness, embracing ambiguity. *"We don't know what we don't know."*

### Phase 2: Define (Convergent)
Synthesize research findings into a clear problem definition.

**Methods**: Affinity mapping, journey mapping, empathy mapping, problem statement, HMW questions, design principles.

**Output**: Problem statement, HMW questions, design criteria, scope definition, project brief.

**Mindset**: Synthesis, clarity, focus. *"What is the specific problem we're solving?"*

### Phase 3: Develop (Divergent)
Generate and test potential solutions. Explore multiple approaches.

**Methods**: Brainstorming, sketching, wireframing, concept development, prototyping, co-creation, design sprints.

**Output**: Multiple concepts, low-fidelity prototypes, test results.

**Mindset**: Ideation, experimentation, volume of ideas. *"Many ideas, cheap tests."*

### Phase 4: Deliver (Convergent)
Finalize and ship. Refine the chosen solution and prepare for implementation.

**Methods**: High-fidelity prototyping, user testing, final design, design system alignment, handoff, QA.

**Output**: Final design, design spec, handoff assets, launch plan.

**Mindset**: Refinement, execution, craftsmanship. *"Ship and iterate."*

---

## 2. Design Sprint (Google Ventures)

5-day process to compress months of work into a week. Best for high-stakes decisions, new product directions, or breaking through stalled projects.

### The 5-Day Sprint

| Day | Phase | Activities | Outputs |
|---|---|---|---|
| **Mon** | Understand & Map | Expert interviews, HMWs, user journey mapping, long-term goal, sprint questions | Journey map, sprint questions, target area |
| **Tue** | Diverge & Sketch | Lightning demos, crazy 8s, solution sketches (4-step: notes, ideas, crazy 8s, solution sketch) | Individual solution sketches |
| **Wed** | Decide | Art museum gallery walk, heat map, sticky decision, storyboarding | Chosen concept, step-by-step storyboard |
| **Thu** | Prototype | "Fake it" prototyping — enough realism for testing, not production quality | Clickable prototype |
| **Fri** | Test | 5 user interviews with prototype, observe patterns, iterate or validate | Test findings, go/no-go decision |

### Sprint Prerequisites
- **One decision-maker** who can say yes/no on the spot
- **Cross-functional team** (design, product, engineering, research)
- **Clear challenge** (not too broad or too narrow)
- **5 consecutive days** (compressed time is a feature, not a bug)
- **No distractions** (no email, meetings, Slack during sprint week)

### When to Sprint

✅ **Good for**:
- Major redesign or new feature direction
- High-stakes decision with significant uncertainty
- Team is stuck or disagreeing on direction
- You need user feedback before committing to development

❌ **Not for**:
- Problems that need deep technical investigation
- Very well-understood problems with clear solutions
- When you can't get real users for Friday's test

---

## 3. Shape Up (Basecamp / Ryan Singer)

A product development methodology designed for fixed-time, variable-scope work.

### Key Concepts

**Appetite**: Set a time budget first (e.g., "6 weeks"), then figure out what can be built in that time. This is the opposite of estimating.
- Small batch: 2 weeks (for a single feature)
- Standard batch: 6 weeks (for a significant feature or improvement)
- Big batch: Use cycles for large initiatives

**Shaping**: Define the problem, scope, solution approach, and boundaries before design starts. Shape to the "fat marker sketch" level — enough to know what we're building but not so detailed that the team has no room for creativity.

**Shaping outputs**:
- **Problem**: Appetite + problem statement
- **Appetite**: Time budget (how much time is this worth?)
- **Solution**: Fat-marker sketch — the key elements of the solution
- **Rabbit holes**: What to avoid, what's out of scope
- **No-gos**: The boundaries and constraints

**Betting**: The decision to invest a cycle's time into a shaped pitch.

**Building**: The team has full ownership during the build. Scope is variable — they cut down to fit the appetite. No interruptions (no mid-cycle changes, no "by the way" features).

**Cooldown**: 2 weeks between 6-week cycles for bug fixes, small improvements, exploration, and learning.

---

## 4. Lean UX (Jeff Gothelf)

A approach to UX design that emphasizes outcomes over outputs, cross-functional collaboration, and continuous learning.

### Principles

1. **Cross-functional teams**: Design, product, engineering work together throughout the process
2. **Outcomes over outputs**: Success is measured by user behavior change, not features shipped
3. **Shared understanding**: Build collective knowledge through conversation and low-fidelity artifacts
4. **Minimum documentation**: Create only what's needed to move forward. Heavy specs don't survive contact with development
5. **Continuous discovery**: Research is ongoing, not a phase. Always learning from users
6. **MVP as learning tool**: The smallest thing you can build to learn the most. Not the cheapest feature set — the fastest learning loop

### The Lean UX Cycle

```
Think                ─→     Make                ─→     Check
(assumptions,        →    (prototypes,          →    (test with users,
hypotheses)               experiments)                measure, learn)

↑_____________________________________________________________↓
                     Learn → iterate or pivot
```

### MVP (Minimum Viable Product) Mindset

**Definition**: The smallest thing you can build to test your riskiest assumption.

**Approach**:
1. List assumptions
2. Identify the riskiest assumption (the one that, if wrong, makes everything else pointless)
3. Design the smallest experiment to test that assumption
4. Build just enough to run the experiment
5. Measure, learn, decide (iterate or pivot)

**MVP is not**:
- A crappy version of your vision
- The first version of your product
- An excuse to ship low-quality work
- Something you do once and then abandon

---

## 5. Jobs-to-Be-Done Framework (Clayton Christensen / Bob Moesta / Tony Ulwick)

JTBD focuses on the *progress* the user is trying to make, not the product they're buying.

### Core JTBD Concepts

**Job**: The progress a person is trying to make in a particular situation.

**Functional job**: The practical task (e.g., "get from one place to another")
**Emotional job**: How the person wants to feel (e.g., "feel in control of my time")
**Social job**: How they want to be perceived (e.g., "be seen as a responsible parent")

**The Forces of Progress** (what drives a switch):
```
Push (Current frustration)          Pull (Attraction of new)
    ↓                                    ↓
    →→→→→→→ [USER] ←←←←←←←
    ↑                                    ↑
Anxiety (Fear of switching)          Habit (Inertia of current)
```

### JTBD Interview Method

Focus on past transitions:
1. **The trigger**: What happened that made you start looking for a solution?
2. **The search**: What options did you consider? Why did you reject some?
3. **The criteria**: What was most important in your decision?
4. **The anxieties**: What were you worried about when making the switch?
5. **The outcome**: How did it work out? What still isn't ideal?

### Outcome-Driven Innovation (ODI)

Tony Ulwick's approach: define the job, then identify the desired outcomes (metrics customers use to measure success).

**Formula for desired outcomes**: "Minimize [metric the user cares about]" or "Increase [desired outcome]"

Examples:
- "Minimize the time it takes to find a product"
- "Increase the likelihood of finding exactly what I'm looking for"
- "Minimize the effort required to complete checkout"

---

## 6. Problem Framing

The most important skill in design is framing the right problem.

### The Problem Statement Format

**Format**: [User type] needs [need/goal] because [insight], but [barrier].

**Example**: "Busy professionals need to track their expenses automatically because manual tracking is tedious and error-prone, but existing solutions require too much manual work and don't integrate with their bank."

### Question Ladder (ascending in specificity)

| Level | Question |
|---|---|
| **Problem area** | "How might we improve financial health?" |
| **Problem scope** | "How might we help people save money?" |
| **Problem statement** | "How might we automate expense tracking so people don't have to remember every transaction?" |
| **Solution question** | "How might we build a bank-integrated auto-categorization expense tracker?" |
| **Implementation** | "How should we design the bank connection flow?" |

*Move down the ladder only when you've validated the level above. Most design mistakes come from jumping straight to implementation questions.*

---

## 7. Ideation Methods

### Brainstorming Rules (IDEO)

1. Defer judgment (no "but", "that won't work", "we tried that")
2. Encourage wild ideas (they lead to practical ones)
3. Build on the ideas of others ("yes and...")
4. Go for quantity (50 ideas per session)
5. One conversation at a time
6. Stay focused on the topic
7. Be visual (sketch, diagram, write on board)

### Crazy 8s (Design Sprint)

Fold a paper into 8 sections. Sketch 8 different ideas in 8 minutes (1 minute per sketch). Forces quick ideation without overthinking.

### How Might We (HMW)

Convert problem statements into opportunity questions:

**Problem**: "Users don't know how much they're spending on subscriptions."
**HMW**: "HMW make subscription costs visible with zero effort?"

**HMW formula**: "How might we [desired outcome] [constraint or opportunity]?"

### Round Robin / SCAMPER

| Technique | Question starters |
|---|---|
| **Substitute** | What can we replace? |
| **Combine** | What can we combine? |
| **Adapt** | How can we adapt an existing solution? |
| **Modify/Magnify** | What can we change or emphasize? |
| **Put to other use** | What else can this be used for? |
| **Eliminate** | What can we remove? |
| **Reverse/Rearrange** | What if we reversed it? |

---

## When to Read This File

Read `design-thinking.md` when:
- Planning a project and deciding which methodology to use
- Framing problems and writing problem statements
- Running ideation sessions or design sprints
- Adopting new design processes (Shape Up, Lean UX, JTBD)
- Teaching or presenting design methodology
- Breaking through a creative block or team disagreement

**Document reference**: Design methodologies, problem framing, ideation techniques, innovation processes
**Last updated**: July 2026
