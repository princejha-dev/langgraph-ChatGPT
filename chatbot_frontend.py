import streamlit
from chatbot_backend import chatbot

if not "message_history" in st.session_state():
    st.session_state['message_history'] = []

for messages in st.session_state['message_history']:
    with st.chat_message[messages['role']]:
        st.text(messages['content'])

user_input = st.text_input("Type here")

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    ai_response = chatbot.invoke(user_input)
    st.session_state['message_history'].append({'role':'ai','content':ai_response})