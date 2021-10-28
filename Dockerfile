FROM python:3.9
COPY . .
RUN pip install -r requirements.txt

EXPOSE 3001

CMD ["python", "-u", "server.py"]