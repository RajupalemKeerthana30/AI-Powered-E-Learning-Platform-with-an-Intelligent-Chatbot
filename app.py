import streamlit as st

from modules.ollama_client import ask_ai
from modules.pdf_reader import extract_text_from_pdf
from modules.text_processor import split_text
from modules.rag import RAGSystem


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="AI-Powered E-Learning Platform",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# COURSE DATA
# =========================================================

COURSES = {
    "Python Programming": {
        "description": "Learn Python programming from basics to intermediate concepts.",
        "lessons": [
            "Introduction to Python",
            "Variables and Data Types",
            "Conditional Statements",
            "Loops",
            "Functions",
            "Lists and Dictionaries"
        ]
    },
    "Data Science": {
        "description": "Learn the fundamentals of Data Science and data analysis.",
        "lessons": [
            "Introduction to Data Science",
            "Data Collection",
            "Data Cleaning",
            "Data Visualization",
            "Statistics",
            "Machine Learning Basics"
        ]
    },
    "Machine Learning": {
        "description": "Understand the basic concepts of Machine Learning.",
        "lessons": [
            "Introduction to Machine Learning",
            "Types of Machine Learning",
            "Supervised Learning",
            "Unsupervised Learning",
            "Regression",
            "Classification"
        ]
    }
}


# =========================================================
# LESSON CONTENT
# =========================================================

LESSON_CONTENT = {
    "Introduction to Python": [
        "🐍 What is Python?",
        "Python is a high-level programming language that is easy to learn.",
        "Python is widely used in Data Science, Artificial Intelligence, web development and automation.",
        "",
        "✨ Features of Python",
        "• Easy and simple syntax",
        "• Free and open-source",
        "• Easy to read and understand",
        "• Large number of libraries",
        "• Useful for Data Science and AI",
        "",
        "💻 Simple Example",
        "print('Hello, World!')",
        "",
        "📌 Key Point",
        "Python is popular because it is simple, powerful and versatile."
    ],

    "Variables and Data Types": [
        "📦 Variables and Data Types",
        "A variable is a name used to store a value in a program.",
        "",
        "Common Data Types:",
        "• int - whole numbers",
        "• float - decimal numbers",
        "• str - text",
        "• bool - True or False",
        "• list - collection of values",
        "• dict - key-value pairs",
        "",
        "💻 Example",
        "name = 'Keerthana'",
        "age = 20",
        "marks = 85.5"
    ],

    "Conditional Statements": [
        "🔀 Conditional Statements",
        "Conditional statements are used to make decisions in a program.",
        "",
        "Types:",
        "• if",
        "• if-else",
        "• if-elif-else",
        "",
        "💻 Example",
        "age = 18",
        "",
        "if age >= 18:",
        "    print('Eligible to vote')",
        "",
        "else:",
        "    print('Not eligible to vote')"
    ],

    "Loops": [
        "🔁 Loops",
        "Loops are used to execute a block of code repeatedly.",
        "",
        "Types of Loops:",
        "• for loop",
        "• while loop",
        "",
        "💻 Example",
        "for i in range(5):",
        "    print(i)",
        "",
        "This prints numbers from 0 to 4."
    ],

    "Functions": [
        "⚙️ Functions",
        "A function is a reusable block of code designed to perform a particular task.",
        "",
        "💻 Example",
        "def greet(name):",
        "    print('Hello', name)",
        "",
        "greet('Keerthana')",
        "",
        "Functions make programs easier to organize and reuse."
    ],

    "Lists and Dictionaries": [
        "📚 Lists and Dictionaries",
        "A list stores multiple values in an ordered collection.",
        "",
        "💻 List Example",
        "fruits = ['Apple', 'Banana', 'Mango']",
        "",
        "A dictionary stores data as key-value pairs.",
        "",
        "💻 Dictionary Example",
        "student = {",
        "    'name': 'Keerthana',",
        "    'age': 20",
        "}"
    ]
}


# =========================================================
# SESSION STATE
# =========================================================

if "rag_system" not in st.session_state:
    st.session_state.rag_system = RAGSystem()

if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


rag_system = st.session_state.rag_system


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 AI E-Learning")

st.sidebar.write(
    "Welcome to your AI-powered learning platform!"
)

selected_course = st.sidebar.selectbox(
    "📚 Select Course",
    list(COURSES.keys())
)


# =========================================================
# PDF UPLOAD
# =========================================================

st.sidebar.divider()

st.sidebar.subheader("📄 Study Material")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.sidebar.button("Process PDF"):

        with st.spinner("Processing study material..."):

            pdf_text = extract_text_from_pdf(uploaded_file)

            chunks = split_text(pdf_text)

            rag_system.add_documents(chunks)

        st.sidebar.success("✅ Study material added!")


# =========================================================
# MAIN TITLE
# =========================================================

st.title("🎓 AI-Powered E-Learning Platform")

st.subheader("with an Intelligent Chatbot")

st.write(
    "Learn courses, study materials and get help "
    "from your personal AI Tutor."
)


course = COURSES[selected_course]


# =========================================================
# TABS
# =========================================================

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Home",
        "📖 Course Learning",
        "🤖 AI Tutor",
        "📝 Quiz",
        "📄 Study Material",
        "ℹ️ About"
    ]
)


# =========================================================
# HOME
# =========================================================

