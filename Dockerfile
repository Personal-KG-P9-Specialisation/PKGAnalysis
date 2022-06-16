FROM python:3.9-slim-buster
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_md
RUN python3 -m spacy_entity_linker "download_knowledge_base"
COPY eml.py eml.py
CMD ["python3", "eml.py"]
