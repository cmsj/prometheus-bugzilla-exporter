from setuptools import setup

setup(name='prombzex',
      version='0.1',
      description='Prometheus Bugzilla Exporter',
      url='https://github.com/cmsj/prombzex',
      author='Chris Jones',
      author_email='cmsj@tenshu.net',
      license='MIT',
      packages=['prombzex'],
      scripts=['bin/prombzex'],
      zip_safe=False)
