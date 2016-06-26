#!/bin/sh
#settle 8081 shut:8006 ajp:8110
#order 8082 shut:8007 ajp:8111
#message 8083 shut:8008 ajp:8112
#paysystem 8084 shut:8009 ajp:8113
#app 8085 shut:8010 ajp:8114
#hsapp 8086 shut:8011 ajp:8115
#databiz 8087 shut:8012 ajp:8116
#econtract 8088 shut:8013 ajp:8117
#searcher 8089 shut:8014 ajp:8118
#searchermaster 8090 shut:8015 ajp:8119


while read app_name start_port shut_port ajp_port
do
	APP_NAME=$app_name
	START_UP_PORT=$start_port
	SHUT_DOWN_PORT=$shut_port
	AJP_PORT=$ajp_port
	cp -rf /opt/srvs/settle /opt/srvs/$APP_NAME
	rm -rf /opt/srvs/$APP_NAME/bin/tomcat.pid
	#rm dir(ROOT)
	rm -rf /opt/srvs/$APP_NAME/webapps/ROOT/
	#rm logs's children,not dir(logs)
	rm -rf /opt/srvs/$APP_NAME/logs/*
	sed -i '4 s/settle/'''$APP_NAME'''/g' /opt/srvs/$APP_NAME/bin/setenv.sh
	sed -i '22 s/8006/'''$SHUT_DOWN_PORT'''/' /opt/srvs/$APP_NAME/conf/server.xml
	sed -i '69 s/8081/'''$START_UP_PORT'''/' /opt/srvs/$APP_NAME/conf/server.xml 
	sed -i '91 s/8110/'''$AJP_PORT'''/' /opt/srvs/$APP_NAME/conf/server.xml
	sed -i '124 s/settle/'''$APP_NAME'''/g' /opt/srvs/$APP_NAME/conf/server.xml
	if [ ! -d "/opt/webapps-$APP_NAME" ];then
		mkdir /opt/java/webapps-$APP_NAME -p
	fi
	ln -s /opt/srvs/$APP_NAME/bin/startup.sh /opt/${APP_NAME}_startup.sh
	ln -s /opt/srvs/$APP_NAME/bin/shutdown.sh /opt/${APP_NAME}_shutdown.sh
        ln -s /opt/java/webapps-$APP_NAME webapps-$APP_NAME
	#/sbin/iptables -I INPUT -p tcp --dport $START_UP_PORT -j ACCEPT
	#/etc/rc.d/init.d/iptables save
done < tomcat_port.txt

##remove settle project template
echo "remove /opt/srvs/order/ /opt/srvs/settle/ /opt/srvs/settle.tgz"
rm -rf /opt/srvs/order/ /opt/srvs/settle/ /opt/srvs/settle.tgz
