from pathlib import Path

p=Path(r".\A_04_AGENTS\ImageDepartment\runner.py")

t=p.read_text(encoding="utf-8")

t=t.replace(
'ckpt_name = self._list_first(ckpt_req, "sd_xl_base_1.0.safetensors")',
'ckpt_name = "RealVisXL_V5.0.safetensors"'
)

t=t.replace('"width": 768','"width": 1024')
t=t.replace('"height": 768','"height": 1024')
t=t.replace('"steps": 20','"steps": 30')

p.write_text(t,encoding="utf-8")

print("QUALITY PATCH OK")
