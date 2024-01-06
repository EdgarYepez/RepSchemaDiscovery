# Pull LTS version of linux.
FROM ubuntu:20.04
RUN echo 'root:root' | chpasswd

# Install software dependencies, like MongoDB and Angular,
# according to the required versions. It also registers the corresponding
# repository to install NodeJS version 16. Due to the deprecation state
# of NodeJS 16, this step shows a warning during installation and delays
# the process by 60 seconds, after which the installation continues on.
RUN apt-get update \
    && apt-get -y dist-upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential \
        ca-certificates \
        curl \
        git \
        gnupg \
        mongodb \
        patch \
        texlive-base \
        texlive-latex-base \
        texlive-xetex \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update -yq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
        nodejs \
    && npm install -g @angular/cli@13.0.0 \
    && npm install -g typescript

# Create a working directory and access into it.
RUN mkdir -p /home/repro_project
WORKDIR /home/repro_project

# Clone the JSONSchemaDiscovery repository and reset its HEAD to
# the latest commit close to the date of the current reproduction experiment:
# January 5th, 2024.
RUN git clone https://github.com/gbd-ufsc/JSONSchemaDiscovery.git
WORKDIR /home/repro_project/JSONSchemaDiscovery
# The c70f4ab commit dates back to January 29th, 2023.
RUN git reset --hard c70f4ab

# Copy and apply code patches.
RUN mkdir -p ./patches
COPY patches ./patches
RUN patch < patches/package.json.diff package.json
RUN patch < patches/angular.json.diff angular.json
RUN patch < patches/proxy.conf.json.diff proxy.conf.json
RUN patch < patches/user.ts.diff server/models/user/user.ts
RUN patch < patches/app.ts.diff server/app.ts
RUN patch < patches/rawSchemaBatch.ts.diff server/controllers/rawSchema/rawSchemaBatch.ts
RUN rm -rf patches

# Install code dependencies.
RUN npm install -f
RUN npm install -f @types/ws@8.5.4
RUN npm install -f --save dotenv

# Copy and apply dependency patches.
RUN mkdir -p ./node_patches
COPY node_patches ./node_patches
RUN patch < node_patches/main.d.ts.diff node_modules/dotenv/lib/main.d.ts
RUN rm -rf node_patches

# Build the application.
RUN ng build

# Copy smoke.sh script.
COPY smoke .
RUN chmod +x smoke.sh

# Clone repository for source data for experiments
RUN git clone https://github.com/mmathioudakis/geotopics.git
WORKDIR /home/repro_project/JSONSchemaDiscovery/geotopics
# The 51ac0a8 commit dates back to June 15th, 2016.
RUN git reset --hard 51ac0a8

# Move data files to a dedicated location and delete cloned repository
WORKDIR /home/repro_project/JSONSchemaDiscovery
RUN mkdir ./data_source
RUN mv ./geotopics/data/* ./data_source
RUN rm -rf geotopics/

# Clone LaTeX report repository
RUN git clone https://github.com/EdgarYepez/RepSchemaDiscovery-Report.git
RUN mv RepSchemaDiscovery-Report/ report