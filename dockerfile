FROM python:3.9-slim

# Java ইনস্টল করা (APK সাইনিং এর জন্য প্রয়োজন)
RUN apt-get update && apt-get install -y openjdk-11-jdk wget unzip

# APK Signer টুল ডাউনলোড করা
RUN wget https://github.com/shcarry/uber-apk-signer/releases/download/v1.3/uber-apk-signer.jar -O /uber-apk-signer.jar

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
