
from pathlib import Path

from cr39py.scan import Scan
from cr39py.cut import Cut

cpsa_path = Path("C:\\", "Users", "Reece", "Desktop", "PRAD UROP stuff", "test.cpsa")

scan = Scan.from_cpsa(cpsa_path)



