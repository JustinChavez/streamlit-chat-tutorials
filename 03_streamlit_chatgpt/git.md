## EC2 Setup

Once ssh'd into the instance, run the following commands:
```
sudo apt-get update
sudo apt upgrade -y
sudo apt-get install nginx git -y
```

I authenticate my github keys with ssh so I need to add new keys to my github account. I use the following commands to do that:
```
ssh-keygen
cat ~/.ssh/id_rsa.pub
```
Then I copy the output of the cat command and paste it into my github account under [settings/ssh keys](https://github.com/settings/ssh/new).

Finally git clone the desired repository. I will use my Streamlit Tutorial repo as an example:
```
git clone git@github.com:JustinChavez/streamlit-chat-tutorials.git
```

#### to open on vscode

sudo chown ubuntu /etc/nginx/sites-available/default
code /etc/nginx/sites-available/default
sudo chown root /etc/nginx/sites-available/default

Helpful Commands
```
#### Stop nginx
sudo service nginx start
```