FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/umudmmmdov1/upbot /root/upbot
WORKDIR /root/upbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
