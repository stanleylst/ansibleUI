#!/bin/sh
TOMCAT_HOME=/opt/inst/
TOMCAT_VERSION=8.0.30
echo $TOMCAT_HOME
if [ ! -d "$TOMCAT_HOME" ];then
	echo "init tomcat"
	mkdir -p $TOMCAT_HOME
	cd $TOMCAT_HOME
	wget http://apache.fayea.com/tomcat/tomcat-8/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz
	tar -xzf apache-tomcat-$TOMCAT_VERSION.tar.gz	
	#mv apache-tomcat-$TOMCAT_VERSION tomcat
	ln -s apache-tomcat-$TOMCAT_VERSION tomcat
	echo "init tomcat end"
else
	echo "tomcat exists"
fi
