import subprocess
import time
import os
from enum import Enum

class DockerStatus(Enum):
    STOPPED = 1
    RUNNING = 2
    RESTARTING = 3
    TIMED_OUT= 4
    ERROR = 5

class DockerImages(Enum):
    SQL_INJECTION = 1
    LOCAL_FILE_INCLUSION = 2
    COMMAND_INJECTION = 3
    STORED_XSS = 4

class DockerChallengeService:
    def __init__(self, app, challenge: DockerImages):
        self.app = app
        self._last_interact_time = time.time()
        self.container_status = DockerStatus.STOPPED
        self._docker_file = ""
        self.update_challenge(challenge)

    def __del__(self):
        if self.container_status == DockerStatus.RUNNING:
            self.stop_container()

    @staticmethod
    def init_app(app, challenge):
        return DockerChallengeService(app, challenge)

    def start_container(self):
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self._docker_file, "up", "-d", "--build"],
                check=True,
                text=True,
                capture_output=True
            )
            print("Docker-compose started successfully.")
            print(result.stdout)
            self.container_status = DockerStatus.RUNNING
        except subprocess.CalledProcessError as e:
            print("An error occurred while starting docker-compose:")
            print(e.stderr)
            self.container_status = DockerStatus.ERROR
        return ("localhost", self.challenge.value)

    def stop_container(self):
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self._docker_file, "-v", "down"],
                check=True,
                text=True,
                capture_output=True
            )
            print("Docker-compose stopped successfully.")
            print(result.stdout)
            self.container_status = DockerStatus.STOPPED
        except subprocess.CalledProcessError as e:
            print("An error occurred while stopping docker-compose:")
            print(e.stderr)
            self.container_status = DockerStatus.RUNNING

    def restart_container(self):
        self.container_status = DockerStatus.RESTARTING
        self.stop_container()
        self.start_container()

    def update_last_interact_time(self):
        self._last_interact_time = time.time()

    def timeout_container(self):
        MAX_TIME_SINCE_LAST_INTERACT_SECONDS = 30 * 60
        if (time.time() - self._last_interact_time) > MAX_TIME_SINCE_LAST_INTERACT_SECONDS:
            self.stop_container()
            self.container_status = DockerStatus.TIMED_OUT

    def update_challenge(self, challenge: DockerImages):
        if self.container_status == DockerStatus.RUNNING:
            self.stop_container()
        _DOCKER_CHALLENGE_FOLDER =  f"{os.getcwd()}/../development_challenges"
        self.challenge = challenge
        if self.challenge == DockerImages.SQL_INJECTION:
            self._docker_file = f"{_DOCKER_CHALLENGE_FOLDER}/SQL Injection/docker-compose.yml"
        elif self.challenge == DockerImages.LOCAL_FILE_INCLUSION:
            self._docker_file = f"{_DOCKER_CHALLENGE_FOLDER}/Local File Inclusion/docker-compose.yml"
        elif self.challenge == DockerImages.COMMAND_INJECTION:
            self._docker_file = f"{_DOCKER_CHALLENGE_FOLDER}/Command Injection/docker-compose.yml"
        elif self.challenge == DockerImages.STORED_XSS:
            self._docker_file = f"{_DOCKER_CHALLENGE_FOLDER}/Stored XSS/docker-compose.yml"