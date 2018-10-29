FROM python
RUN pip install --upgrade pip
RUN pip install bottle
VOLUME /mnt
WORKDIR /mnt
ADD . /mnt
EXPOSE 80
CMD python server.py
