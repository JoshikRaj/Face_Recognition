from setuptools import setup, find_packages

setup(
    name="face_recognition_package",  # Package name
    version="0.1.0",  # Version number
    packages=find_packages(),  # Automatically find packages
    install_requires=[  # Dependencies
        "numpy",
        "opencv-python",
        "face-recognition"
    ],
    entry_points={  # Allow running the main script as a command
        'console_scripts': [
            'face-recognition=face_recognition_package.main:main',
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Joshik Raj",
    author_email="joshikrajjojo@gmail.com",
    description="A face recognition package with attendance tracking",
    
)
