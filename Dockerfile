# Uses a lightweight Linux image with Python 3.12.
FROM python:3.12-slim  

# Sets /app as the working directory inside the container.
WORKDIR /app

# Copies our project files from the current folder into /app inside the image.
COPY . /app

# apt-get update → Updates the Linux package list so the system knows about the latest available packages.
# pip install → Installs all Python packages listed in requirements.txt.
RUN apt-get update && pip install -r requirements.txt

# Runs app.py when the Docker container starts.
# When you run docker run Only this line runs:
CMD ["python3", "app.py"]