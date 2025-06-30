**Multilingual-AES-with-Rubric-Customization**

![image](https://github.com/user-attachments/assets/ed81c06d-4d97-45f3-9108-cbcac0ed322d)

The Multilingual AES and feedback generation system illustrated in Figure 1 is supported by a flexible system design that has four components: the front-end user interface, the back-end server, the LLM integration module, and the data storage component.  

**Front-end user interface:** The front end has two parts: one for administrators and one for students. Students use their part to see available rubrics that are assigned by the admin, upload essays, and see feedback. Administrators use their part to manage essay topics, language, difficulty, standard of the essay and create rubrics. 

**Back-end server:**  The backend server is the core coordinator, providing user authentication, request routing, and role-based access. It securely coordinates interaction among users, the LLM module, and the database. When an evaluation is started, the server translates the rubric and essay into a prompt appropriate for the input format of the chosen LLM. The LLM integration module receives the prompt from the API, interfacing with proprietary LLMs hosted via open-source models such as LLaMA3-70B-8192 served through the Groq API, which enables high throughput local or cloud-based execution.

**LLM integration module:** The LLM integration module performs the tasks of prompt engineering while executing API calls and result parsing and error management tasks. It enables the LLM to generate outputs that are brief yet easy to read while following the definitions from the established rubric. 

**Data storage component:** The processed outputs move from the front end to the backend where they are saved in an auditable relational database. The database contains user profiles together with submitted essays and defined rubric templates and evaluation results and feedback records. The system enables auditing through the assessment of past evaluations together with feedback delivered by the model while maintaining full transparency. 
