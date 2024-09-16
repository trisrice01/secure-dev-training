#!/bin/bash

source /etc/apache2/envvars

#!/bin/bash
exec service ssh start &
exec apache2-foreground
