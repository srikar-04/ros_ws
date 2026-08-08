from setuptools import find_packages, setup

package_name = 'topic_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='srikar',
    maintainer_email='srikar.code01@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "publisher = topic_pkg.publisher:main",
            "subscriber = topic_pkg.subscriber:main",
            "gripper_service = topic_pkg.gripper_service:main",
        ],
    },
)
