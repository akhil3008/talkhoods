sudo docker build -t akhil_app_talk_hoods ../../.
sudo docker run -it -d -p 5000:5000 -p 3306:3306 akhil_app_talk_hoods
sudo docker ps -a