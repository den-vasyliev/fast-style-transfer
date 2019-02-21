FROM python:2.7-slim as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt .
RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev libffi-dev --no-install-recommends
RUN pip install -r requirements.txt --prefix="/install"
FROM python:2.7-slim
COPY --from=builder /install /usr/local
RUN apt-get update && apt-get install -qq -y libgomp1
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["gunicorn", "-b :5000", "app:app"]
