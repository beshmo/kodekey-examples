FROM debian:trixie-slim

RUN apt-get update && apt-get install -y \
    git \
    ssh \
    curl \
    python3-full \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN cd /opt && git clone https://github.com/beshmo/kodekey-examples.git

WORKDIR /opt/kodekey-examples/kodekey-chatbot

RUN python3 -m venv /opt/kodekey-examples/kodekey-chatbot/venv
RUN /opt/kodekey-examples/kodekey-chatbot/venv/bin/python -m pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

COPY .env.example /opt/kodekey-examples/kodekey-chatbot/.env

RUN sed -i 's/your-api-key-here/'"$KODEKEY_API_KEY"'/g' /opt/kodekey-examples/kodekey-chatbot/.env

EXPOSE 8501

CMD ["./venv/bin/streamlit", "run", "chatbot_stream.py"]

