test:
  docker run \
    --publish=7474:7474 --publish=7687:7687 \
    neo4j
  python tests/main.py
