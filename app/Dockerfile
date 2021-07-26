FROM ""

USER 0
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN sudo mkdir /app/serve
RUN sudo chmod 755 /app/serve
CMD [ "python", "./server.py" ]