FROM pypy:3
WORKDIR /app
COPY . /app
RUN  pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt 
EXPOSE 80
CMD ["pypy3","app.py"]
