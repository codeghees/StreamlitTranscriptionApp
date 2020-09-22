## Audio Transcription App 

### Written in Streamlit - Python

#### How to run

1. Install Streamlit `pip install streamlit`
2. Install Streamlit-ace `pip install streamlit-ace`
3. Add relevant paths in `app.py`

      `transcript_path = "PATH_TO_TRANSCRIPTS_DIR"`

      `wavs_path = "PATH_TO_WAVS/*.wav"`

      `PathToFixed ="PATH TO FIXED DIR"`
4. streamlit run app.py --server.port [PORT]

The app saves discarded files and index in State.pkl.
This will preserve your state against multiple runs and crashes.
DO NOT DELETE ONCE IT IS WRITTEN.

Live demo here (https://s4a.streamlit.io/codeghees/streamlittranscriptionapp/master/app.py/+/)
