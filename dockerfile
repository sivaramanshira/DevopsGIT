FROM python:3

ADD source.py /
ADD HashtagToAnalyse.txt /

RUN pip install tweepy
RUN pip install textblob
RUN pip install matplotlib

CMD [ "python3", "./source.py" ]
