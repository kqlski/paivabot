# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster as base

# Setup ENV variables here (if needed in the future)


FROM base as python-deps

# Install pipenv
RUN pip3 install pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Setup workdir
WORKDIR /bot

# Install app into container
COPY . .
#generate prisma
RUN prisma generate

# Create a non-root user and add permission to access /bot folder
RUN adduser -u 5678 --disabled-password --gecos "" botuser
RUN chown -R botuser /bot
USER botuser

# Run the app
CMD [ "python3", "bot.py" ]
