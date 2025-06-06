

## Quick Start

This section describes how to run YCSB on Solr running locally. 

### 1. Set Up YCSB

Clone the YCSB git repository and compile:

    git clone git://github.com/brianfrankcooper/YCSB.git
    cd YCSB
    mvn -pl site.ycsb:thesis-binding -am clean package -DskipTests=True

    mvn -pl site.ycsb:thesis-binding -am clean package -DskipTests=True -Dcheckstyle.skip
