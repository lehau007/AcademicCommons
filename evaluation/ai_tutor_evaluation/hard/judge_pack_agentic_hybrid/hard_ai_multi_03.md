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
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- **Function** TABLE-DRIVEN-AGENT(percept) **returns** an action

- **static:** 
  - *percepts*, a sequence, initially empty
  - *table*, a table of actions, indexed by percept sequences, initially fully specified
- Append *percept* to the end of *percepts*
- *action* $\leftarrow$ LOOKUP(*percepts*, *table*)

**Return** *action*

- <span style="color:red">Drawback: huge table!</span>
- **Function** KB-AGENT(percept) **returns** an action

- static: KB, a knowledge base

t, a counter, initially 0, indicating time

- TELL(KB, MAKE-PERCEPT-SENTENCE(percept,t)
    - action ← ASK(KB, MAKE-ACTION- QUERY(^))
    - TELL(KB, MAKE-ACTION-SENTENCE(action,t) )
    - t ← t+1
    - return action

## Tutor answer
## 1. Agent function ánh xạ từ đâu sang đâu?

Theo tài liệu, **agent function** là một ánh xạ từ **lịch sử percept** (percept histories) sang **hành động** (actions):

$$f : \mathcal{P}^* \rightarrow \mathcal{A}$$

Trong đó:
- $\mathcal{P}^*$ — tập tất cả các chuỗi percept có thể (mọi lịch sử nhận thức mà agent đã thu nhận được từ trước đến nay).
- $\mathcal{A}$ — tập các hành động mà agent có thể thực hiện.

Nói cách khác, với **mọi lịch sử percept** mà agent quan sát được, hàm này cho biết agent nên **chọn hành động nào** để đưa ra.

> **Lưu ý phân biệt:** *Agent function* là khái niệm trừu tượng (toán học). *Agent program* mới là chương trình cụ thể chạy trên một *architecture* vật lý để hiện thực hóa agent function đó. Mối quan hệ: **agent = architecture + program**.

## 2. Sự khác nhau giữa Agent và Environment

| | **Agent** | **Environment** |
|---|---|---|
| **Định nghĩa** | Là **thực thể** (entity) **nhận thức** môi trường thông qua **sensors** và **tác động** lên môi trường thông qua **actuators**. | Là **phần thế giới bên ngoài** mà agent tương tác — cung cấp percepts cho agent và chịu tác động bởi actions của agent. |
| **Vai trò** | Chủ động: ra quyết định và hành động. | Bị động: phản hồi lại hành động, sinh ra percept mới. |
| **Giao tiếp** | Nhận **percepts** đi vào, gửi **actions** đi ra. | Nhận **actions** từ agent, gửi **percepts** cho agent. |
| **Ví dụ** | **Human agent:** sensors = mắt, tai…; actuators = tay, chân, miệng… **Robot Aishimo:** sensors = camera, cảm biến hồng ngoại; actuators = các motor. | Mặt đất, vật cản, thời tiết, đường đi, các xe khác… (đối với xe tự lái). |

### Mối quan hệ Agent ↔ Environment (theo sơ đồ)

```
   Agent                               Environment
+----------+                          +-----------+
| Sensors  | <------- Percepts ------|           |
+----------+                          |           |
|   [ ? ]  |                          |           |
+----------+                          |           |
| Actuators| ------- Actions ------> |           |
+----------+                          +-----------+
```

**Tóm lại:**
- **Agent** = bên *nhận thức và hành động* (có sensors + actuators + chương trình quyết định).
- **Environment** = bên *bị tác động* và *cung cấp thông tin* cho agent — mọi thứ nằm ngoài agent nhưng chịu ảnh hưởng từ hành động của nó.

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
  },
  {
    "chunk_id": "30300eec-d65c-472b-927a-37480bf0e42b",
    "document_title": "it3160e_ai_introduction.pdf",
    "document_tier": "community",
    "document_subtype": "summary_note",
    "section_title": "Rational agents",
    "page_number": null,
    "chunk_order": 10,
    "excerpt": "[Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is t"
  },
  {
    "chunk_id": "803a9519-9652-4953-bcc2-531222ef78d7",
    "document_title": "lecture2_agent.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Agent function based on conditional table",
    "page_number": null,
    "chunk_order": 4,
    "excerpt": "**Function** TABLE-DRIVEN-AGENT(percept) **returns** an action\n\n- **static:** \n  - *percepts*, a sequence, initially empty\n  - *table*, a table of actions, indexed by percept sequences, initially full"
  },
  {
    "chunk_id": "524b2f4b-08ad-426c-893b-278b35469f7b",
    "document_title": "lecture2_agent.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Knowledge-based agents",
    "page_number": null,
    "chunk_order": 22,
    "excerpt": "**Function** KB-AGENT(percept) **returns** an action\n\n- static: KB, a knowledge base\n\nt, a counter, initially 0, indicating time\n\n- TELL(KB, MAKE-PERCEPT-SENTENCE(percept,t)\n    - action ← ASK(KB, MAK"
  }
]
```
