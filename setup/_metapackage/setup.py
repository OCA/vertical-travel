import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-vertical-travel",
    description="Meta package for oca-vertical-travel Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-passport_expiration',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
