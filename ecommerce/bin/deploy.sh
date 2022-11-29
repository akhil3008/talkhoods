sudo docker build -t talk--hoods-app--apts ../../.
sudo docker run -it -d -p 5000:5000 -p 3306:3306 talk--hoods-app talk--hoods-app--apts
sudo docker ps -a