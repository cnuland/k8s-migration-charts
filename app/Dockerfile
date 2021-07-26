FROM ""

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir /app/serve
CMD [ "python", "./server.py" ]