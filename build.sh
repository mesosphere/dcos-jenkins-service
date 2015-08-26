export COPYFILE_DISABLE=1
rm -f jenkins-on-mesos.tgz
mkdir jenkins-on-mesos
cp -r *.war jenkins-on-mesos
cp -r *.xml jenkins-on-mesos
cp -r plugins jenkins-on-mesos
tar czf jenkins-on-mesos.tgz jenkins-on-mesos
rm -rf jenkins-on-mesos