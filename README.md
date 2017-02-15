#Fanmail

An email to let you know the fans are running above a certain rpm

Ensure a valid SES sending email address is specified

Emails will be sent if one fan is running above MAX_RPM

## ~/.bashrc for standalone use

export SES_SENDER='sending_email@anothermailservice.com'

export SES_DEST='dest_email@somemailservice.com'

export MAX_RPM='2500'

export AWS_ACCESS_KEY_ID=''

export AWS_SECRET_ACCESS_KEY=''

export AWS_DEFAULT_REGION=''


## systemD for use as a service

edit /etc/sysconfig/fanmail and add the ENV vars

SES_SENDER='sending_email@anothermailservice.com'

SES_DEST='dest_email@somemailservice.com'

MAX_RPM='2500'

AWS_ACCESS_KEY_ID=''

AWS_SECRET_ACCESS_KEY=''

AWS_DEFAULT_REGION=''

## service

change paths in fanmail.service to match absolute location of this repo

ExecStart and WorkingDirectory

sudo cp fanmail.service /etc/systemd/system

sudo systemctl enable fanmail.service

sudo systemctl preset fanmail.service

## service operations

sudo service fanmail start|stop|restart|status

##AWS & python Requirements

apt install python3-pip

pip3 install awscli

you'll need to have a valid email account setup on AWS SES 

##Dell Requirements

###OpenManage

http://linux.dell.com/repo/community/ubuntu/

