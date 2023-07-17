Follow [Amazon Linux Setup Tutorial](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html). I use the following configs:
- Instead of Amazon Linux choose Ubuntu any size (I use t2.small) 
- Security group: allow all traffic for ssh/http/https (also add inbound for port 8501 for all ip)
- Storage any size (I use 40GB)

## Streamlit Setup

Once ssh'd into the instance, run the following commands:
```
sudo apt-get update
sudo apt upgrade -y
```

Let's setup a basic streamlit application on localhost
```
python3 -m venv venv
```
⚠️ Warning, you may see the following error
```
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.10-venv
```
Follow the instrustions and install the package, but add sudo and -y to the command they give you:
```
sudo apt install python3.10-venv -y
```
Continue installing the packages and create the .env file
```
. venv/bin/activate
pip install streamlit
```

Create a simple streamlit application that prints "hello world" in a file called `app.py`
```
echo -e 'import streamlit as st\n\nst.write("hello world")' > app.py
```

Run the application and open the External URL in your browser. You should be able to see "hello world".
```
streamlit run app.py
```

## Setup HTTP Access

Install nginx
```
sudo apt-get install nginx -y
```

#### Create nginx
Clear the current configuration of nginx
```
sudo sh -c 'echo -n > /etc/nginx/sites-available/default'
```
Open the nginx config file
```
sudo vi /etc/nginx/sites-available/default
```

Then paste the following
```
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

upstream backend {
    server 127.0.0.1:8501;
    keepalive 64;
}

server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Restart your nginx server
```
sudo service nginx restart
```
You should now be able to view your external URL without the port number.

## Custom Domain on HTTP
Sign up for an account on [noip.com](https://www.noip.com/)

Create a host name, I used chatwith.hopto.org. Keep all default settings and enter the EC2 External URL for the IPv4 address requested (for example 3.91.241.72).

Now if you navigate to your new custom domain you should see your streamlit application


## HTTPS

Install the certbot
```
sudo apt install certbot -y
```

Stop Nginx so the certbot can run
```
sudo service nginx stop
```

Create a certificate for your domain, for example mine would look like
```
sudo certbot certonly --standalone -d chatwith.hopto.org
```

Start nginx again
```
sudo service nginx start
```

Clear the current configuration of nginx
```
sudo sh -c 'echo -n > /etc/nginx/sites-available/default'
```
Open the nginx config file
```
sudo vi /etc/nginx/sites-available/default
```

Paste the following. ⚠️ Be sure to use your custom domain name instead of mine.
```
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

upstream backend {
    server 127.0.0.1:8501;
    keepalive 64;
}

server {
    listen 80;
    server_name chatwith.hopto.org;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name chatwith.hopto.org;

    ssl_certificate /etc/letsencrypt/live/chatwith.hopto.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/chatwith.hopto.org/privkey.pem;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Restart your nginx server
```
sudo service nginx restart
```
