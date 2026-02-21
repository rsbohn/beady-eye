# HTML Demo Pages

*2026-02-21T01:47:09Z by Showboat 0.6.0*
<!-- showboat-id: cca4bddb-2f12-4393-92a2-36d31d3a5317 -->

This demo captures basic metadata (title and file size) for each HTML page in the repository.

```python3
from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")
match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
title = match.group(1).strip() if match else "(title not found)"
print(f"{path}: {title}")
print(f"Bytes: {len(text)}")

```

```output
index.html: beady-eye
Bytes: 3013
```

```python3
from pathlib import Path
import re

path = Path("playground.html")
text = path.read_text(encoding="utf-8")
match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
title = match.group(1).strip() if match else "(title not found)"
print(f"{path}: {title}")
print(f"Bytes: {len(text)}")

```

```output
playground.html: beady-eye: displayio Playground
Bytes: 7487
```

```python3
from pathlib import Path
import re

path = Path("examples/bubbles.html")
text = path.read_text(encoding="utf-8")
match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
title = match.group(1).strip() if match else "(title not found)"
print(f"{path}: {title}")
print(f"Bytes: {len(text)}")

```

```output
examples/bubbles.html: beady-eye - Moving Bubbles Demo
Bytes: 5282
```

```python3
from pathlib import Path
import re

path = Path("examples/pyodide-demo.html")
text = path.read_text(encoding="utf-8")
match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
title = match.group(1).strip() if match else "(title not found)"
print(f"{path}: {title}")
print(f"Bytes: {len(text)}")

```

```output
examples/pyodide-demo.html: beady-eye: Pyodide displayio Demo
Bytes: 3485
```

```python3
from pathlib import Path
import re

path = Path("examples/radiator.html")
text = path.read_text(encoding="utf-8")
match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
title = match.group(1).strip() if match else "(title not found)"
print(f"{path}: {title}")
print(f"Bytes: {len(text)}")

```

```output
examples/radiator.html: beady-eye: Radiator Demo
Bytes: 1992
```
