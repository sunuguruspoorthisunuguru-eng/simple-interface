import streamlit as st
from datetime import datetime
import time
import html

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Simple Interface - Real-Time Interaction",
    page_icon="💬",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "username" not in st.session_state:
    st.session_state.username = "User"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ============================================================
# HTML + CSS + JAVASCRIPT
# ============================================================

st.markdown("""
<style>

* {
    box-sizing: border-box;
}

.stApp {
    background: #0f172a;
    color: #f8fafc;
    font-family: Arial, sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 25px;
}

/* ================= HEADER ================= */

.header {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.3);
}

.header-content {
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-icon {
    width: 60px;
    height: 60px;
    background: rgba(255,255,255,0.2);
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}

.header h1 {
    margin: 0;
    color: white;
    font-size: 28px;
}

.header p {
    margin: 5px 0 0;
    color: #dbeafe;
    font-size: 14px;
}

.online {
    display: inline-block;
    margin-top: 15px;
    padding: 6px 12px;
    border-radius: 20px;
    background: rgba(34,197,94,0.2);
    color: #86efac;
    font-size: 12px;
    border: 1px solid rgba(134,239,172,0.3);
}

/* ================= USER CARD ================= */

.user-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 20px;
}

.user-title {
    font-size: 13px;
    color: #94a3b8;
}

.user-name {
    font-size: 18px;
    font-weight: bold;
    margin-top: 5px;
    color: white;
}

/* ================= CHAT AREA ================= */

.chat-container {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 20px;
    min-height: 420px;
    max-height: 500px;
    overflow-y: auto;
}

/* ================= MESSAGE ================= */

.message {
    display: flex;
    margin-bottom: 18px;
    animation: slideIn 0.3s ease;
}

.message.user {
    justify-content: flex-end;
}

.message.other {
    justify-content: flex-start;
}

.message-box {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 16px;
}

.message.user .message-box {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white;
    border-bottom-right-radius: 4px;
}

.message.other .message-box {
    background: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-bottom-left-radius: 4px;
}

.message-user {
    font-size: 11px;
    font-weight: bold;
    margin-bottom: 4px;
    opacity: 0.8;
}

.message-text {
    font-size: 15px;
    line-height: 1.5;
    word-wrap: break-word;
}

.message-time {
    font-size: 10px;
    margin-top: 6px;
    opacity: 0.6;
}

/* ================= EMPTY CHAT ================= */

.empty {
    text-align: center;
    padding: 100px 20px;
    color: #64748b;
}

.empty-icon {
    font-size: 50px;
    margin-bottom: 10px;
}

/* ================= TYPING ================= */

.typing {
    display: flex;
    gap: 5px;
    padding: 10px;
}

.dot {
    width: 8px;
    height: 8px;
    background: #94a3b8;
    border-radius: 50%;
    animation: typing 1s infinite;
}

.dot:nth-child(2) {
    animation-delay: 0.2s;
}

.dot:nth-child(3) {
    animation-delay: 0.4s;
}

/* ================= BUTTONS ================= */

.stButton button {
    border-radius: 10px;
    background: #1e293b;
    color: white;
    border: 1px solid #475569;
    transition: 0.2s;
}

.stButton button:hover {
    background: #2563eb;
    border-color: #60a5fa;
    color: white;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 11px;
    padding: 20px;
}

/* ================= ANIMATIONS ================= */

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
    }

    30% {
        transform: translateY(-5px);
    }
}

/* ================= MOBILE ================= */

@media(max-width: 700px) {

    .header h1 {
        font-size: 21px;
    }

    .header-icon {
        width: 50px;
        height: 50px;
        font-size: 24px;
    }

    .message-box {
        max-width: 85%;
    }

    .chat-container {
        min-height: 400px;
    }
}

</style>

<script>

// Scroll chat area to bottom

function scrollToBottom() {

    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    });

}

// Keyboard shortcut

document.addEventListener("keydown", function(event) {

    // Ctrl + Enter can be used for quick interaction

    if (event.ctrlKey && event.key === "Enter") {

        const buttons = document.querySelectorAll(
            'button'
        );

        if (buttons.length > 0) {
            buttons[buttons.length - 1].click();
        }
    }

});

</script>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header">

    <div class="header-content">

        <div class="header-icon">
            💬
        </div>

        <div>

            <h1>
                Simple Interface for Real-Time User Interaction
            </h1>

            <p>
                A clean and responsive interface for real-time communication
            </p>

        </div>

    </div>

    <div class="online">
        ● Online • Real-Time Interaction
    </div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Controls")

    username = st.text_input(
        "Enter your name",
        value=st.session_state.username
    )

    if username.strip():
        st.session_state.username = username.strip()

    st.divider()

    if st.button(
        "🗑️ Clear Messages",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("""
    ### 📌 Features

    ✅ Simple interface  
    ✅ Real-time interaction  
    ✅ User messages  
    ✅ Timestamps  
    ✅ Typing indicator  
    ✅ Responsive design  
    ✅ HTML + CSS + JavaScript  
    ✅ Python backend  

    """)

# ============================================================
# USER INFORMATION
# ============================================================

st.markdown(f"""
<div class="user-card">

    <div class="user-title">
        CURRENT USER
    </div>

    <div class="user-name">
        👤 {html.escape(st.session_state.username)}
    </div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# CHAT DISPLAY
# ============================================================

st.markdown(
    '<div class="chat-container">',
    unsafe_allow_html=True
)

if not st.session_state.messages:

    st.markdown("""
    <div class="empty">

        <div class="empty-icon">
            💬
        </div>

        <h3>
            Start a conversation
        </h3>

        <p>
            Enter a message below to begin real-time interaction.
        </p>

    </div>
    """, unsafe_allow_html=True)

else:

    for message in st.session_state.messages:

        message_class = (
            "user"
            if message["user"] == st.session_state.username
            else "other"
        )

        safe_user = html.escape(message["user"])
        safe_message = html.escape(message["text"])

        st.markdown(
            f"""
            <div class="message {message_class}">

                <div class="message-box">

                    <div class="message-user">
                        {safe_user}
                    </div>

                    <div class="message-text">
                        {safe_message}
                    </div>

                    <div class="message-time">
                        {message["time"]}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# MESSAGE INPUT
# ============================================================

st.markdown("### ✍️ Send a Message")

message_input = st.chat_input(
    "Type your message and press Enter..."
)

# ============================================================
# PROCESS MESSAGE
# ============================================================

if message_input:

    clean_message = message_input.strip()

    if clean_message:

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        # Add user message

        st.session_state.messages.append({
            "user": st.session_state.username,
            "text": clean_message,
            "time": current_time
        })

        # Simulated real-time processing

        with st.spinner("Processing..."):

            time.sleep(0.5)

        # Simple automatic response

        lower_message = clean_message.lower()

        if "hello" in lower_message or "hi" in lower_message:

            reply = (
                f"Hello {st.session_state.username}! 👋 "
                "Nice to interact with you."
            )

        elif "how are you" in lower_message:

            reply = (
                "I'm doing great! 😊 "
                "I'm ready for your next message."
            )

        elif "help" in lower_message:

            reply = (
                "Sure! You can send me messages and "
                "I'll respond in real time."
            )

        else:

            reply = (
                f"Received your message: "
                f"\"{clean_message}\" 👍"
            )

        reply_time = datetime.now().strftime(
            "%I:%M %p"
        )

        # Add response

        st.session_state.messages.append({
            "user": "System Assistant",
            "text": reply,
            "time": reply_time
        })

        st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    Simple Interface for Real-Time User Interaction

    <br><br>

    Built with Python • Streamlit • HTML • CSS • JavaScript

</div>
""", unsafe_allow_html=True)