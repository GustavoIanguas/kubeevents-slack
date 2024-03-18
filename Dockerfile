FROM python:3.9

WORKDIR /app

#install gcloud
RUN apt update && apt-get install apt-transport-https ca-certificates gnupg curl -y
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get update && apt-get install google-cloud-cli -y
RUN apt update && apt-get install google-cloud-cli-gke-gcloud-auth-plugin -y 
RUN gcloud --version

#install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
RUN kubectl version --client

COPY . .

#get config file
RUN gcloud auth login --cred-file=service-account.json
RUN gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project civic-replica-408912

#test config
RUN kubectl get pods -n default

RUN pip install -r requeriments.txt

EXPOSE 5000

CMD [ "python3", "app.py"]