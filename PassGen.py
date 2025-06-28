import streamlit as st
import string
import secrets

# --- Helper Functions ---
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return ""

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    return score

def strength_label(score):
    if score <= 2:
        return "Weak", "❌"
    elif score == 3:
        return "Moderate", "⚠️"
    elif score == 4:
        return "Strong", "✅"
    else:
        return "Excellent", "🌟"

# --- Streamlit App ---
st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    .stButton>button {
        color: white;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        border: none;
        padding: 0.5em 2em;
        font-weight: bold;
        font-size: 1.1em;
    }
    .stSlider>div>div>div>div {
        background: #667eea;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔐 Beautiful Password Generator")
st.write(
    "Create strong, secure, and unique passwords instantly. "
    "Customize your password and check its strength in real time!"
)

with st.sidebar:
    st.header("🔧 Customize your password")
    length = st.slider("Password Length", 8, 32, 12)
    use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
    use_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
    use_digits = st.checkbox("Include Numbers (0-9)", value=True)
    use_symbols = st.checkbox("Include Symbols (!@#...)", value=True)

if not (use_upper or use_lower or use_digits or use_symbols):
    st.warning("Please select at least one character type.")
    st.stop()

if st.button("✨ Generate Password"):
    password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
    if password:
        st.success("Your generated password:")
        st.code(password, language="")

        # Custom copy to clipboard button with JavaScript
        copy_code = f"""
        <button onclick="navigator.clipboard.writeText('{password}'); 
                         var btn = this; btn.innerText='✅ Copied!'; 
                         setTimeout(function(){{btn.innerText='📋 Copy to Clipboard';}}, 2000);"
            style="
                background-color: #667eea;
                color: white;
                padding: 0.5em 1em;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1em;
                margin-top: 10px;
            ">📋 Copy to Clipboard</button>
        """
        st.markdown(copy_code, unsafe_allow_html=True)
        st.write("*(Copied password will be available in your clipboard.)*")

        # Password strength
        score = password_strength(password)
        label, icon = strength_label(score)
        st.progress(score / 5)
        st.markdown(f"**Strength:** {icon} {label}")

        # Toast for strong passwords
        if score >= 4:
            st.toast("✅ Strong password generated!", icon="🔒")
    else:
        st.error("No character types selected. Please adjust your options.")
else:
    st.info("Click '✨ Generate Password' to create your password.")

st.markdown(
    """
    <hr>
    <div style="text-align:center; color: #888;">
        <small>Made with ❤️ using Streamlit | <a href="https://github.com/CyberArchit3ct" target="_blank">My Github</a></small>
    </div>
    """,
    unsafe_allow_html=True
)
