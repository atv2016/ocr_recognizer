FROM python:3.10.12

WORKDIR /usr/src/app

EXPOSE 7777/tcp

COPY requirements.txt .

# LibGL install is to fix ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update && \
apt install -y libgl1-mesa-glx && \
pip install -r requirements.txt

COPY main.py .

ENTRYPOINT  ["python"]
CMD ["./main.py"]
