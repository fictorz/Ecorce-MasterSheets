python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
# install just your top-level deps (the few you actually use), e.g.:
python -m pip install "fastapi" "uvicorn[standard]" "pydantic<2"  # <-- example
# verify + see the tree
python -m pip install pipdeptree
pipdeptree -w fail || true   # shows conflicts if any
# lock it
pip freeze --all > requirements.txt
