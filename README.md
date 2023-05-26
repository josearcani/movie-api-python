# Movie API with fastAPI

install all packages

```sh
pip install -r requirements.txt
```

Run project
```sh
uvicorn main:app --reload
```

ALtenative to SQLalchemy
SQLMODEL 



test these commands in a VM

```sh
# Pasos para hacer el 
upt update

upt -y upgrade


#instalar python y git
python3 -V

git --version


# instalar ngnex
apt install nginx

# ejecutar la app con el servidor
nodejs --version

apt install nodejs

# Instalar para ejecutar la aplicaciooon
apt install npm

#instalar globalmente 
npm install pm2@lastest -g

# Aqui debe salir la aplicación de python.
pm2 list

# instalar el entorno virtual 
apt install python3-venv


#Crear y activar el intorno virtual
python3 -m venv venv
source venv/vim/activate

pip install -r requirements.txt
```
https://railway.app/pricing



```
pm2 start "uvicorn main:app --port 5000 --host 0.0.0.0" --name my-movie-api

deactivate out of venv

nano /etc/nginx/sites-enabled/my-movie-api


server {
        listen 80;
        server_name 104.248.228.181;
        location / {
                proxy_pass http://127.0.0.1:5000;
        }

}

save and exit 

systemctl status nginx

systemctl restart nginx
```