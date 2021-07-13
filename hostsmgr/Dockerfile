FROM python:3.8

RUN pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install starlette -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pydantic -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pymongo -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mkdir /app
COPY *.py /app/

WORKDIR /app

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--reload"]
