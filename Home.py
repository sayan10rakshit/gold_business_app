import streamlit as st


# Main Streamlit App
st.set_page_config(
    page_title="Gold Calculator",
    page_icon="✨",  # Add your own icon
    layout="wide",
)

st.title("Gold Calculator :sparkles:")
st.write(
    "Welcome to the Gold Calculator, your one-stop solution for all your gold purchasing or selling needs."
)
if "mesage_shown" not in st.session_state:
    st.toast(
        "**Please select an option from the sidebar to get started**",
        icon="✨",
    )
    st.toast(
        "**More features coming soon!**",
        icon="✨",
    )
    st.session_state["mesage_shown"] = True

st.markdown("")

st.markdown("### What can this app do for you?")
col1, col2 = st.columns([1, 2], gap="small")
with col1:
    st.markdown(" - :green[**Transparent Pricing**]:")
with col2:
    st.markdown("Understand the breakdown of charges.")

col1, col2 = st.columns([1, 2], gap="small")
with col1:
    st.markdown(" - :green[**Save Money**]:")
with col2:
    st.markdown("Don't pay more than you should.")

col1, col2 = st.columns([1, 2], gap="small")
with col1:
    st.markdown(" - :green[**Save Time**]:")
with col2:
    st.markdown("No more manual calculations or guesswork.")

st.markdown("")
st.markdown(
    "Start exploring and make your gold purchasing or selling experience smoother and smarter with Gold Calculator!"
)
