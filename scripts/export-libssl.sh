#!/bin/sh 
#
# Older versions of mesos or DC/OS send relative paths
# for the LIBPROCESS_SSL_ environment variables. This
# script tries to detect that and prepend the env vars
# with the MESOS_SANDBOX value. This results in an 
# absolute path to the needed SSL certificates.

# check if the SSL file exists and if not assume it needs
# the MESOS_SANDBOX prefix.
fix_ssl_var()
{
	local var_name=\$"$1"
	local var_val=`eval "expr \"$var_name\""`
	if [ ! -f $var_val ]; then
		eval "$1=\"$MESOS_SANDBOX/$var_val\""
	fi
}

fix_ssl_var LIBPROCESS_SSL_CA_FILE
fix_ssl_var LIBPROCESS_SSL_CERT_FILE
fix_ssl_var LIBPROCESS_SSL_KEY_FILE

# pass on new values
export LIBPROCESS_SSL_CA_FILE LIBPROCESS_SSL_CERT_FILE LIBPROCESS_SSL_KEY_FILE

