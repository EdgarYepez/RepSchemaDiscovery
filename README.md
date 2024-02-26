# Experiment Replication: JSON Schema Discovery

This repository aims at replicating the experiment regarding correctness and completeness of the JSON-document to JSON-schema mappings formulated in the paper by Frozza A. et al. The paper, available at https://ieeexplore.ieee.org/document/8424731, is associated with a public repository at https://github.com/gbd-ufsc/JSONSchemaDiscovery, from where code artefacts for the hereby purpose were pulled. The code artefacts correspond to a web application built on the MongoDB, Express, Angular and Node (MEAN) stack.

The source code, data, and/or other artefacts related to the current repository have been made available on Zenodo at DOI 10.5281/zenodo.10702962.

## Organisation

This repository bundles a Docker configuration file to pull the code artefacts and prepare the experiment setup. Alongside the configuration file, patches to the code artefacts are organised in a dedicated directory named `patches`. Additionally, a script named `doAll.sh` is provided to check for the correct installation of the code artefacts.

## Usage

A stable installation of Docker is required to use this repository.

This repository can be used by building the experiment image and container from source, or by importing the pre-built binary container.

### Building from source

Build a Docker image from the provided configuration file with the following command:

```
docker build -t json-rep . --no-cache
```

The image will be created with the appropriate versions of the MEAN stack, namely Angular v13.3.11 and Node v16.20.2, as well as the code artefacts from the aforementioned original repository. To guarantee a seamless execution of the upcoming steps and the overall experiment execution, the configuration file will automatically reset the code artefacts to their latest commit close to the date of the current reproduction setting. Next, the patches will be applied to the code artefacts as accordingly, and the application will be built. See `Dockerfile` for more details. Finally, the repository for the associated document report will be automatically cloned into a directory named `report`. Refer to the up next Report section for additional information.

**Note:**  Due to the deprecation state of Node v16.x, the image building process shows a "SCRIPT DEPRECATION" warning and is delayed by 60 seconds in between execution. The process continues on, however, after said time span elapses.

Run an interactive Docker container based on the recently created image with the following command:

```
docker run -it --name json-rep json-rep bash
```

The container will boot up directly to the code artefacts directory, named `JSONSchemaDiscovery`, from where the whole prepared setup and experiment can be executed by running the `doAll.sh` script. Refer to the up next Experiment section for additional information.

### Importing the binary container

Download the pre-built binary container from the repository artefacts link (Zenodo) and use the following command to import it over as a Docker image.

```
docker import json-schema-experiment-replication_bin.tar json-rep:latest
```

Run an interactive Docker container based on the recently imported image with the following command:

```
docker run -it --name json-rep json-rep bash
```

The container will boot up to the root directory `/`. From here, access the main experiment directory using the following command:

```
cd /home/repro_project/JSONSchemaDiscovery/
```

From this directory the whole prepared setup and experiment can be executed by running the `doAll.sh` script. Refer to the up next Experiment section for additional information.

## Experiment

The experiment to be conducted aim at evaluating the correctness and completeness of the JSON-document to JSON-schema mappings as stated by the paper's authors. To that end, an example dataset is automatically pulled during setup preparation and placed into a file named `firenze_checkins.json` inside a `data_source` directory. The dataset consists of a collection of 900 JSON documents from Foursquare about check-ins in the city of Florence. All documents in the collection contained the following fields, each of which is mandatory.

- `_id`: A unique identifier for the check-in.
- `foursquareURL`: The public Foursquare URL for the check-in.
- `venueId`: A unique identifier for the venue where the check-in was performed.
- `timestamp`: The posix timestamp of the check-in.
- `foursquareUserId`: A unique identifier for the associated user.
- `timeZoneOffset`: The number of minutes offset from Greenwich time.
- `swarmULR`: Is the public Swarm URL for the check-in.

The experiment execution consists of a five-stage process, which is all initiated and carried out by executing the `doAll.sh` script.

### Execution

1. **Environment preparation:** During this stage, all running processes in the container operating system are terminated in order to guarantee a clean execution of the experiment. Then, the 900 JSON documents from the `firenze_checkins.json` file are uploaded to a database called `repeng` in the installed instance of the MongoDB server.
2. **Application execution:** In this stage, the main web application is initiated by concurrently bootstrapping both the Angular client side and the Express server side. To ensure a successful initialisation of the web application, the script halts for 120 seconds during this stage.
3. **Running a job:** In this stage, a python script called `main_experiment.py` is executed, which is responsible of communicating with the web application in order to initiate a JSON schema extraction job over the documents in the `repeng` database. Upon job completion, the extracted JSON schema is downloaded and stored inside the `experiment` directory with the name `firenze_checkins_generated_schema.json`.
4. **Schema comparison:** In this stage, yet another python script, called `json_deepdiff.py`, is executed, which performs a deep difference comparison between the just extracted JSON schema and the ground-truth JSON schema named `firenze_checkins_reference_schema.json` also located in the `experiment` directory. The resulting difference output as well as a summary are stored in the `experiment` directory with names `firenze_checkins_diff.json` and `firenze_checkins_summary.txt` respectively.
5. **Report generation:** This is the final stage, where the difference output and summary files from the previous stage are used to generate a LaTeX report describing the obtained results.

## Report

In order to successfully build the LaTeX report, the experiment must be carried out as described in the Execution section. The report is the accessible inside the `report` directory with the name `main.pdf`. For report source code, refer to the repository at https://github.com/EdgarYepez/RepSchemaDiscovery-Report.

## License

This repository is governed by the MIT license. For the official statement and details, see https://opensource.org/license/mit/.
