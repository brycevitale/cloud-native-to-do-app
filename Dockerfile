# docker image for frontend app
FROM python:3

# pass in the API VM IP 
ARG api_ip
ENV TODO_API_IP=${api_ip}

# install what the frontend needs
RUN pip install flask
RUN pip install requests

# flask app runs on 5000 in the container
EXPOSE 5000/tcp

# copy over the frontend app files
COPY todolist.py .
COPY templates/index.html templates/
COPY templates/login.html templates/
COPY templates/register.html templates/

# start the frontend app
CMD python todolist.py
