pip install -r requirements.txt
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
ngrok config add-authtoken 2wwCZ7hSsVKLHhIclv5s4j3HH9b_4LHYLWPpHzi4e11EJTvJv
