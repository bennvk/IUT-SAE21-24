FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --proxy http://cache-etu.univ-artois.fr:3128 --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]