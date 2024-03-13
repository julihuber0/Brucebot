FROM python
WORKDIR /app
COPY requirements_fixed.txt requirements_fixed.txt
RUN pip3 install -r requirements_fixed.txt

COPY . .

CMD ["python3","main.py"]