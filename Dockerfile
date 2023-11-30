FROM harbor.inboc.net/images/ubuntu_conda:v1
WORKDIR /opt
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements.txt
