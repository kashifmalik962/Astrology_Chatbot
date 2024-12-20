FROM node:16-alpine

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "main.py" ]