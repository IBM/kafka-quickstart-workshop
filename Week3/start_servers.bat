rmdir /S /Q C:\tmp
Del /F /Q logs\*
start cmd.exe /k "bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties"
start cmd.exe /k "bin\windows\kafka-server-start.bat .\config\server0.properties"
start cmd.exe /k "bin\windows\kafka-server-start.bat .\config\server1.properties"
start cmd.exe /k "bin\windows\kafka-server-start.bat .\config\server2.properties"
sleep 5
start cmd.exe /k "bin\windows\kafka-topics.bat --bootstrap-server "localhost:9092,localhost:9192,localhost:9292" --create --replication-factor 3 --partitions 1 --topic streams-plaintext-input"

