import streamlit as st
import secrets
import string
import streamlit.components.v1 as components


def generate_password(length, upper, lower, digits, symbols):
    charset = ""
    if upper:
        charset += string.ascii_uppercase
    if lower:
        charset += string.ascii_lowercase
    if digits:
        charset += string.digits
    if symbols:
        charset += string.punctuation

    if not charset:
        return ""

    return ''.join(secrets.choice(charset) for _ in range(length))


def evaluate_strength(password):
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


def strength_feedback(score):
    if score <= 2:
        return "Weak", "❌"
    elif score == 3:
        return "Moderate", "⚠️"
    elif score == 4:
        return "Strong", "✅"
    else:
        return "Excellent", "🌟"


st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="centered")

st.markdown("""
    <style>
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
""", unsafe_allow_html=True)

st.title("🔐 Password Generator")
st.write("Create strong, secure, and unique passwords instantly. Customize the options below and check the strength of your new password.")

with st.sidebar:
    st.header("🔧 Customize Your Password")
    length = st.slider("Password Length", 8, 32, 12)
    use_upper = st.checkbox("Include Uppercase (A-Z)", value=True)
    use_lower = st.checkbox("Include Lowercase (a-z)", value=True)
    use_digits = st.checkbox("Include Numbers (0–9)", value=True)
    use_symbols = st.checkbox("Include Symbols (!@#$...)", value=True)

if not (use_upper or use_lower or use_digits or use_symbols):
    st.warning("Please select at least one character type.")
    st.stop()

if st.button("✨ Generate Password"):
    password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)

    if password:
        st.success("Here’s your new password:")
        st.code(password, language="")

        # Escape characters for JavaScript string
        js_safe_pw = password.replace("\\", "\\\\").replace("'", "\\'")

        components.html(f"""
            <script>
                function copyPassword() {{
                    navigator.clipboard.writeText('{js_safe_pw}').then(() => {{
                        const btn = document.getElementById('copy-btn');
                        btn.innerText = '✅ Copied!';
                        setTimeout(() => btn.innerText = '📋 Copy to Clipboard', 2000);
                    }});
                }}
            </script>
            <button id="copy-btn" onclick="copyPassword()"
                style="
                    background-color: #667eea;
                    color: white;
                    padding: 0.5em 1em;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1em;
                    margin-top: 10px;
                ">
                📋 Copy to Clipboard
            </button>
        """, height=70)

        st.caption("The password has been copied to your clipboard.")

        strength = evaluate_strength(password)
        label, icon = strength_feedback(strength)
        st.progress(strength / 5)
        st.markdown(f"**Strength:** {icon} {label}")

        if strength >= 4:
            st.toast("✅ Strong password generated!", icon="🔒")
    else:
        st.error("Unable to generate password. Please check your settings.")
else:
    st.info("Click the button above to generate a password.")

st.markdown("""
    <hr>
    <div style="text-align:center; color: #888;">
        <small>Made for fun | <a href="https://github.com/CyberArchit3ct" target="_blank">My GitHub</a></small>
    </div>
""", unsafe_allow_html=True)
