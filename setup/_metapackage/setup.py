import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-vertical-travel",
    description="Meta package for oca-vertical-travel Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-travel',
        'odoo8-addon-travel_journey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
