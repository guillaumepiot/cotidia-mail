from setuptools import find_packages, setup


setup(
    name="cotidia-mail",
    description="Transaction email manager.",
    version="1.0",
    author="Guillaume Piot",
    author_email="guillaume@cotidia.com",
    url="https://code.cotidia.com/cotidia/mail/",
    packages=find_packages(),
    package_data={
        'cotidia.mail': [
            'templates/admin/mail/*.html',
            'templates/notice/*.html',
            'templates/notice/*.txt',
        ]
    },
    namespace_packages=['cotidia'],
    include_package_data=True,
    install_requires=[
        'django-form-utils>=1.0.3',
        'django-filter>=0.13.0',
        'djrill>=2.1.0'
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
)
