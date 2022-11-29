sudo docker build -t talkhoods-app ../../.
sudo docker run -it -d -p 5000:5000 -p 3306:3306 talkhoods-app
sudo docker ps -a