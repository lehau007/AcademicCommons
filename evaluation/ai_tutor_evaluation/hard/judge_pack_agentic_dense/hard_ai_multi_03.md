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
- - Environment: **cooperative** or **competitive**
- Issue: the environment is not **static** → **synchronization**
- Require a model of the other agent's plans
- **Cooperation**: joint goals and plans, e.g., team planning in doubles tennis.
  - Joint goal: returning the ball that has been hit to them and ensuring that at least one of them is covering the net
  - Joint plan: multibody planning
  - Coordination mechanisms: decompose and distribute tasks
- **Competition**: e.g., chess-playing
  - An agent in a competitive environment must
    - recognize that there are other agents
    - compute some of the other agent's possible plans
    - compute how the other agent's plans interact with its own plans
    - decide on the best action in view of these interactions.
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources

## Tutor answer
# Trả lời

## (1) Agent function ánh xạ từ cái gì sang cái gì?

Theo tài liệu môn học, **agent function** là một ánh xạ từ **lịch sử tri giác (percept histories)** sang **hành động (actions)**, được ký hiệu toán học là:

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

Trong đó:
- $\mathcal{P}^*$ là tập tất cả các chuỗi tri giác (percept histories) mà agent có thể nhận được — tức là toàn bộ những gì agent đã "thấy/nghe/cảm nhận" được cho đến thời điểm hiện tại.
- $\mathcal{A}$ là tập các hành động mà agent có thể thực hiện.

Nói cách khác, với mỗi lịch sử tri giác đầu vào, agent function cho ra **một hành động** tương ứng.

> Lưu ý: Chính **agent program** chạy trên **architecture** (phần cứng) mới sinh ra agent function. Công thức: **agent = architecture + program**.

## (2) Sự khác nhau giữa Agent và Environment

Dựa trên định nghĩa trong bài giảng:

| | **Agent** | **Environment** |
|---|---|---|
| **Bản chất** | Là *thực thể* (entity) có khả năng tri giác và hành động | Là *thế giới bên ngoài* mà agent tương tác |
| **Vai trò** | Chủ thể thực hiện hành động | Đối tượng bị tác động và cung cấp thông tin |
| **Cơ chế tương tác với phía còn lại** | Dùng **sensors** (cảm biến) để nhận **percepts** từ environment, và dùng **actuators** (bộ truyền động) để gửi **actions** vào environment | Nhận actions từ agent, tạo ra các percept mới và cung cấp lại cho agent |
| **Ví dụ (human agent)** | Con người — sensors: mắt, tai; actuators: tay, chân, miệng | Thế giới vật lý xung quanh |
| **Ví dụ (robotic agent)** | Robot Aishimo — sensors: camera, cảm biến hồng ngoại; actuators: các động cơ | Môi trường mà robot hoạt động |

**Tóm gọn lại:** Agent là *bên quyết định và hành động* (thông qua agent function ánh xạ percept → action), còn Environment là *bên bị tri giác và bị tác động*. Agent và environment giao tiếp qua hai chiều: mũi tên percept đi **từ environment → agent** (qua sensors), và mũi tên action đi **từ agent → environment** (qua actuators).

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
    "chunk_id": "17b10140-d5bc-42c2-b508-6673c005a7c6",
    "document_title": "lecture2_agent.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Environment types",
    "page_number": null,
    "chunk_order": 14,
    "excerpt": "- **Static** (vs. dynamic): The environment is unchanged while an agent is deliberating.\n- **Discrete** (vs. continuous): A limited number of distinct, clearly defined percepts and actions.\n- **Single"
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
    "chunk_id": "fcbd419e-67d2-41a5-ad08-017147bd1fcd",
    "document_title": "lecture2_agent.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Multi-agent planning",
    "page_number": null,
    "chunk_order": 23,
    "excerpt": "- Environment: **cooperative** or **competitive**\n- Issue: the environment is not **static** → **synchronization**\n- Require a model of the other agent's plans\n- **Cooperation**: joint goals and plans"
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
  }
]
```
