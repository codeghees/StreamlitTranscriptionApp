import glob
import SessionState
import streamlit as st
from streamlit_ace import st_ace
import os
import pickle


THEMES = ["chrome", "ambiance"]
DELIM = "/" # Use "/" for Linux
KEYBINDINGS = [
    "emacs", "sublime", "vim", "vscode"
]
# @st.cache

def SavePickleState(index, rejected = ""):
    print(index)
    if os.path.exists("State.pkl"):
       StateDict = {}
       with open("State.pkl", "rb") as Pkl:
           StateDict =  pickle.load(Pkl)
       with open("State.pkl", "wb") as Pkl:
            StateDict["current_index"] = index
            if rejected!= "":
                StateDict["rejected"].append(rejected)
            pickle.dump(StateDict, Pkl)
    else:
        with open('State.pkl', 'wb') as pklfile:
            StateDict = {}
            StateDict["current_index"] = index
            StateDict["rejected"] = []
            if rejected!= "":
                StateDict["rejected"].append(rejected)
            pickle.dump(StateDict, pklfile)
            pklfile.close()

def render_file(wavfile, transcript_path, PathToFixed):
    
    TranscriptFile = os.path.join(transcript_path, wavfile.split(DELIM)[-1].replace(".wav",".txt"))

    with open(TranscriptFile,'r', encoding='utf-8') as f:
      data = f.read()
    key = wavfile.split(DELIM)[-1]
    
    st.subheader("Name of File = " + key)
    st.audio(open(wavfile, 'rb').read(), format='audio/wav')
    content = st_ace(
    value = data,
    theme=st.sidebar.selectbox("Theme.", options=THEMES, key=key),
    font_size=st.sidebar.slider("Font size.", 5, 24, 24, key=key),
    tab_size=st.sidebar.slider("Tab size.", 1, 8, 4, key=key),
    show_gutter=st.sidebar.checkbox("Show gutter.", value=True, key=key),
    show_print_margin=st.sidebar.checkbox("Show print margin.", value=True,key=key),
    wrap=st.sidebar.checkbox("Wrap enabled.", value=True,key=key),
    key=key
    )
    st.title(content)
    

    if st.sidebar.button("Reject"):
        print("Reject", key)
        SessionState.get().current_index += 1
        SessionState.sync()
        SavePickleState(SessionState.get().current_index, key.replace(".wav", ".txt"))
        return


    if st.sidebar.button("Go to next file"):

        FixedTranscript = os.path.join(PathToFixed, key.replace(".wav", ".txt"))
        print(FixedTranscript)
        open(FixedTranscript,"w", encoding = "utf-8").write(content)
        SessionState.get().current_index += 1
        SessionState.sync()
        SavePickleState(SessionState.get().current_index)

           

# SET PATHS 
# transcript_path: Path to all the transcripts.
# wavs_path: Path to all the wavs. INCLUDE *.wav AT THE END 
# PathToFixed: Path where to save the FixedTranscripts

def main():
    st.title("Transcription Labeling App")
    st.sidebar.title("Labeling Data")


    
    # PATHS
    transcript_path = "./sample/"
    wavs_path = "./sample/*.wav"
    wavs_list = glob.glob(wavs_path)  
    PathToFixed ="./sample/"

    # LOAD STATE
    current_index = 0
    if os.path.exists("State.pkl") and os.path.getsize("State.pkl")>0:
       with open("State.pkl", "rb") as ReadPickle:
        StateDict =  pickle.load(ReadPickle)
        current_index = StateDict["current_index"]
        # print(StateDict)
        ReadPickle.close()

    session_state = SessionState.get(current_index = current_index)

    if session_state.current_index == len(wavs_list):
        st.warning("DONE!")
        st.stop()

    render_file(wavs_list[session_state.current_index], transcript_path, PathToFixed)


if __name__ == "__main__":
    main()
