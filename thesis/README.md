

## Quick Start

This section describes how to run YCSB on the Thesis database.

### 1. Set Up YCSB

Clone the YCSB git repository and compile:

    git clone git://github.com/brianfrankcooper/YCSB.git
    cd YCSB
    mvn -pl site.ycsb:thesis-binding -am clean package -DskipTests=True

    mvn -pl site.ycsb:thesis-binding -am clean package -DskipTests=True -Dcheckstyle.skip

### 2. Load Data
Run the following command to load data:

    python3 bin/ycsb load thesis -P workloads/workloada -p thesis.ip=http://<ip-here>:8080
