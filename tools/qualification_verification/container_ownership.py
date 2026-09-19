"""One ownership vocabulary for protected launch and disposable-host cleanup.

Labels narrow discovery; durable dispatch, exact name, image and container ID
establish the relationship. A label alone never authorizes retirement.
"""
import re

HOST_LABEL = 'fp.qualification.host'
EXECUTION_LABEL = 'org.first-passage.qualification.execution'
BUILD_LABEL = 'fp.qualification.build'


def host_identity(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{32}',value) is None:
        raise ValueError('owned container host identity differs')
    return value


def owned_containers(rows, executions, *, run_id, image_id, release_sha256):
    host_identity(run_id)
    if (type(image_id) is not str or re.fullmatch('sha256:[0-9a-f]{64}',image_id) is None
            or type(release_sha256) is not str or re.fullmatch('[0-9a-f]{64}',release_sha256) is None
            or type(rows) is not list or type(executions) is not list):
        raise ValueError('owned container enrollment differs')
    try:
        dispatches={}
        for execution in executions:
            name=execution['execution_id']
            if (type(name) is not str or re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]{0,127}',name) is None
                    or name in dispatches or execution['release_sha256']!=release_sha256):
                raise ValueError('owned container dispatch differs')
            recorded=execution['container_id']
            if recorded is not None and (type(recorded) is not str or re.fullmatch('[0-9a-f]{64}',recorded) is None):
                raise ValueError('owned container recorded identity differs')
            dispatches[name]=recorded
        result=[]
        for row in rows:
            container=row['Id']
            labels=row['Config']['Labels']
            name=labels[EXECUTION_LABEL]
            if (type(container) is not str or re.fullmatch('[0-9a-f]{64}',container) is None
                    or container in result or labels[HOST_LABEL]!=run_id or name not in dispatches
                    or row['Name']!='/qexec-'+name or row['Image']!=image_id or row['Config']['Image']!=image_id
                    or dispatches[name] not in (None,container)):
                raise ValueError('owned container identity differs')
            result.append(container)
        return tuple(sorted(result))
    except (KeyError,TypeError) as exc:
        raise ValueError('owned container inventory malformed') from exc

def campaign_host_slice(run_id):
    """Shared identity producer for diagnostic runtime and administrator cleanup."""
    import hashlib
    if type(run_id) is not str or re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]{0,127}',run_id) is None:
        raise ValueError('campaign host identity differs')
    return 'fpq' + hashlib.sha256(run_id.encode()).hexdigest()[:16] + '.slice'


def campaign_scopes(run_id, attempt, work):
    import hashlib
    import json
    for value in (attempt,work):
        if type(value) is not str or re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]{0,127}',value) is None:
            raise ValueError('campaign work identity differs')
    parent=campaign_host_slice(run_id)[:-6]
    campaign=parent+'-'+hashlib.sha256(attempt.encode()).hexdigest()[:24]
    scoped=campaign+'-'+hashlib.sha256(work.encode()).hexdigest()[:24]
    identity=json.dumps([run_id,attempt,work],separators=(',',':'),ensure_ascii=False).encode()
    return dict(campaign_slice=campaign+'.slice',work_slice=scoped+'.slice',payload_slice=scoped+'-payload.slice',
                guardian_unit=parent+'guardian'+hashlib.sha256(identity).hexdigest()+'.service')

# '--' ends busctl's option parsing: GNU getopt permutes, so the guardian's
# ExecStart values ('-I', '--attempt', '--work') would otherwise be read as
# busctl options ("invalid option -- 'I'", first --s2 run 35456019676).
CAMPAIGN_BUS_START = ('/usr/bin/busctl', '--system', '--no-pager', '--timeout=5s', '--', 'call',
    'org.freedesktop.systemd1', '/org/freedesktop/systemd1', 'org.freedesktop.systemd1.Manager',
    'StartTransientUnit', 'ssa(sv)a(sa(sv))')
