FROM python:3.11.4-bookworm

# Use specific chrome version as sometimes the webdriver is not available for the latest stable
ARG CHROME_VERSION="114.0.5735.198-1"
# Updating apt to see and install Google Chrome
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
    && apt update \
    && apt install -y /tmp/chrome.deb \
    && apt update --fix-missing \
    && rm /tmp/chrome.deb 

# Install requirements
COPY ./containers/python/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
# RUN mkdir /opt/app
COPY ./ opt/app
WORKDIR /opt/app
CMD [ "python", "main.py" ]