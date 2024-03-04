import requests
import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Speech Trainer Tools")
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>.stAudio {height: 45px;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''', unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''', unsafe_allow_html=True)  # lightmode

SPEECH_URL = 'http://localhost:8000'
STT_SPEECH_URL = f"{SPEECH_URL}/recognize_speech"
TTS_SPEECH_URL = f"{SPEECH_URL}/generate_sample_audio"
SCORING_SPEECH_URL = f"{SPEECH_URL}/get_score"

def audiorec_demo_app():
    speech_service_status = False
    try:
        response = requests.get(SPEECH_URL)
        if response.status_code==200:
            speech_service_status = True
    except:
        st.warning("Couldn't connect to Server ..")
        st.stop()
    if not speech_service_status:
        st.error("The speech API is down!!")
        st.stop()

    st.title('Speech Trainer Tools')
    st.markdown('Train your speech skill here!')
    st.write('\n\n')

    lang = st.radio("Choose the language👇", ["zh", "en"], horizontal=True)
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        user_input = st.text_input('Type your text below')
    with col_space:
        if st.button('Listen'):
            try:
                the_url = f"{TTS_SPEECH_URL}/?text={user_input}&lang={lang}"
                resp = requests.get(url=the_url)
                st.audio(resp.content, format='audio/wav')
                # out_path = resp.headers['content
            except Exception as e:
                print(e)
                st.warning("Failed to use the TTS API")
    col_info2, col_space2 = st.columns([0.57, 0.43])
    with col_info2:
        wav_audio_data = audio_recorder(energy_threshold=[0.15,0.01], pause_threshold=1.5, sample_rate=44100)# tadaaaa! yes, that's it! :D
        st.write('\n')  # add vertical spacer
        do_scoring = False
        if wav_audio_data is not None:
            the_url = f"{STT_SPEECH_URL}/?lang={lang}"
            st.audio(wav_audio_data, format='audio/wav')
            file = { 'file': wav_audio_data }
            try:
                resp = requests.post(url=the_url, files=file)
                resp = resp.json()
                result = resp['text'][0]
                print(resp['text'])
                st.write(resp['text'][0])  # add vertical spacer
                do_scoring = True
            except Exception as e:
                print(e)
                st.warning("failed to do speech recognition")
            if do_scoring:
                try:
                    the_url = f"{SCORING_SPEECH_URL}/?ground_truth={user_input}&answer={result}&lang={lang}"
                    resp = requests.get(url=the_url)
                    resp = resp.json()
                    print(resp['score'])
                    st.write(f"Your speech error rate is {resp['score']}")  # add vertical spacer
                except Exception as e:
                    print(e)
                    st.warning("failed to do speech scoring")

if __name__ == '__main__':
    audiorec_demo_app()    # call main function
