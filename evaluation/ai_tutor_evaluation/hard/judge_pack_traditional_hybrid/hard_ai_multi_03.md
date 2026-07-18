# hard_ai_multi_03

## Question
Cho tôi hai điều: (1) agent function ánh xạ từ cái gì sang cái gì, và (2) sự khác nhau giữa agent và environment. Trả lời cả hai ý.

## Ground truth
(1) Agent function ánh xạ từ chuỗi lịch sử tri giác (percept histories) sang hành động, ký hiệu P* → A. (2) Agent là thực thể tri giác (perceive) và hành động (act); environment là môi trường mà agent tri giác qua percepts và tác động vào bằng actions. Agent tương tác với environment qua vòng percept–action.

## Retrieved context (what the tutor saw)
- - An agent is an entity that perceives and acts
- An agent function maps from percept histories to actions:

$\mathcal{P}^* \rightarrow \mathcal{A}$

|  Agent |       | Environment  |
|  ------|       |--------------|
|  Percepts    |
|  <---------- 
|  Actions     |
|  ----------> 
|               |
|               |
|  Sensors|       | Actuators|

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- - The **agent function** maps from percept histories to actions: 
  - [Formula: agent function mapping]
- The **agent program** runs on the physical **architecture** to produce the agent function
  - agent = architecture + program

| Agent        | Environment |
|--------------|-------------|
| +-------------+  |             |
| |   Sensors   |<--+--Percepts            |
| +------+------+  |             |
|         |         |             |
|    +----+----+    |             |
|    |    ?    |    |             |
|    +----+----+    |             |
|         |         |             |
|  +------+------+  |             |
|  |  Actuators  |--+--+->Actions            |
|  +-------------+  |             |
- - An **agent** is anything that can be viewed as **perceiving** its **environment** through **sensors** and **acting** upon that environment through **actuators**
- Example 1: human agent
  - Sensors: eyes, ears, ...
  - Actuators: hands, legs, mouth, ...
- Example 2: robotic agent (e.g., Aishimo)
  - Sensors: camera, infrared range finders
  - Actuators: various motors
- **Function Reflex-Vacuum-Agent([position, state]) returns action**
If state = Dirty then return Suck
Else if position = A then return Right
Else if position = B then return Left
End Function

- Does the agent act reasonably?
- - **Static** (vs. dynamic): The environment is unchanged while an agent is deliberating.
- **Discrete** (vs. continuous): A limited number of distinct, clearly defined percepts and actions.
- **Single agent** (vs. multiagent): An agent operating by itself in an environment.
- ```text
function SIMPLE-PROBLEM-SOLVING-AGENT(percept) returns an action
    static: seq, an action sequence, initially empty
            state, some description of the current world state
            goal, a goal, initially null
            problem, a problem formulation

    state ← UPDATE-STATE(state, percept)
    if seq is empty then do
        goal ← FORMULATE-GOAL(state)
        problem ← FORMULATE-PROBLEM(state, goal)
        seq ← SEARCH(problem)
    action ← FIRST(seq)
    seq ← REST(seq)
    return action
```

[Diagram: This pseudocode shows a simple agent loop that maintains internal state, formulates a goal and problem when it has no planned actions, and then uses search to produce an action sequence. It matters because it illustrates how an agent can act deliberately rather than reacting only to the current percept.]
- - An **agent** is an entity that perceives and acts
- An agent function maps from percept histories to actions:

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

```text
+--------------------------- Agent ---------------------------+      +-------------+
|                                                             |      |             |
|  Sensors  <-- Percepts                                      |      | Environment |
|     |                                                       |      |             |
|     v                                                       |      |             |
|    [?]                                                      |      |             |
|     |                                                       |      |             |
|     v                                                       |      |             |
|  Actuators ---- Actions ----------------------------------> |      |             |
+-------------------------------------------------------------+      +-------------+
```
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources

## Tutor answer
Dựa trên tài liệu được cung cấp, tôi xin trả lời cả hai ý như sau:

