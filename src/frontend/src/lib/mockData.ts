export interface User {
  user_id: string;
  email: string;
  full_name: string;
  role: "admin" | "reviewer" | "student";
  note?: string;
}

export interface Course {
  course_code: string;
  name: string;
  description: string;
  topic_summary: string;
}

export type DocumentStatus = "PENDING" | "PROCESSING" | "APPROVED" | "REJECTED" | "FAILED";
export type DocumentTier = 1 | 2; // Tier 1: Official, Tier 2: Community

export interface Document {
  id: string;
  course_code: string;
  title: string;
  filename: string;
  uploaded_by: string;
  uploaded_at: string;
  status: DocumentStatus;
  tier: DocumentTier;
  file_type: "syllabus" | "textbook" | "lecture_slides" | "student_note" | "exam_prep";
  file_size_bytes: number;
  ocr_quality_score?: number;
  word_count?: number;
  markdown_content?: string;
  error_message?: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  citations?: { doc_id: string; page_number?: number; snippet: string }[];
}

export interface ChatSession {
  id: string;
  course_code: string;
  title: string;
  created_at: string;
}

export interface DLQJob {
  id: string;
  queue_name: "ocr_queue" | "eval_queue" | "index_queue";
  payload: {
    document_id: string;
    filename: string;
    course_code: string;
    attempts: number;
  };
  error_message: string;
  failed_at: string;
  ocr_trace?: {
    current_step: string;
    recent_events: { time: string; event: string }[];
  };
}

// 1. Mock Users
export const mockUsers: User[] = [
  {
    user_id: "admin-001",
    email: "admin@soict.hust.edu.vn",
    full_name: "System Admin",
    role: "admin"
  },
  {
    user_id: "reviewer-001",
    email: "reviewer.linhnt@soict.hust.edu.vn",
    full_name: "Nguyễn Thị Linh",
    role: "reviewer",
    note: "TA for IT3210, IT3292E"
  },
  {
    user_id: "reviewer-002",
    email: "reviewer.ducpv@soict.hust.edu.vn",
    full_name: "Phạm Văn Đức",
    role: "reviewer",
    note: "TA for IT3160E"
  },
  {
    user_id: "student-001",
    email: "student.anhnv@sis.hust.edu.vn",
    full_name: "Nguyễn Văn Anh",
    role: "student"
  },
  {
    user_id: "student-002",
    email: "student.huylt@sis.hust.edu.vn",
    full_name: "Lê Trung Huy",
    role: "student"
  },
  {
    user_id: "student-003",
    email: "student.maiptt@sis.hust.edu.vn",
    full_name: "Phạm Thị Thu Mai",
    role: "student"
  }
];

