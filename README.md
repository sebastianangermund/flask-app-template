Tut on docker: https://dev.to/sre_panchanan/how-to-dockerize-a-flask-application-4mi

# build and deploy

gcloud auth application-default login
gcloud auth configure-docker europe-north1-docker.pkg.dev

docker build --platform linux/amd64 -t escape/flask-app:v1.0.0 .
docker run --name my-flask-server -p 8080:8080 escape/flask-app:v1.0.0
docker tag <image> europe-north1-docker.pkg.dev/my-project-344409/docker-images/flask-app:v1.0.0
docker push <tag>