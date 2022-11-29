sudo docker build -t talk-hoods-app ../fe-be/.
sudo docker run -it -d -p 5000:5000 -p 3306:3306 talk-hoods-app
sudo docker ps -a