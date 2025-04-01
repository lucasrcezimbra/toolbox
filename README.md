# Toolbox

![](./contrib/screenshot.png)

## Installation
```bash
git clone git@github.com:lucasrcezimbra/toolbox.git
cd toolbox
make install
```

### Test
```bash
make test
```

### Run
```bash
# 1. Collect data from sources
make datacollect github=<your-github-username>

# 2. Import collected data
make dbload

# 3. Run server
make dev
```
