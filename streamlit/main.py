import requests
import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="")
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode

SPEECH_URL = 'http://localhost:8000'

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

    st.title('Speech Trainer')
    st.markdown('Train your speech skill here!')
    st.write('\n\n')

    lang = st.radio("Choose the language👇", ["zh", "en"], horizontal=True)
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        user_input = st.text_input('Type your text below')
        st.write('\n')  # add vertical spacer
        wav_audio_data = audio_recorder(energy_threshold=[0.15,0.01], pause_threshold=1.5, sample_rate=44100)# tadaaaa! yes, that's it! :D
        st.write('\n')  # add vertical spacer

        if wav_audio_data is not None:
            # display audio data as received on the Python side
            col_playback, col_space = st.columns([0.58,0.42])
            with col_playback:
                if lang == "None":
                    the_url = f"{STT_SERVICE_URL}"
                else:
                    the_url = f"{STT_SERVICE_URL}/?lang={lang}"
                st.audio(wav_audio_data, format='audio/wav')
                file = { 'file': wav_audio_data }
                try:
                    resp = requests.post(url=the_url, files=file)
                    resp = resp.json()
                    print(resp['text'])

                    st.write(resp['text'])  # add vertical spacer
                    st.write(f"the language is {resp['language']}")  # add vertical spacer
                except:
                    st.warning("failed to send the audio files to the server")
    with col_space:
        if st.button('Submit'):
            try:
                file = {'text': user_input, "gender": gender, "language": lang}
                resp = requests.post(url=TTS_SERVICE_URL, json=file,)
                st.audio(resp.content, format='audio/wav')
                # out_path = resp.headers['content
            except Exception as e:
                print(e)
                st.warning("Failed to use the TTS API")

if __name__ == '__main__':
    # call main function
    audiorec_demo_app()
