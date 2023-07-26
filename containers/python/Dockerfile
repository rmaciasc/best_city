FROM python:3.11.4-bookworm
# Adding trusting keys to apt for repositories

ARG CHROME_VERSION="114.0.5735.198-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
    && apt update \
    && apt install -y /tmp/chrome.deb \
    && apt update --fix-missing \
    && rm /tmp/chrome.deb 
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

# Install requirements
COPY ./requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome-stable_current_amd64.deb
# sudo apt --fix-broken installdf