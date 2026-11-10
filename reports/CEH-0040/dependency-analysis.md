# CEH-0040 · remsky/Kokoro-FastAPI

https://github.com/remsky/Kokoro-FastAPI

```json
{
  "manifests": [
    "docker/test-client/pyproject.toml",
    "examples/pyproject.toml",
    "examples/requirements.txt",
    "package.json",
    "pyproject.toml"
  ],
  "npm": {},
  "npm_dev": {
    "@playwright/test": "^1.57.0"
  },
  "install_hooks": {},
  "python": [
    "fastapi>=0.128.8",
    "starlette>=1.3.1",
    "uvicorn==0.54.0",
    "click>=8.0.0",
    "pydantic==2.10.4",
    "pydantic-settings==2.7.0",
    "python-dotenv==1.2.2",
    "sqlalchemy==2.0.27",
    "numpy>=1.26.0",
    "scipy==1.14.1",
    "soundfile==0.13.0",
    "inno-kokoro==0.3.0",
    "python-multipart>=0.0.20",
    "regex>=2025.10.22",
    "unicode-segmentation-rs>=0.3.3",
    "aiofiles==23.2.1",
    "tqdm==4.67.1",
    "requests==2.33.0",
    "munch==4.0.0",
    "tiktoken==0.8.0",
    "loguru==0.7.3",
    "mutagen>=1.47.0",
    "psutil>=6.1.1",
    "espeakng-loader==0.2.4",
    "kokoro==0.9.4",
    "huggingface-hub>=1.6.0",
    "transformers>=5.5.0,<6",
    "misaki[en,ja,ko,zh]==0.9.4",
    "pyopenjtalk-plus>=0.4.1 ; sys_platform == 'win32'",
    "spacy==3.8.5",
    "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
    "inflect>=7.5.0",
    "phonemizer-fork>=3.3.2",
    "av>=14.2.0",
    "text2num>=2.5.1",
    "wsproto==1.3.2"
  ]
}
```
