from fabric.api import local, task


@task
def test():
    local('docker start db_eb_testing')
    local('docker start eburyroot_django')
    local('docker exec -i -t eburyroot_django python manage.py test')
    local('docker stop db_eb_testing')
