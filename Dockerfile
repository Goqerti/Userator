FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/goqerti/userator /root/userator
WORKDIR /root/userator/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
