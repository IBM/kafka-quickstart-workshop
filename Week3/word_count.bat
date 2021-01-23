cd C:\src\kafka-2.7.0-src

START /b /wait cmd /C "gradle assemble -x clients:javadoc streams:test-utils:javadoc streams:streams-scala:scaladoc connect:mirror-client:javadoc connect:api:javadoc core:javadoc core:compileScala"

pause

COPY "C:\src\kafka-2.7.0-src\streams\examples\build\libs\kafka-streams-examples-2.7.0.jar" "C:\kafka_2.13-2.7.0\libs"

cd C:\kafka_2.13-2.7.0

start cmd.exe /k "bin\windows\kafka-run-class.bat org.apache.kafka.streams.examples.wordcount.WordCountDemo"
