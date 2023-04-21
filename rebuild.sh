IMAGE_NAME=upload-server
CONTAINER_NAME=upload-server

docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}

docker build -f Dockerfile . -t ${IMAGE_NAME}

LISTEN_PORT=8000
HOST_PORT=8888
UPLOADED_FILES_DIR=/data/uploaded-files

docker run -d -p $HOST_PORT:$LISTEN_PORT \
	-v $UPLOADED_FILES_DIR:/upload-data \
	--env http-listen-address=0.0.0.0 \
        --env http-listen-port=${LISTEN_PORT} \
        --env data-dir=/upload-data \
       	--name ${CONTAINER_NAME} ${IMAGE_NAME}

