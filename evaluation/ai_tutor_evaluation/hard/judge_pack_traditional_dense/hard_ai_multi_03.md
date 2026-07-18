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
- - Policy
  - defines the agent’s behaviour at a given time
  - maps from perceptions to actions
  - can be defined by: look-up table, neural net, search algorithm...
  - may be stochastic

- Reward Function
  - defines the goal(s) in an RL problem
  - maps from states, state-action pairs, or state-action-successor state, triplets to a numerical reward
  - goal of the agent is to maximise the total reward in the long run
  - the policy is altered to achieve this goal
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources

## Tutor answer
# Trả lời

## (1) Agent function ánh xạ từ cái gì sang cái gì?

Theo tài liệu, **agent function ánh xạ từ lịch sử tri giác (percept histories) sang hành động (actions)**:

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

Trong đó:
- $\mathcal{P}^*$: tập tất cả các chuỗi tri giác (percept histories) mà agent có thể nhận được
- $\mathcal{A}$: tập các hành động (actions) mà agent có thể thực hiện

Nói cách khác, với mỗi lịch sử tri giác đã quan sát được, agent function quyết định agent nên thực hiện hành động nào.

## (2) Sự khác nhau giữa Agent và Environment

Dựa trên tài liệu, có thể phân biệt như sau:

| **Agent** | **Environment** |
|-----------|-----------------|
| Là thực thể **cảm nhận** và **hành động** | Là những gì **bị** cảm nhận và **bị tác động** lên |
| Có **sensors** (cảm biến) — ví dụ: mắt, tai, camera | Cung cấp **percepts** cho agent thông qua sensors |
| Có **actuators** (bộ truyền động) — ví dụ: tay, chân, motor | Nhận **actions** từ agent thông qua actuators |

**Mối quan hệ tương tác** giữa chúng:
- Environment → gửi **percepts** → đến Sensors của Agent
- Agent → gửi **actions** (qua Actuators) → tác động lên Environment

**Ví dụ minh họa** (từ tài liệu):
- Agent người: sensors là mắt, tai; actuators là tay, chân, miệng
- Agent robot (ví dụ Aishimo): sensors là camera, cảm biến hồng ngoại; actuators là các motor

Tóm lại, **agent** là chủ thể chủ động với khả năng cảm nhận–hành động, còn **environment** là đối tượng bị tác động và cung cấp thông tin phản hồi cho agent. Agent và environment tạo thành một vòng tương tác liên tục: environment → percepts → agent → actions → environment.

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