## (1) Agent function ánh xạ từ cái gì sang cái gì?

**Agent function ánh xạ từ tập hợp các lịch sử tri giác (percept histories) sang hành động (actions).**

Công thức toán học được biểu diễn như sau:

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

Trong đó:
- $\mathcal{P}^*$ là tập tất cả các chuỗi/lịch sử tri giác mà agent có thể nhận được
- $\mathcal{A}$ là tập các hành động mà agent có thể thực hiện

Nói cách khác, với mỗi lịch sử tri giác đầu vào, agent function sẽ quyết định hành động tương ứng cần thực hiện. (Tham chiếu: chunk `34cb54f9-0fba-48a9-8d08-0adc7c35d235` và `796d1cc0-37d9-49ea-9d9e-5c3f0792167b`)

## (2) Sự khác nhau giữa Agent và Environment

| **Agent** | **Environment** |
|-----------|-----------------|
| Là thực thể **nhận thức** (perceive) môi trường thông qua **sensors** (cảm biến) | Là thực thể bị agent tác động lên |
| **Hành động** (act) lên môi trường thông qua **actuators** (bộ truyền động) | Cung cấp **percepts** (tri giác) cho agent |
| Chạy **agent program** trên một **architecture** vật lý | Không thuộc kiểm soát của agent |

**Mối quan hệ giữa chúng** được mô tả qua sơ đồ luồng tương tác:
- Environment → gửi **Percepts** → đến Sensors của Agent
- Agent → gửi **Actions** → qua Actuators đến Environment

**Ví dụ minh họa** (từ tài liệu):
- **Human agent**: sensors là mắt, tai,...; actuators là tay, chân, miệng,...
- **Robotic agent** (ví dụ: Aishimo): sensors là camera, cảm biến hồng ngoại; actuators là các loại động cơ khác nhau

(Tham chiếu: chunk `63a01df0-e3e5-4875-a02f-43bd12ac56a1`, `796d1cc0-37d9-49ea-9d9e-5c3f0792167b`, `e8d0cf8d-ad47-4bea-812a-b31c7a38de13`)

---

```json

## Citations
```json
[
  {
    "chunk_id": "34cb54f9-0fba-48a9-8d08-0adc7c35d235",
    "document_title": "lecture1_introduction.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Rational agents",
    "page_number": null,
    "chunk_order": 14,
    "excerpt": "- An agent is an entity that perceives and acts\n- An agent function maps from percept histories to actions:\n\n$\\mathcal{P}^* \\rightarrow \\mathcal{A}$\n\n|  Agent |       | Environment  |\n|  ------|      "
  },
  {
    "chunk_id": "796d1cc0-37d9-49ea-9d9e-5c3f0792167b",
    "document_title": "lecture2_agent.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Agents and environments (con't)",
    "page_number": null,
    "chunk_order": 3,
    "excerpt": "- The **agent function** maps from percept histories to actions: \n  - [Formula: agent function mapping]\n- The **agent program** runs on the physical **architecture** to produce the agent function\n  - "
  },
  {
    "chunk_id": "63a01df0-e3e5-4875-a02f-43bd12ac56a1",
    "document_title": "lecture2_agent.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Agents and environments",
    "page_number": null,
    "chunk_order": 2,
    "excerpt": "- An **agent** is anything that can be viewed as **perceiving** its **environment** through **sensors** and **acting** upon that environment through **actuators**\n- Example 1: human agent\n  - Sensors:"
  },
  {
    "chunk_id": "e8d0cf8d-ad47-4bea-812a-b31c7a38de13",
    "document_title": "it3160e_ai_introduction.pdf",
    "document_tier": "community",
    "document_subtype": "summary_note",
    "section_title": "Rational agents",
    "page_number": null,
    "chunk_order": 9,
    "excerpt": "- An **agent** is an entity that perceives and acts\n- An agent function maps from percept histories to actions:\n\n$$\\mathcal{P}^* \\rightarrow \\mathcal{A}$$\n\n```text\n+--------------------------- Agent -"
  }
]
```
