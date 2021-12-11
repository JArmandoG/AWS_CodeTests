# First approach to using Pulumi for AWS IaC deployments with Python

## First steps:
Get Pulumi access keys for deployment

! Use a virtual environment. At the end do
´´´pip freeze | tee requirements.txt´´´

---

## Pulumi commands
´´´pulumi new python´´´
(Creates a new project with all the dependencies, ready to work before installing and getting the venv running)
´´´pulumi config set aws:region us-east-2´´´
´´´pulumi config set this-project:siteDir www´´´
(Set "siteDir" variable to point to www, to be used programatically by config.require() function. This is ONLY a "www" string, not the contents of the actual www directory)

´´´pulumi up´´´

(Runs and applies changes)

´´´pulumi stack init prod´´´
(Creates another stack for "prod"; a "branch")
´´´pulumi set aws:region same-or-other-region-east-1´´´
´´´pulumi config set this-project:siteDir www´´´

´´´pulumi destroy´´´
(Destroy the present stack's objects including "prod" variables and data, and also AWS objects & Infra created)

---

To-Do: Deploy an AWS s3 log aggregator