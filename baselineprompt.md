To evaluate the effectiveness of the proposed U2F framework, we constructed three baseline prompting strategies for comparison.
 Each prompt was used to query the LLM under identical context conditions, using the same project description and requirement specification.

------

### **1. Zero-shot Prompt (ZSP)**

**Purpose:** Serves as the most basic baseline, testing the LLM’s spontaneous ability to identify potential “unknown unknowns” without explicit role or structure.

**Prompt Template (English):**

```
You are given a software project description and its current requirements.
Please identify potential "unknown unknowns"—factors or opportunities that are not explicitly mentioned
but could significantly change the system design, architecture, or user experience.
Explain why each identified factor was likely missing from the original requirements.
```

**Input Format Example:**

```
[Project Description]
A web-based collaboration platform with real-time document editing.

[Current Requirements]
- Implement user authentication and role-based access control.
- Provide document version history.
- Enable live editing and comments.

[Your Task]
Identify potential unknown unknowns (UUs).
```

------

### **2. Role-based Prompt (RBP)**

**Purpose:** Tests whether role assignment (e.g., system architect, domain expert) enhances discovery by invoking specialized reasoning.

**Prompt Template (English):**

```
You are acting as a senior software architect responsible for uncovering missing assumptions and hidden dependencies
that may affect long-term system scalability and innovation.
Based on the project description and requirements below, identify possible "unknown unknowns"—
concepts, constraints, or opportunities that are absent but could fundamentally reshape the system.
For each UU, explain:
1. Why it was overlooked.
2. How it could influence design or architecture.
```

**Input Format Example:**

```
[Role]
Senior Software Architect

[Project Description]
A web-based collaboration platform with real-time document editing.

[Requirements]
(As above)
```

------

### **3. Template-based Prompt (TBP)**

**Purpose:** Provides explicit structure to guide systematic reasoning while avoiding open-ended generation noise.
 It serves as a controlled prompt to evaluate structured reasoning versus exploratory reasoning.

**Prompt Template (English):**

```
Analyze the following project in four steps:
Step 1 — Identify any implicit assumptions in the given requirements.
Step 2 — Consider cross-domain or regulatory factors that may have been overlooked.
Step 3 — Suggest one or more potential "unknown unknowns" that could expand or constrain the solution space.
Step 4 — Justify each UU by explaining:
  - (a) Evidence of absence in the current documentation.
  - (b) How discovery could alter design decisions or enable new capabilities.
Return your answer in the following structured format:

[
  {
    "UU_Name": "",
    "Type": "(Cross-Domain / Regulatory / Technical / User-Context / Performance)",
    "Description": "",
    "Justification": ""
  }
]
```

**Input Example:**

```
[Project Description]
A web-based collaboration platform with real-time document editing.

[Requirements]
(As above)
```

>