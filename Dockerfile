# Use an existing Docker image as a base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
# Copy only the necessary files
COPY src/ ./src
COPY requirements.txt .
COPY .env .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ETL script into the container
#COPY [ "Pipfile", "Pipfile.lock", "./" ]
#COPY [src/ .]
COPY src/ ./src


# Specify the command to run the ETL process
# Run app.py when the container launches
#CMD ["python", "main_ELT.py"]
ENTRYPOINT ["python", "./src/main.py"]
