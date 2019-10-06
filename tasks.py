from invoke import task

@task
def bump_version(ctx, part, confirm=False):
    """
    Run : invoke bump-version {major, minor, patch} --confirm to actually perform the bump version 
    """
    if confirm:
        ctx.run('bumpversion {part}'.format(part=part))
    else:
        ctx.run('bumpversion --dry-run --allow-dirty --verbose {part}'.format(part=part))
        print('Add "--confirm" to actually perform the bump version.')

@task
def clean(c, docs=False, bytecode=False, extra=''):
    patterns = ['build']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))

@task
def build(c, docs=False):
    c.run("python setup.py build")
    if docs:
        c.run("sphinx-build docs docs/_build")

@task
def dist(c,):
    """
    Run : invoke dist to create a new dist
    """
    c.run("python setup.py sdist")

@task
def upload(c,):
    """
    Run : invoke upload to push the latest dist to pypi
    """
    c.run("twine upload dist/*")
