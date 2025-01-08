import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase


class SimpleVideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        return frame


def main():
    st.title("Teste WebRTC")
    webrtc_streamer(
        key="example",
        video_transformer_factory=SimpleVideoTransformer,
    )


if __name__ == "__main__":
    main()
