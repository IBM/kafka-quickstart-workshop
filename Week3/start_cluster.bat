rmdir /S /Q C:\tmp
Del /F /Q logs\*
start cmd.exe /k "C:\kafka_2.13-2.7.0\bin\windows\zookeeper-server-start.bat \C:\kafka_2.13-2.7.0\config\zookeeper.properties"
start cmd.exe /k "C:\kafka_2.13-2.7.0\bin\windows\kafka-server-start.bat C:\kafka_2.13-2.7.0\config\server0.properties"
start cmd.exe /k "C:\kafka_2.13-2.7.0\bin\windows\kafka-server-start.bat C:\kafka_2.13-2.7.0\config\server1.properties"
start cmd.exe /k "C:\kafka_2.13-2.7.0\bin\windows\kafka-server-start.bat C:\kafka_2.13-2.7.0\config\server2.properties"

