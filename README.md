jenkins-standalone
==================

Jenkins standalone instance package with the Mesos plugin with Docker support pre-installed.

git clone https://github.com/ahunnargikar/jenkins-standalone && cd jenkins-standalone;
export JENKINS_HOME=$(pwd);
java -jar jenkins.war --webroot=war --httpPort=$PORT0 --ajp13Port=-1 --httpListenAddress=0.0.0.0 --ajp13ListenAddress=127.0.0.1 --preferredClassLoader=java.net.URLClassLoader --logfile=../jenkins.log