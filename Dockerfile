FROM python:3.12.1

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /blog

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# Expose port
EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["/blog/blogsh.sh"]