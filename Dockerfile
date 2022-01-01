FROM python:3.8

WORKDIR /app

COPY . .
COPY requirements.txt requirements.txt

ENV TZ=Asia/Seoul

RUN python -m pip install --upgrade pip

# Install Dependencies of Miniconda
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge" >> ~/.bashrc && \
    echo "conda install -c conda-forge jpype1" >> ~/.bashrc


#RUN python -m pip install gunicorn

#CMD ["python", "manage.py", "runserver"]

#EXPOSE 8000