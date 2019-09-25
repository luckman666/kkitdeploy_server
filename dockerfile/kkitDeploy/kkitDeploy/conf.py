

# Redis配置
REDIS_HOST = 'kkitredis'
REDIS_PORT = '6379'
REDIS_SPACE = '0'
REDIS_PASSWD = 'root1234'

deployMenu = {
            'database':{'mysql':['mysql','mysql_repliaction','mysql_pxc'], 'redis':['redis','redis_sentinel'],'mongo':['mongo','mongo_sharding'],
                              'postgreSQL':['PostgreSQL','postgreSQL_streaming','postgreSQL_pgpool]']},
            'proxy':{'nginx':['nginx','nginx_keepalived'],
                            'haproxy':['haproxy','haproxy_keepalived']},
            'container':{'k8s':['k8s1.13.1','k8s1.14.1','k8s1.15.0'],'swarm':['swarm'],'docker':['docker_and_compose']},
            'storage':{'ceph':['ceph_luminous']},
                       'other':{'other':['glpi','mutual_trust']}
        }



