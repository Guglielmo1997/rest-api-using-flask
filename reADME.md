Create an Image
docker build -t <nome_container> .

Run the Container 
docker run -d -p 5000:5000 -w /app -v "${pwd}:/app" <nome Container> 

-w - Current working directory of the container

-v - Linking the pwd(host) to work directory of the container 