// 2. Mock Courses (Matching data/seed/courses.json exactly)
export const mockCourses: Course[] = [
  {
    course_code: "IT3210",
    name: "C Programming Language",
    description: "Học phần nhằm cung cấp cho sinh viên các kiến thức cơ bản về ngôn ngữ lập trình C bao gồm các khái niệm về giải thuật, chương trình, cấu trúc và cú pháp của chương trình C, các kiểu dữ liệu cơ sở và có cấu trúc, các cấu trúc điều khiển, các thao tác tính toán trên biểu thức và các thao tác vào ra dữ liệu.",
    topic_summary: "Giải thuật và chương trình; Cấu trúc và cú pháp chương trình C; Kiểu dữ liệu cơ sở (số, ký tự); Kiểu dữ liệu có cấu trúc (mảng, xâu, struct); Cấu trúc điều khiển (if, switch, for, while); Biểu thức và toán tử; Vào ra dữ liệu (stdin/stdout, file); Hàm và truyền tham số; Con trỏ; Quản lý bộ nhớ động"
  },
  {
    course_code: "IT3292E",
    name: "Database",
    description: "This course provides students with concepts related to database, database systems and its principles; data models with a focus on relational data model, database query languages; database design methods; database technologies such as storage and indexing, query processing, transaction management",
    topic_summary: "This course provides students with concepts related to databases, database systems, and their principles;data models with a focus on relational data model, database query languages; practical skills in using relational database management systems; database design methods; database technologies such as storage organization, indexing, query optimization, and data integrity. The course also provides teamwork, problem-solving, and practice skills through group discussion and presentation (during the class) and experimental work."
  },
  {
    course_code: "IT3160E",
    name: "Introduction to Artificial Intelligence",
    description: "This course will introduce the basic ideas and techniques of artificial intelligence: intelligent agents, search strategies, constraint satisfaction, logic and automatic proofing, knowledge representation, uncertain knowledge and reasoning, machine learning. By doing a capstone project at the end of this course, students will gain practical experience in building an AI system. In addition, students will practice necessary skills for future work such as teamwork skills, research skills, writing reports and presentations.",
    topic_summary: "This course will introduce the basic ideas and techniques of artificial intelligence: intelligent agents, problem solving, logic and automatic proofing, knowledge representation and inference. In addition, students are also introduced to some advanced concepts and techniques in artificial intelligence: machine learning. By doing a capstone project at the end of this course, students will gain practical experience in building an AI system. In addition, students will practice necessary skills for future work such as teamwork skills, research skills, writing reports and presentations."
  },
  {
    course_code: "IT3220",
    name: "C Programming (Introduction)",
    description: "The course provides students with methods to write and execute programs in C programming language on UNIX environment including basic grammar of C programming language and usage of functions in standard libraries,  techniques to create simple programs in C programming language. The course also equips students with the ability to understand basic topics in C via solving programing quizzes.",
    topic_summary: "Concepts of algorithm program; structure and syntax, keywords of C programs; primitive data types for numbers and characters, and structural data types for strings, arrays, and structures, control structures for branch, selection and iteration, expressions; data input/output from/to standard input/output and text files"
  },
  {
    course_code: "IT3020E",
    name: "Discrete Math",
    description: "The goal of this course is to introduce students to ideas and techniques from discrete mathematics that are widely used in computer science. This course teaches the students techniques in how to think logically and mathematically and apply these techniques in solving problems.  For instance, to specify computational problems precisely, one needs to abstract the detail and then use mathematical objects such as sets, functions, relations, orders and sequences; to prove that a proposed solution does work as specified, one need to apply the principles of mathematical logic, and to use proof techniques such as induction; and to reason about the efficiency of an algorithm, one often needs to count the size of complex mathematical objects. To achieve this goal, students will learn logic and proof, sets, functions, relations, graphs as well as algorithms and mathematical reasoning.",
    topic_summary: "Combinatorial theory: Counting problem, Existence problem, Enumerate problem, Combinatorial Optimization problem; Graph theory: Basic concepts of graph theory, Graph representation, Searching on graph, Minimum spanning Tree, Shortest path problem, Maximum flow problem"
  },
  {
    course_code: "IT4110E",
    name: "Scientific Computing",
    description: "This course helps students to grasp the basic concepts of scientific computing, common problems in science and engineering; methods and algorithms to solve complex problems in science and engineering. The course also helps students familiarize with the use of programming languages and tools to calculate as well as to develop software to solve complex problems in science and engineering.",
    topic_summary: "Calculating and programming using MATLAB; Error and condition of the problem; Numerical methods of algebra and calculus: Solving system of linear equations, Solving nonlinear equation, Approximation of derivative and integral, Numerical methods for differential equations, Curve fitting; Numerical methods for optimization: Non-linear programming, Linear programming; Matlab application in scientific computing."
  },
  {
    course_code: "IT3100E",
    name: "Object-Oriented Programming",
    description: "This course provides students with concepts, principles, methods, and techniques of Object-Oriented Programming (OOP) with the demonstration of the Java programming language. The course also provides students with such soft skills as team working and presentation, which are necessary for their future jobs.",
    topic_summary: "This course provides students with concepts, principles, methods, and techniques of Object-Oriented Programming (OOP) with the demonstration of the Java programming language. The course also provides students with such soft skills as team working and presentation, which are necessary for their future jobs. At the beginning of the course, the concept of object oriented technology, basics of Java programming, and Unified Modelling Language (UML) are introduced to students. They then get used to four object-oriented programming principles, i.e., abstraction, encapsulation, inheritance, and polymorphism. Next, object-oriented techniques including aggregation, composition, abstract class, interface, generic programming, exception handling, and graphical user interface (GUI) programming are respectively explained to students. They then practise designing software by means of UML diagrams. The last part of the course is for discussion to help students understand the context of the course in the big picture of the whole education program. This part also instructs students to apply their objected programming techniques in specific mini projects."
  },
  {
    course_code: "IT3312E",
    name: "Data Structures & Algorithms",
    description: "This course provides students basic knowledges about data structures and algorithms for the design and development of algorithms to solve computation problems. After the course, students will understand basic data structures likes linked lists, stacks queues, trees, binary search trees, hash tables and will be able to apply these data structures flexibly to different computation problems. Students also understand fundamental algorithmic paradigms such as recursion, greedy, divide-and-conquer, dynamic programming as well as different sorting algorithms and implement these algorithms to solve specific problems. Students will also be able to analyze the efficiency of algorithms in term of big-O notations.",
    topic_summary: "Basic concepts about data structures and algorithms; pseudo code for describing algorithms; time complexity analysis using big-O notation; recursion; backtracking; branch and bound; algorithmic paradigms with greedy, divide and conquer, dynamic programming; linked list, stack, queue, tree and binary tree, tree traversal; sorting algorithms with selection sort, insertion sort, bubble sort, merge sort, quick sort, heap sort; searching techniques with sequential search, binary search, binary search tree, red black tree, hash tables; graph data structures, graph traversal with depth-first search, breadth-first search, Kruskal algorithm implementation for finding minimum spanning tree with the disjoint set data structure, Dijkstra algorithm implementation for finding the shortest path from a source node to other nodes using the priority queue data structure. "
  },
  {
    course_code: "IT3230E",
    name: "Data Structures and Algorithms Basic Lab",
    description: "The course provide students skills to implement basic problem related to the course data structures and algorithms using the C programming language. After finishing the course, the students are able to implement fundamental data structures including linked lists, stacks, queues, trees, hash table as well as applying these data structures to computing applications. The students also have skill to design and implement recursive algorithms for solving combinatorial problems. Students can implement and experimentally compare the efficiency of different sorting algorithms.",
    topic_summary: "Array, dynamic array, struct, string, recursion, linked list, tree, sorting, searching with sequential search, binary search, binary search tree, hash table"
  },
  {
    course_code: "IT3420E",
    name: "Electronics for Information Technology",
    description: "This course provides students with fundamental knowledge of analog and digital electronics essential for Information Technology majors, serving as a solid foundation for understanding, analyzing, and designing computer systems, communication systems, embedded systems, and IoT. Students will work with basic electronic components (both passive and active), principles of electronic circuit analysis, Boolean algebra, combinational systems with logic circuit design principles, and sequential systems with state machine models. In addition, the course also equips students with practical skills such as using circuit simulation and design software, reading and interpreting technical design documents, and classifying and utilizing electronic components and devices.",
    topic_summary: "The contents of this course are divided into 2 parts: \n+ The analog electronics part includes basic concepts and technical parameters of passive and active electronic components, principles of some basic electronic circuits and systems related to computer engineering. \n+ The digital electronics part includes principles of Boolean algebra, combinational and sequential logic systems, principles of logic circuit design and finite state machines. In addition, this course also provides students with various skills in using circuit design and simulation softwares, reading datasheets and other technical documents, and knowing how to use electronic components and equipment. "
  },
  {
    course_code: "IT3170E",
    name: "Applied Algorithms",
    description: "The course will cover basics and enhancements in design, analysis and implementation of algorithms. Students will learn how to solve  competitive programming exercises on online judge systems and to solve real-life practical problems. The problems are described in the form of multidisciplinary applications such as on transportation, communication networks, bioinformatics, scheduling, artificial intelligence, data processing, .... In addition to mastering the basic knowledge of the algorithm, students will learn skills to implement and quickly implement different types of algorithms, different basic and advanced data structures. The course also provides students with access to a number of programming problems in job interviews of famous companies, a number of problems in the Olympic in informatics for students and International Collegiate Programming Contest (ICPC). This makes advantage for students in preparing to looking for opportunities to get a job in a famous company, even in abroad. Students will also have access to the best online judge systems in the world.",
    topic_summary: "Topics include: Data structure and basic algorithms libraries, Recursion and branch-and-bound techniques, Greedy algorithm, Divide and Conquer, Dynamic programming, Data structure and algorithm on graphs, Algoritms on strings, Introduction to NP-completeness. The topics are illustrated on practical application problems."
  },
  {
    course_code: "IT3280E",
    name: "Assembly Language and Computer Architecture Lab",
    description: "This is a hands-on course in Assembly Language Programming and Computer Architecture. The course helps students understand the interaction between hardware and software, the operation of a processor and a computer system via assembly code and a computer system simulator.",
    topic_summary: "Introduction of the simulator; Basic Instructions and Directives; Arithmetic and Logical operation; Load/ Store; Jump & Branch; Array and Pointer; Procedures and Stack; Cache memory; Peripherals and IO Programming; Interrupts;"
  },
  {
    course_code: "IT3070E",
    name: "Operating System",
    description: "This course aims to provide students with an understanding of the core concepts of modern operating systems; helps students understand and evaluate the algorithms used in the operating systems, so that they can be applied these algorithms in real problems. The course also introduces some basic system services (related to process, thread, memory, files...) of Windows/Linux operating systems, thereby the course helps students improve their concurrency programming and system- level programing skills. In addition, through the assignments and course projects, this course also helps students develop the necessary skills for future work such as document research, time management, teamwork, report writing, presentation…",
    topic_summary: "This module aims to provide students with an overview of the development of operating systems and basic knowledge of the principles of modern operating systems. This course consists of main sections: Overview of Operating systems; Process management (including topics related to processes and thread, CPU scheduling, process synchronization, deadlock); Memory management (linking, dynamic memory allocation, dynamic address translation, virtual memory) file management (storage devices management, directories, file system implementation) Input output system and System protection and security. In addition, through the assignments and course projects, this course also helps students develop the necessary skills for future work such as document research, time management, teamwork, report writing, presentation"
  },
  {
    course_code: "IT3283E",
    name: "Computer Architecture",
    description: "This course introduces instruction set architecture and computer organization, as well as the fundamental principles of computer design. The main topics include: computer structure and function, performance evaluation, RISC-V instruction set architecture and assembly programming, computer arithmetic, processor design, memory and I/O system organization, parallel architectures.",
    topic_summary: "The main contents of the course: Introduction to modern computers and  performance evaluation; Instruction set architecture and assembly language programming; Computer arithmetic; Organization of basic components in the computer systems: processors, memory, and input-output system; Parallel computer architectures."
  },
  {
    course_code: "IT4593E",
    name: "Introduction to Communication Engineering",
    description: "This course provides students with knowledge of communication engineering with an overview of digital communication systems and digital modulations. The course comprises two parts: The former of this course addresses an introduction to modern digital communication systems, including signal space, binary labeling, and transmitted waveform. Besides, students are nurtured by knowledge of decision theory, receiver architectures, and error probability estimation methods. Spectrum estimation, intersymbol interference, and the Nyquist criterion are also introduced in the first part. The latter of this course addresses digital modulation techniques, including PAM constellations, QAM constellations, line coding, linear modulation, and quadrature modulation.",
    topic_summary: "The course provides students with knowledge of communication engineering with an overview of digital communication systems and digital modulations. The course comprises two parts: The former of this course addresses an introduction to modern digital communication systems, including signal space, binary labeling, and transmitted waveform. Besides, students are nurtured by knowledge of decision theory, receiver architectures, and error probability estimation methods. Spectrum estimation, intersymbol interference, and the Nyquist criterion are also introduced in the first part. The latter of this course addresses digital modulation techniques, including PAM constellations, QAM constellations, line coding, linear modulation, and quadrature modulation."
  },
  {
    course_code: "IT3191E",
    name: "Machine Learning and Data Mining",
    description: "This course will provide the fundamental knowledge about Machine Learning (ML) and Data Mining (DM). It contains basic concepts, problems, and methods/models of ML/DM, as well as the methodology to work with data. Those methods/models can be implemented in different systems that can make prediction and discover new knowledge in real applications. The course also introduces some typical applications of ML and DM, and some useful libraries or frameworks. Beside, the course will enable the students to work in group, presentation skill, and the necessary attitude to work in the areas of ML and DM and in the future.",
    topic_summary: "This course will provide the fundamental knowledge about Machine Learning (ML) and Data Mining (DM). It contains basic concepts, problems, and methods/models of ML/DM, as well as the methodology to work with data. Those methods/models can be implemented in different systems that can make prediction and discover new knowledge in real applications. The course also introduces some typical applications of ML and DM, and some useful libraries or frameworks. Beside, the course will enable the students to work in group, presentation skill, and the necessary attitude to work in the areas of ML and DM and in the future."
  },
  {
    course_code: "IT3323E",
    name: "Compiler Construction",
    description: "This course is intended to provide a basic understanding of how  a compiler of a programming language  works. In addition,  after learning the course, students also have basic knowledge of language theory, especially the method for syntax and semantics  description. From there, students understand the principles of programming languages. With knowledge of this field, students will write programs in a more efficient way, and make it easier to learn new languages. Students also understand models language processing to apply to many other fields such as natural language processing, bioinformatics, structural recognition ...",
    topic_summary: "This course consists of main sections: language theory; the phases of a compiler; lexical analysis. Syntax analysis. Sematic analysis, code generation, code optimization. In the course project, the students were asked to complete a compiler for a simple programming language, thereby allowing students to work with important data structures and algorithms, to link them together to create a complete software."
  },
  {
    course_code: "IT4409E",
    name: "Web technologies and e- Services",
    description: "This course provides students with both foundational and advanced knowledge to design and develop web-based applications and online services. Upon completion, students will be able to: Proficiently use a programming language such as JavaScript, Java, or PHP to develop web applications in various domains, including content management systems (CMS), portals, and electronic applications (e-Commerce, e-Learning, e-Government, etc.). Gain a solid understanding of widely adopted web technologies, platforms, and frameworks. In addition, the course enhances students’ teamwork, presentation skills, and professional attitudes, providing a strong foundation for participating in projects or pursuing careers in software companies in the future.",
    topic_summary: "Internet, web, architecture of web application,  HTML, CSS, Javascript, PHP, JSP, Ajax, DOM, XML, SOA, website security, etc."
  },
  {
    course_code: "IT4549E",
    name: "ITSS Software Development",
    description: "The course provides students with knowledge and experiences on developing software in compliance with the ITSS industry standard. Students are able to grasp and apply object-oriented analysis and design, design principles, and construction practices to build a good software with loose coupling and tight cohesion. The students will learn, discuss, present and practice S.O.L.I.D principles with a case study in their teams. The course also shows the role of software construction and design with other courses related to software development process and object-oriented analysis and design methodology. Methods, techniques and tools of the following tasks will be covered: architectural design and detail design, code refactoring (with Eclipse), test-driven software development (with JUnit). Students are also given the overview of design patterns, some of the best practices adapted by experienced object-oriented software developers, which will be deeply studied in the engineer or master program.",
    topic_summary: "Introduction to Software Design and Construction. Architectural design. Detail design. Basic design Principles, Modularity, Coupling, Cohesion. Software coupling levels: Content, common, external, control, stamp, data, message. Software cohesion levels: Coincidental, logical, temporal, procedural, communicational, sequential, functional. Programming: Coding standard, code organization, framework, code refactoring, code management and integration (Git). Unit Testing. S.O.L.I.D design principles. Introduction to design patterns."
  },
  {
    course_code: "IT4082E",
    name: "Software Engineering",
    description: "This course introduces students to the main activities in the software development process, from requirements defining to implementing and operating a software in practice. The course covers the basic knowledge of software lifecycle, software development process, software models, software project management, software configuration and version management, software analysis and design, software construction and software quality assurance. Students will experience the software development process in practice from defining requirements, analysis and design, programming, testing, and software deployment through exercises and capstone project. In addition, this course also equips students with teamwork and presentation skills as well as attitudes needed for future works in software development companies.",
    topic_summary: "This course provides students with the main activities of the software life cycle processes beginning with defining requirements or needs of the customer, developing and deploying a software in a production environment and ending with the retirement of the software. The main activities include software development processes (i.e. software requirement engineering, software design and construction, software integration, software qualification testing), software delivery, operation and maintenance. The course introduces modern software development models (waterfall, prototype, iterative, agile), basic software project management, configuration and version management, and software quality assurance. Students will experience the software development process in practice from defining requirements, analysis and design, programming, testing, and software deployment through exercises and capstone projects. The course also provides students with such soft skills as team working and presentation, which are necessary for their future jobs."
  },
  {
    course_code: "IT3080E",
    name: "Computer Networks",
    description: "This course aims to provide students background  knowledge of computer network systems, data communication on the network environment, distributed environment, as a basis for designing, building and operating the network system. , IoT and data communications. Basic concepts about computer networks, OSI model and TCP/IP. Local area network, multiple access methods and local area network connection using Bridge, Switch, Hub. Inter-network connection using Internet Protocol (IP) and related issues (routing, addressing ...). TCP / UDP protocol and connection management process, sliding window mechanism, flow control, congestion control ... Popular applications on the Internet (Mail ...).",
    topic_summary: "This course aims to provide students the background knowledge of computer network systems, data communication on the network environment, distributed environment, as a basis for designing, building and operating the network system. , IoT and data communications. The contents of the course include: Basic concepts about computer networks, OSI model and TCP/IP. Local area network, multiple access methods and local area network connection using Bridge, Switch, Hub. Inter-network connection using Internet Protocol (IP) and related issues (routing, addressing ...). TCP / UDP protocol and connection management process, sliding window mechanism, flow control, congestion control ... Popular applications on the Internet (Mail ...)."
  },
  {
    course_code: "IT4441E",
    name: "User Interface and User Experience",
    description: "The User Interface and Experience course provides students with essential knowledge and skills to be able to design, implement and evaluate interfaces of interactive systems.",
    topic_summary: "The User Interface and Experience course provides students with essential knowledge and skills to be able to design, implement, and evaluate interfaces of interactive systems. This course provides the basic concepts of interfaces, interactions, human and computer elements in the process of interaction, usability, and user experience. The course introduces a user-centered design approach according to ISO 9241-210, an iterative design process for interface design and user experience design for interactive systems. This course focuses on principles, techniques, and tools that assist in designing interfaces, shaping the user experience according to the application requirements and communication requirements of different users. Through visual lectures and exercises, students are trained in design skills, creating interface prototypes, building interactive prototypes, measuring the usability of ISO 9241-11 standard, testing the organization of the content and the structure of the interfaces to create a good user experience. Besides, the course also focuses on training students in creative working skills, critical thinking, and the necessary attitude to self-study graphic design methods, prototype construction, interface evaluation for their future careers."
  },
  {
    course_code: "IT4542E",
    name: "Management of Software Development",
    description: "This course aims to provide students with the knowledge and skills to manage software development projects effectively.",
    topic_summary: "To help students have knowledge and skills: understanding the main features of Software Project management; master Software Project management process; Software Project management methods and techniques; grasp the key techniques for successful Software Project development; Planning (planing); Risk management; quality assurance; Change control and human resource management (humain resource management)."
  },
  {
    course_code: "IT4142E",
    name: "Introduction to Data Science",
    description: "This course introduces students to the field of Data Science, an interdisciplinary field of scientific methods, processes, and systems to extract knowledge from data. Methods from Data Science would support decision making and prediction. This course presents the key steps of data science processes, such as making assumption, data crawling, preprocessing, data analysis, knowledge evaluation, making prediction. Necessary methods from machine learning, data mining, and statistics will be introduced. The students will be introduced to how to work with texts, images, videos, graphs, social networks, ratings, feedbacks, … This course also introduces the typical applications in practice and useful tools and libraries.",
    topic_summary: "Overview, Web Crawling, Data Integration and preprocessing, Data Exploration, Data Visualization, Machine Learning, Big data management, Coputer vision, LinkAnalysis, Evaluation"
  },
  {
    course_code: "IT4785E",
    name: "Mobile Programming",
    description: "The course provides students with basic skills to develop an application on mobile platform. The main content focuses on Android framework (which is one of the most popular mobile platforms now) and surrounding technologies. Besides, this course also equips students with the ability to understand basic ideas and some skills to build up a multiplatform application. In addition, students will learn about teamwork and presentation skills.",
    topic_summary: "Chapter  1. Introduction about mobile programming, Chapter 2. Android application structure, Chapter 3. Android components, Chapter 4. Basic Gui programming, Chapter 5. Thread and Timer, Chapter 6. Notification and Activities communication, Chapter 7. Work with file system, Chapter 8. Background services, Chapter 9. Basic device sensors (optional), Chapter 10. Native programming, NDK, JNI"
  },
  {
    course_code: "IT4015E",
    name: "Introduction to Information Security",
    description: "Equip students with the basic knowledge of information security from the technical perspective of information system developers. Students grasp the overall picture of information security from two dimensions: from theoretical basis and from practice. Necessary technical knowledge about the basis: elementary cryptology, authentication problems, access control problems, network attacks.",
    topic_summary: "Overview: the basic concepts surrounding information assets, threats & attacks; the general goals of the security system; reflecting on the relationship between theoretical basis and practical solutions. Fundamentals of cryptography and basic security tools. Authentication problem and popular solutions. Access control problems and common access mechanisms. Overview of network security and common network attacks. This module provides a solid foundation for the next advanced courses on information security (IS) as well as supports the basis for self-study and self-training later (if students do not take more advanced courses on IS)"
  },
  {
    course_code: "IT4062E",
    name: "Network Programming",
    description: "This course focuses to build the network programming experiences. It starts from the review of computer network and C programming knowledge, then it covers the TCP and UDP application development techniques. The course gives practical and hands-on skills in designing and implementing TCP/IP networking applications in a Unix environment.",
    topic_summary: "Computer Network review, C/C++ programming review, SOCKET Introduction, Programming with TCP and UDP SOCKET, Multithreading programming, Basic and advanced I/O methods, Protocol designing and implementation, Course project"
  }
];

