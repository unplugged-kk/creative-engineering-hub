import json
from contentos.qa import run_qa
from pathlib import Path
results=run_qa(Path('/tmp/ceh-benchmark/video.mp4'))
print(json.dumps([dict(check=c,status=s,detail=d) for c,s,d in results],indent=2))
raise SystemExit(any(s=='FAIL' for _,s,_ in results))
