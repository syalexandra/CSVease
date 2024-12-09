FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Create user's home directory structure
RUN mkdir -p /root/ && \
    mv /app/input/generator/* /root/ && \
    rm -rf /app/input

# Set up the csvease command
RUN echo 'alias csvease="python3 /app/CSVeaseGenerator.py"' > /root/.bash_aliases

RUN echo 'if [ -f ~/.bash_aliases ]; then\n\
    . ~/.bash_aliases\n\
fi' >> /root/.bashrc

RUN echo 'shopt -s expand_aliases' >> /root/.bashrc

SHELL ["/bin/bash", "-c"]

RUN chmod +x test.sh

RUN echo 'export PS1="\[\033[1;35m\]csvease>\[\033[0m\] "' >> /root/.bashrc

WORKDIR /root

ENTRYPOINT ["/bin/bash", "-l"]