// 3. Mock Documents (PENDING, PROCESSING, APPROVED, FAILED, REJECTED)
export const mockDocuments: Document[] = [
  {
    id: "doc-001",
    course_code: "IT3210",
    title: "C Programming Syllabus 2026",
    filename: "it3210_syllabus_2026.pdf",
    uploaded_by: "student.anhnv@sis.hust.edu.vn",
    uploaded_at: "2026-06-15T08:30:00Z",
    status: "APPROVED",
    tier: 1,
    file_type: "syllabus",
    file_size_bytes: 1048576,
    ocr_quality_score: 0.98,
    word_count: 3200,
    markdown_content: "# Đề cương chi tiết học phần Lập trình C\n\n## 1. Thông tin chung\n- Mã học phần: IT3210\n- Khối lượng: 3(2-1-0-6)\n\n## 2. Mô tả học phần\nHọc phần cung cấp kiến thức lập trình cơ bản bằng ngôn ngữ C..."
  },
  {
    id: "doc-002",
    course_code: "IT3292E",
    title: "Database Lecture Slides - Chapter 3 Relational Model",
    filename: "db_lecture_ch3.pdf",
    uploaded_by: "reviewer.linhnt@soict.hust.edu.vn",
    uploaded_at: "2026-06-16T14:15:00Z",
    status: "APPROVED",
    tier: 1,
    file_type: "lecture_slides",
    file_size_bytes: 4194304,
    ocr_quality_score: 0.95,
    word_count: 1500,
    markdown_content: "# Chapter 3: Relational Model\n\n## Structure of Relational Databases\n- Relation schema: $R(A_1, A_2, \\dots, A_n)$\n- Relation instance: $r(R)$"
  },
  {
    id: "doc-003",
    course_code: "IT3160E",
    title: "Introduction to AI Midterm Cheat Sheet",
    filename: "ai_midterm_cheat_sheet.pdf",
    uploaded_by: "student.huylt@sis.hust.edu.vn",
    uploaded_at: "2026-06-17T09:00:00Z",
    status: "PROCESSING",
    tier: 2,
    file_type: "exam_prep",
    file_size_bytes: 2097152
  },
  {
    id: "doc-004",
    course_code: "IT3210",
    title: "Pointer Lab Guide",
    filename: "pointer_lab_guide.pdf",
    uploaded_by: "student.maiptt@sis.hust.edu.vn",
    uploaded_at: "2026-06-17T09:12:00Z",
    status: "PENDING",
    tier: 2,
    file_type: "student_note",
    file_size_bytes: 524288
  },
  {
    id: "doc-005",
    course_code: "IT3020E",
    title: "Discrete Math Course Note (Incomplete)",
    filename: "dm_note_corrupted.pdf",
    uploaded_by: "student.huylt@sis.hust.edu.vn",
    uploaded_at: "2026-06-17T07:45:00Z",
    status: "FAILED",
    tier: 2,
    file_type: "student_note",
    file_size_bytes: 153600,
    error_message: "OCR processing failed: Page 4 contains invalid PDF format elements and couldn't parse text."
  },
  {
    id: "doc-006",
    course_code: "IT3100E",
    title: "Object-Oriented Programming Exam Solution 2025",
    filename: "oop_exam_2025_solutions.pdf",
    uploaded_by: "student.anhnv@sis.hust.edu.vn",
    uploaded_at: "2026-06-16T11:00:00Z",
    status: "REJECTED",
    tier: 2,
    file_type: "exam_prep",
    file_size_bytes: 1258291,
    error_message: "Rejected by Subject Reviewer: Incorrect solutions to Question 4 and lack of markdown structure."
  }
];

