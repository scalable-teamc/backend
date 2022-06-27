docker rmi teamc-controller &&
docker build -t teamc-controller .. &&
docker run -it --rm -p 5000:5000 teamc-controller &&
# -it runs container interactively, allowing the use of CTRL+C
# --rm makes it so that the container deletes itself after the process is done