CODE_DIR=$1
mkdir -p "$CODE_DIR"
cd "$CODE_DIR"

git clone -b rel/commons-csv-1.14.0 https://github.com/apache/commons-csv.git apache-commons-csv

git clone -b rel/commons-imaging-1.0.0-alpha5 https://github.com/apache/commons-imaging.git commons-imaging

git clone https://github.com/apache/commons-jxpath.git

git clone --branch version-2.1.4 https://github.com/dom4j/dom4j.git

git clone --branch v2.2.2 https://github.com/osiegmar/FastCSV.git fastcsv

git clone -b 2.0.57 https://github.com/alibaba/fastjson2.git fastjson2

git clone https://github.com/itext/itext-java.git itext7
cd itext7 && git checkout tags/7.2.5
cd ..

git clone https://github.com/jettison-json/jettison.git jettison

git clone -b json-flattener-0.16.0 https://github.com/wnameless/json-flattener.git

git clone https://github.com/OWASP/json-sanitizer.git

git clone -b tag_release_1_1_1 https://github.com/fangyidong/json-simple.git

git clone -b 2.5.1 https://github.com/netplex/json-smart-v2.git json-smart

git clone https://github.com/jhy/jsoup.git

git clone https://github.com/JSQLParser/JSqlParser.git jsqlparser
cd jsqlparser && git checkout tags/jsqlparser-4.8
cd ..

git clone https://github.com/drewnoakes/metadata-extractor.git metadata-extractor

git clone -b 2.1.0 https://github.com/rometools/rome.git

git clone -b woodstox-core-7.1.0 https://github.com/FasterXML/woodstox.git

git clone -b XSTREAM_1_4_20 https://github.com/x-stream/xstream.git xstream

git clone -b v2.9.0 https://github.com/srikanth-lingala/zip4j.git zip4j

git clone https://github.com/zeroturnaround/zt-zip.git zt-zip
cd zt-zip && git checkout tags/zt-zip-1.16
cd ..
