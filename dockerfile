FROM python:3.10

WORKDIR /fastapi-all_the_way

COPY requirements.txt /fastapi-all_the_way

RUN pip install -r /fastapi-all_the_way/requirements.txt

COPY items_manager/ /fastapi-all_the_way/items_manager/

EXPOSE 8080

CMD ["python", "items_manager/main.py"]
