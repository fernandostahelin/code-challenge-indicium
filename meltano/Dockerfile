# registry.gitlab.com/meltano/meltano:latest is also available in GitLab Registry
FROM meltano/meltano:v3.0-python3.10

WORKDIR /project

# Copy over Meltano project directory
COPY . .

RUN meltano install

# Don't allow changes to containerized project files
ENV MELTANO_PROJECT_READONLY=1

# Expose default port used by `meltano ui`
EXPOSE 5000

ENTRYPOINT ["meltano"]