with tab0:

    st.header("🏠 Welcome to AI-Powered E-Learning Platform")

    st.write(
        "Learn smarter with AI-powered courses "
        "and your personal AI Tutor."
    )

    st.subheader("📚 Your Learning Dashboard")

    total_lessons = sum(
        len(course_data["lessons"])
        for course_data in COURSES.values()
    )

    completed_count = len(
        st.session_state.completed_lessons
    )

    st.metric(
        "Total Available Lessons",
        total_lessons
    )

    st.metric(
        "Completed Lessons",
        completed_count
    )

    progress = completed_count / total_lessons

    st.subheader("📊 Overall Progress")

    st.progress(progress)

    st.write(
        f"Progress: {completed_count} / {total_lessons} lessons completed"
    )

    st.info(
        f"📖 Currently Selected Course: {selected_course}"
    )

    st.subheader("✨ Available Courses")

    for course_name, course_info in COURSES.items():

        st.write(f"### 📘 {course_name}")

        st.write(course_info["description"])


# =========================================================
# COURSE LEARNING
# =========================================================

with tab1:

    st.header(f"📚 {selected_course}")

    st.write(course["description"])

    st.subheader("Available Lessons")

    for i, lesson in enumerate(course["lessons"], start=1):

        with st.expander(
            f"Lesson {i}: {lesson}"
        ):

            if lesson in LESSON_CONTENT:

                for line in LESSON_CONTENT[lesson]:

                    if line.startswith("💻"):

                        st.subheader(line)

                    elif line.startswith("###"):

                        st.markdown(line)

                    elif line.startswith("🐍"):
                        
                        st.subheader(line)

                    elif line.startswith("✨"):
                        
                        st.subheader(line)

                    elif line.startswith("📌"):

                        st.subheader(line)

                    elif line.startswith("📦"):

                        st.subheader(line)

                    elif line.startswith("🔀"):

                        st.subheader(line)

                    elif line.startswith("🔁"):

                        st.subheader(line)

                    elif line.startswith("⚙️"):

                        st.subheader(line)

                    elif line.startswith("📚"):

                        st.subheader(line)

                    else:

                        st.write(line)

            else:

                st.write(
                    f"This lesson covers the important concepts of {lesson}."
                )

                st.write(
                    "You can ask the AI Tutor questions about this topic."
                )


            lesson_id = f"{selected_course}_{i}"

            if lesson_id in st.session_state.completed_lessons:

                st.success("✅ Lesson Completed")

            else:

                if st.button(
                    "Mark Lesson as Completed",
                    key=f"complete_{selected_course}_{i}"
                ):

                    st.session_state.completed_lessons.append(
                        lesson_id
                    )

                    st.rerun()


# =========================================================
# AI TUTOR
# =========================================================

with tab2:

    st.header("🤖 Intelligent AI Tutor")

    st.write(
        "Ask questions about your course or uploaded study material."
    )

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    question = st.chat_input(
        f"Ask something about {selected_course}..."
    )


    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)


        with st.chat_message("assistant"):

            with st.spinner("AI Tutor is thinking..."):

                context = rag_system.search(question)

                answer = ask_ai(
                    question,
                    context
                )

            st.markdown(answer)


        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

# =========================================================
# QUIZ
# =========================================================

with tab3:

    st.header("📝 Python Programming Quiz")

    st.write(
        "Test your understanding of Python programming."
    )

    q1 = st.radio(
        "1. Which of the following is a Python data type?",
        [
            "HTML",
            "int",
            "CSS",
            "HTTP"
        ],
        key="q1"
    )

    q2 = st.radio(
        "2. Which function is used to display output in Python?",
        [
            "display()",
            "show()",
            "print()",
            "output()"
        ],
        key="q2"
    )

    q3 = st.radio(
        "3. Which keyword is used to define a function in Python?",
        [
            "function",
            "define",
            "def",
            "fun"
        ],
        key="q3"
    )

    q4 = st.radio(
        "4. Which symbol is used to write a comment in Python?",
        [
            "//",
            "#",
            "/* */",
            "<!-- -->"
        ],
        key="q4"
    )

    q5 = st.radio(
        "5. Which loop is commonly used to iterate over a sequence?",
        [
            "repeat",
            "for",
            "loop",
            "iterate"
        ],
        key="q5"
    )

    if st.button("🎯 Submit Quiz"):

        score = 0

        if q1 == "int":
            score += 1

        if q2 == "print()":
            score += 1

        if q3 == "def":
            score += 1

        if q4 == "#":
            score += 1

        if q5 == "for":
            score += 1

        st.success(
            f"🎉 Your Score: {score} / 5"
        )

        if score == 5:
            st.balloons()
            st.success(
                "🏆 Excellent! You got all answers correct!"
            )

        elif score >= 3:
            st.info(
                "👍 Good job! Keep practicing to improve your score."
            )

        else:
            st.warning(
                "📚 Keep learning and try the quiz again!"
            )
# =========================================================
# STUDY MATERIAL
# =========================================================

with tab4:

    st.header("📄 Study Material")

    st.write(
        "Upload your PDF from the sidebar to give "
        "the AI Tutor additional study material."
    )

    if uploaded_file is not None:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        st.info(
            "Click Process PDF in the sidebar to add "
            "this material to the AI knowledge base."
        )

    else:

        st.info("No PDF uploaded yet.")


# =========================================================
# ABOUT
# =========================================================

with tab5:

    st.header("ℹ️ About the Project")

    st.write(
        "AI-Powered E-Learning Platform with an Intelligent Chatbot "
        "is an educational application designed to help students "
        "learn through interactive courses and AI-powered assistance."
    )

    st.subheader("✨ Main Features")

    st.write("• Multiple learning courses")
    st.write("• Lesson-wise learning")
    st.write("• AI-powered chatbot")
    st.write("• Local Llama 3.2 model")
    st.write("• PDF study material upload")
    st.write("• Text extraction from PDF")
    st.write("• Text chunking")
    st.write("• TF-IDF-based study material search")
    st.write("• RAG-based question answering")
    st.write("• Simple and user-friendly interface")

    st.success(
        "🎯 Goal: Make learning easier and more interactive using Artificial Intelligence."
    )