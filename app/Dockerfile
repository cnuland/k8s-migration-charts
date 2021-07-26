FROM ""

USER 0
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir /app/serve
RUN chmod 755 /app/serve
CMD [ "python", "./server.py" ]