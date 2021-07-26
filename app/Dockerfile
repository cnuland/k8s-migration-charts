FROM ""

COPY requirements.txt ./

ADD charts /usr/local/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]