// 4. Mock Tutor Chat Dialogues
export const mockChatSessions: ChatSession[] = [
  {
    id: "session-001",
    course_code: "IT3210",
    title: "Con trỏ trong lập trình C",
    created_at: "2026-06-17T09:30:00Z"
  },
  {
    id: "session-002",
    course_code: "IT3160E",
    title: "Giải thuật A* Search",
    created_at: "2026-06-17T09:40:00Z"
  }
];

export const mockChatMessages: ChatMessage[] = [
  // Session 1: Pointer in C
  {
    id: "msg-001",
    session_id: "session-001",
    role: "user",
    content: "Con trỏ trong C hoạt động thế nào và có sự khác biệt gì so với tham chiếu?",
    timestamp: "2026-06-17T09:30:10Z"
  },
  {
    id: "msg-002",
    session_id: "session-001",
    role: "assistant",
    content: "Trong lập trình C, **con trỏ (pointer)** là một biến lưu trữ địa chỉ bộ nhớ của một biến khác. Nó cho phép bạn trực tiếp tương tác và thao tác với bộ nhớ.\n\n### Điểm khác biệt chính giữa Con trỏ (C) và Tham chiếu (C++):\n1. **Khởi tạo**: Con trỏ có thể khai báo mà không cần khởi tạo ngay (ví dụ: `int *p;`), và có thể mang giá trị `NULL`. Tham chiếu bắt buộc phải gắn liền với một biến cụ thể khi khai báo.\n2. **Gán lại**: Con trỏ có thể thay đổi địa chỉ mà nó trỏ tới bất kỳ lúc nào. Tham chiếu không thể bị thay đổi để tham chiếu tới biến khác sau khi đã khởi tạo.\n3. **Cú pháp**: Con trỏ cần các toán tử định vị địa chỉ `&` và toán tử giải tham chiếu `*`. Tham chiếu sử dụng cú pháp tự nhiên như biến thông thường.",
    timestamp: "2026-06-17T09:31:00Z",
    citations: [
      { doc_id: "doc-001", page_number: 5, snippet: "Bài giảng lập trình C chương 5 đề cập đến Pointer, cấu trúc ô nhớ và cách truy xuất biến qua con trỏ." }
    ]
  },
  // Session 2: A* Search
  {
    id: "msg-003",
    session_id: "session-002",
    role: "user",
    content: "Giải thích cách hoạt động của thuật toán tìm kiếm A*",
    timestamp: "2026-06-17T09:40:15Z"
  },
  {
    id: "msg-004",
    session_id: "session-002",
    role: "assistant",
    content: "Thuật toán **A\* Search** là giải thuật tìm kiếm đường đi tốt nhất, kết hợp giữa tìm kiếm Dijkstra (khoảng cách thực tế đã đi) và thuật toán tham lam (ước lượng khoảng cách còn lại tới đích).\n\nGiải thuật dựa trên hàm đánh giá:\n$$f(n) = g(n) + h(n)$$\nTrong đó:\n- $g(n)$: Chi phí thực tế đi từ node bắt đầu đến node hiện tại $n$.\n- $h(n)$: Chi phí ước lượng (heuristic) từ node $n$ tới node đích.",
    timestamp: "2026-06-17T09:41:20Z"
  }
];

