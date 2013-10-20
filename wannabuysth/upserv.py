from fabric.api import run, settings, cd, env, hosts

@hosts(['125.65.46.33'])
def update():
    env.user = 'root'
    env.password = '_]jK"r`5(}7LaidA'
    with cd('/www/webdoc/wannabuysth/wannabuysth'):
        run("git pull")
        run("supervisorctl restart app")
     

