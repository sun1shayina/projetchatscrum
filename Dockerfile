#Dockerfile basev3 (building on top of basev1)
FROM docker.io/showpopulous/chatscrum_img_base2:basev2
#FROM docker.io/showpopulous/chatscrum_img_base3:basev3

######################## HOLD ON  ##########################################
# If all you need to do is to run chatscrum,
# then you do not need to build a new image, just run existing image with the following
# docker pull docker.io/showpopulous/chatscrum_img_base3:basev3 
# NOTE: edit chatscrum_img:basevi to fit the latest version for your use
# If you don't already have a database, install mysql and create a database called chatscrum
# mkdir /web && cd /web
# copy chatscrum artifacts to /web, untar it there
# mkdir /web/www && cd /web/www
# git init .
# git remote add origin https://gitlab.com/showpopulous/scrumastr.git
# git pull
# cd /web/www/Django/ScrumMaster
# python3.6 manage.py makemigrations
# python3.6 manage.py migrate
# run chatscrum with this: docker run -p 5000:5000 --name chatscrum_ci local/chatscrum_img_base2
# type the ip address of your server into your browser and you should see chatscrum

####### Troubleshooting Tips
# to test mysql connection problems if you are using mysql.connect.django: 
# -- from container, import mysql.connector, then conn = mysql.connector.connect(host='xx',database='xx',password='xx')
# 

####### If you are rebuilding the chatscrum image 
# your machine must be minimum 12G
# create extra swap of minimum 640Mb
# In this dockerfile, suppose your IP is 2.2.2.2, replace ci.chatscrum.com with your ip. You should have 2.2.2.2:5000 below
# pull and run a redis image. For example:
# in the even that you have rebuilt the image, make sure db user linuxjobber can access your database, then run the command below:
# docker run -d -p 5000:5000 -p 5100:5100 -e "DATABASE_URL=mysql://linuxjobber:8iu7*IU&@lj_db" -e "SESSION_DEFAULTS=database" --link lj_db --name history_image   

MAINTAINER The CentOS Project <cloud-ops@centos.org>

LABEL Vendor="CentOS" \
      License=GPLv2 \
      Version=2.4.6-40


RUN mkdir -p /web/
COPY www/ /web/www/
COPY nginx.conf /etc/nginx/
COPY package.json /web
COPY start.sh /start.sh
COPY settings.py /web/www/Django/ScrumMaster/ScrumMaster/settings.py
RUN chmod +x /start.sh

RUN rm -rf /web/Chatscrum-Angular && yum install -y nodejs && yum install -y gcc-c++ make && cd /web && npm install
RUN git config --global user.email "joseph.showunmi@linuxjobber.com" && \
 git config --global user.name "joseph.showunmi" && \
 cd /web && . $HOME/.nvm/nvm.sh && ng new Chatscrum-Angular --routing && \
 pip3.6 install Pillow channels_redis

RUN . $HOME/.nvm/nvm.sh && yes | cp -r /web/www/Angular/* /web/Chatscrum-Angular/src && \
 cd /web/Chatscrum-Angular/ && sed -i '26s/.*/"src\/styles.css","node_modules\/materialize-css\/dist\/css\/materialize.min.css"/' angular.json; 
RUN cd /web/Chatscrum-Angular/ && sed -i '28s/.*/"scripts": ["node_modules\/jquery\/dist\/jquery.min.js","node_modules\/materialize-css\/dist\/js\/materialize.min.js"]/' angular.json; sed -i '19s/.*/],"types": ["jquery","materialize-css"]/' tsconfig.json;
RUN cd /web/Chatscrum-Angular/ && sed -i 's/127.0.0.1:8000/ci.chatscrum.com:5000/' src/app/data.service.ts;
#RUN ls /web/Chatsrum-Angular && \
# cat /web/Chatscrum-Angular/src/app/profile/profile.component.html
RUN cd /web/Chatscrum-Angular && . $HOME/.nvm/nvm.sh && npm install ngx-materialize materialize-css@next ng2-dragula rxjs && ng build --prod --aot
RUN yes | cp -r /web/Chatscrum-Angular/dist/Chatscrum-Angular/assets/ /web/Chatscrum-Angular/dist/Chatscrum-Angular/src/ && \
yes | cp -r /web/Chatscrum-Angular/dist/Chatscrum-Angular/* /usr/share/nginx/web/Chatscrum-Angular

#RUN cd /web/www/Django/ScrumMaster/ && /bin/python3.6 manage.py makemigrations && /bin/python3.6 manage.py migrate
#RUN cd /web/www/Django/ScrumMaster/ && /bin/python3.6 manage.py runserver 0.0.0.0:5000

RUN touch /etc/uwsgi.d/chatscrum.ini && echo "[uwsgi]" > /etc/uwsgi.d/chatscrum.ini
RUN echo "socket = /run/chatscrumuwsgi/uwsgi.sock" >> /etc/uwsgi.d/chatscrum.ini && echo "chmod-socket = 775" >> /etc/uwsgi.d/chatscrum.ini
RUN echo "chdir = /web/www/Django/ScrumMaster" >> /etc/uwsgi.d/chatscrum.ini && echo "master = true" >> /etc/uwsgi.d/chatscrum.ini && RUN echo "module = ScrumMaster.wsgi:application" >> /etc/uwsgi.d/chatscrum.ini
RUN echo "uid = uwsgi" >> /etc/uwsgi.d/chatscrum.ini && echo "gid = uwsgi" >> /etc/uwsgi.d/chatscrum.ini
RUN echo "processes = 1" >> /etc/uwsgi.d/chatscrum.ini && echo "threads = 1" >> /etc/uwsgi.d/chatscrum.ini && echo "plugins = python36u,logfile" >> /etc/uwsgi.d/chatscrum.ini

RUN mkdir -p /run/chatscrumuwsgi/ && chgrp nginx /run/chatscrumuwsgi && chmod 2775 /run/chatscrumuwsgi && touch /run/chatscrumuwsgi/uwsgi.sock

#for basev2, container nginx should be running on port 5000 so that host nginx can run on 80
EXPOSE 5000 5100

ENV APP_ROOT=/web
ENV PATH=${APP_ROOT}/bin:${PATH} HOME=${APP_ROOT}
COPY bin/ ${APP_ROOT}/bin/
RUN chmod -R u+x ${APP_ROOT}/bin && \
    chgrp -R 0 ${APP_ROOT} && \
    chmod -R g=u ${APP_ROOT} /etc/passwd

### Containers should NOT run as root as a good practice
USER 10001
WORKDIR ${APP_ROOT}

### user name recognition at runtime w/ an arbitrary uid - for OpenShift deployments
ENTRYPOINT [ "uid_entrypoint" ]
VOLUME ${APP_ROOT}/logs ${APP_ROOT}/data
CMD ["/start.sh"]
