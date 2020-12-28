# Use an official Python runtime as a parent image
FROM python:3.6-slim

# run as user prod
RUN useradd prod -d /home/prod && mkdir /home/prod && chown -R prod.prod /home/prod
USER prod

# Set the working directory
WORKDIR /home/prod

# Copy source into the image
# one layer per file to make use of caching
COPY --chown=prod:prod main /home/prod 
COPY --chown=prod:prod messages.py /home/prod  
COPY --chown=prod:prod metrics.py /home/prod
COPY --chown=prod:prod server.py /home/prod

# make main executable, permissions don't persist :expressionless:
RUN chmod u+x /home/prod/main

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run when the container launches
CMD ["./main"]
