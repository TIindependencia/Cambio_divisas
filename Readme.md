crear imagen docker 
docker build -t docker-python .

docker run -it --name docker-python docker-python

entrar al docker  docker exec -i -t -u root 6ad5 /bin/sh


docker exec -it [container] pip3 install pandas