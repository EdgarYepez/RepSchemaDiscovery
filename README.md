# Experiment Reproduction: JSON Schema Discovery

This repository aims at reproducing the experiment regarding correctness and completeness of the JSON-document to JSON-schema mappings formulated in the paper by Frozza A. et al. The paper, available at https://ieeexplore.ieee.org/document/8424731, is associated with a public repository at https://github.com/gbd-ufsc/JSONSchemaDiscovery, from where code artefacts for the hereby purpose were pulled. The code artefacts correspond to a web application built on the MongoDB, Express, Angular and Node (MEAN) stack.

## Organisation

This repository bundles a Docker configuration file to pull the code artefacts and prepare the experiment setup. Alongside the configuration file, patches to the code artefacts are organised in dedicated directories named with a `patches` suffix. Additionally, a script named `smoke.sh` is provided to check for the correct installation of the code artefacts.

## Usage

A stable installation of Docker is required to use this repository.

Clone the repository and build a Docker image from the provided configuration file with the following command:

```
docker build -t json-rep . --no-cache
```

The image will be created with the appropriate versions of the MEAN stack, namely Angular v13.3.11 and Node v16.20.2, as well as the code artefacts from the aforementioned original repository. To guarantee a seamless execution of the upcoming steps and the overall experiment execution, the configuration file will automatically reset the code artefacts to their latest commit close to the date of the current reproduction setting. Next, the patches will be applied to the code artefacts as accordingly, and the application will be built. See `Dockerfile` for more details. Finally, the repository for the associated document report will be automatically cloned into a directory named `report`. Refer to the up next Experiments section for additional information.

**Note:**  Due to the deprecation state of Node v16.x, the image building process shows a "SCRIPT DEPRECATION" warning and is delayed by 60 seconds in between execution. The process continues on, however, after said time span elapses.

Run an interactive Docker container based on the recently created image with the following command:

```
docker run -it --name json-rep json-rep bash
```

The container will boot up directly to the code artefacts directory, named `JSONSchemaDiscovery`, from where the whole prepared setup can be checked by executing the `smoke.sh` script.

### Checking setup

Since the prepared setup corresponds to a web application, the `smoke.sh` script fires the `ng serve &` command to start the web application up in a background process. As the `ng serve` command typically involves a long-running process, which does not exit until manually stopped, it is not possible for the script to check for a successful exit status of the command. In turn, the script will only check whether the command started successfully and keeps running for at least 120 seconds. This is considered as a sufficient criteria for checking the prepared setup since starting up and running the application involve a successful installation of dependencies as well as a successful compilation of the web application.

Execute the `smoke.sh` script with the following command:

```
./smoke.sh
```

After 120 seconds, upon successful execution of the script, the message `ng serve is running with process ID {{PID}}.` is shown; otherwise, the message `Failed to start ng serve.` is shown.

## Experiments

The experiments to be conducted aim at evaluating the correctness and completeness of the JSON-document to JSON-schema mappings as stated by the paper's authors. To that end, the example dataset cited in the paper is automatically pulled during setup preparation and placed into a directory named `data_source`. For details, refer to the report document repository at https://github.com/EdgarYepez/RepSchemaDiscovery-Report.

## License

This repository is governed by the MIT license. For the official statement and details, see https://opensource.org/license/mit/.
