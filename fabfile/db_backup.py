from fabric.api import local, task
from datetime import date


@task
def db_backup():
    local('docker start db_eb_postgres')
    local('docker start redis_cache')
    local('docker start eburyroot_django')
    local((
        'docker exec -i -t db_eb_postgres pg_dump -U postgres postgres'
        ' > db_backup/bck_{}.psql'
    ).format(date.today().strftime('%Y%m%d')))