// 5. Mock DLQ Jobs (for Admin Dashboard)
export const mockDLQJobs: DLQJob[] = [
  {
    id: "job-001",
    queue_name: "ocr_queue",
    payload: {
      document_id: "doc-005",
      filename: "dm_note_corrupted.pdf",
      course_code: "IT3020E",
      attempts: 3
    },
    error_message: "RuntimeError: MinIO object retrieve failed. Connection timeout.",
    failed_at: "2026-06-17T07:45:00Z",
    ocr_trace: {
      current_step: "RETRIEVE_OBJECT",
      recent_events: [
        { time: "2026-06-17T07:44:30Z", event: "Job received from queue" },
        { time: "2026-06-17T07:44:32Z", event: "Parsing document headers" },
        { time: "2026-06-17T07:45:00Z", event: "Connection timeout while calling MinIO storage adapter" }
      ]
    }
  },
  {
    id: "job-002",
    queue_name: "eval_queue",
    payload: {
      document_id: "doc-006",
      filename: "oop_exam_2025_solutions.pdf",
      course_code: "IT3100E",
      attempts: 3
    },
    error_message: "ValidationError: Output validation failed. The generated JSON does not fit Agent 3 schema requirements.",
    failed_at: "2026-06-16T11:05:00Z",
    ocr_trace: {
      current_step: "EVALUATION_AGENT_3",
      recent_events: [
        { time: "2026-06-16T11:01:00Z", event: "Job received from eval queue" },
        { time: "2026-06-16T11:03:00Z", event: "Completed Agent 1 validation summary" },
        { time: "2026-06-16T11:04:30Z", event: "Completed Agent 2 duplicate matching check" },
        { time: "2026-06-16T11:05:00Z", event: "Validation failed: 'evaluation_justification' block is missing from final JSON response" }
      ]
    }
  }
];

// Helper functions for state modification
export const addDocument = (doc: Omit<Document, "id" | "uploaded_at" | "status">): Document => {
  const newDoc: Document = {
    ...doc,
    id: `doc-${Math.floor(1000 + Math.random() * 9000)}`,
    uploaded_at: new Date().toISOString(),
    status: "PENDING"
  };
  mockDocuments.push(newDoc);
  return newDoc;
};

export const transitionDocumentStatus = (docId: string, newStatus: DocumentStatus, errorMessage?: string): boolean => {
  const doc = mockDocuments.find(d => d.id === docId);
  if (!doc) return false;
  doc.status = newStatus;
  if (errorMessage) {
    doc.error_message = errorMessage;
  }
  return true;
};

export const reprocessDLQJob = (jobId: string): boolean => {
  const index = mockDLQJobs.findIndex(j => j.id === jobId);
  if (index === -1) return false;
  
  const job = mockDLQJobs[index];
  // Find the corresponding document and update its status back to PROCESSING
  const doc = mockDocuments.find(d => d.id === job.payload.document_id);
  if (doc) {
    doc.status = "PROCESSING";
    delete doc.error_message;
  }
  
  // Remove from DLQ queue
  mockDLQJobs.splice(index, 1);
  return true;
};
