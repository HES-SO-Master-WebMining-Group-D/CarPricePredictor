FROM python:3.10

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src/

EXPOSE 8050

CMD ["python", "src/main_ui.py"]