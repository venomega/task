from distutils.core import setup

setup(
    name='task',
    author="venomega",
    author_email="usercryptonumberzero@gmail.com",
    version='0.3',
    packages=['task', ],
    install_requires=[
        'arrow',
        'pyotp'
    ],
    license='GPL-3',
    url="https://github.com/venomega/task",
    download_url="https://github.com/venomega/task/archive/0.1.tar.gz",
    description="Just get the tasks stright"
)
