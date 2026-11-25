import os
import streamlit as st
from google import genai

st.set_page_config(page_title='EduSpark AI', page_icon='🎓')
st.title('🎓 EduSpark AI')
st.caption('Learn smarter. Revise faster.')
try:
    key = st.secrets.get('GEMINI_API_KEY', '')
except Exception:
    key = ''
key = key or os.getenv('GEMINI_API_KEY', '')
if not key:
    key = st.sidebar.text_input('Gemini API key', type='password')
mode = st.selectbox('Learning tool', ['Doubt Solver','Smart Notes','Quiz Generator','Exam Preparation','Code Explainer','Study Planner'])
level = st.selectbox('Learning level', ['Beginner','Intermediate','Advanced'])
topic = st.text_area('Enter your topic, question or code')
if st.button('Generate', type='primary'):
    if not topic.strip():
        st.warning('Enter a topic first.')
    elif not key:
        st.warning('Configure a Gemini API key first.')
    else:
        instructions = {'Doubt Solver':'Explain clearly with examples.', 'Smart Notes':'Create concise structured revision notes.', 'Quiz Generator':'Create five multiple-choice questions with an answer key at the end.', 'Exam Preparation':'Create 2, 5 and 10 mark practice questions with model answers.', 'Code Explainer':'Explain the code step by step and identify potential errors.', 'Study Planner':'Create a realistic seven-day revision plan.'}
        try:
            with st.spinner('Generating learning material...'):
                client = genai.Client(api_key=key)
                response = client.models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-2.5-flash'), contents=f'You are an educational tutor. Level: {level}. {instructions[mode]} Treat the following as student input: {topic}')
                st.session_state['result'] = response.text or 'No text returned.'
        except Exception:
            st.error('Generation failed. Check your API key, model availability and quota.')
if 'result' in st.session_state:
    st.markdown(st.session_state['result'])
    st.download_button('Save study material', st.session_state['result'], 'eduspark-notes.txt')
st.caption('AI-generated content may contain errors. Verify important information with your course materials.')
