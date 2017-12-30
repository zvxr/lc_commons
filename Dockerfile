# 
# Image for project.
#
FROM python:3.6

MAINTAINER Mike McConnell


# Set-up installation
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/


# Add source
RUN mkdir -p /lc-commons-dist/lc_commons
ADD . /lc-commons-dist/lc_commons
RUN mv /lc-commons-dist/lc_commons/setup.py /lc-commons-dist/


# Install source -- basic setup.py
RUN cd /lc-commons-dist &&\
    python setup.py build &&\
    python setup.py install


# Default command
CMD ["python"]
