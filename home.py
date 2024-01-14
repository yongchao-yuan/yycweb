import streamlit as st

st.set_page_config(
    page_title="MainPage",
    page_icon="👋",
)

st.write("# Willkommen auf meiner Website 👋")

st.sidebar.success("Bitte wählen Sie eine der oben genannten Optionen.")

st.markdown(
    """
    Diese Website bietet hauptsächlich deutsches Wortlernen, 
    Bestandsinformationsanfragen, Memo und vieles mehr.
    **👈 Wählen Sie die gewünschte Funktion aus der Seitenleiste 
    aus ** !
    ### Möchten Sie mehr über Streamlit-Inhalte erfahren?
    - Suchen nach [streamlit.io](https://streamlit.io)
    - Zum Link springen [documentation](https://docs.streamlit.io)
    - AStellen Sie Fragen in  [Community-Foren]
        (https://discuss.streamlit.io)
    ### See more complex demos
    - Verwenden Sie ein neuronales Netz, [um den Udacity Self Driving Car Image Dataset zu analysieren](https://github.com/streamlit/demo-self-driving)
    - Erkunden Sie einen [New York City Rideshare-Datensatz](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
