"""
실습 1: 해수의 물리적 성질과 해양의 수직 구조
- 국립수산과학원 정선해양조사자료 활용 (동해-104 line)
- 정선 관측 자료로 수온ㆍ염분 수직 분포 작성
- 표층과 저층의 밀도 차이 비교
- 동일 지점에서 여름철 성층과 겨울철 혼합층 구조 설명
- 관측자료를 이용하여 T-S diagram 작성 및 설명
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# - 국립수산과학원 정선해양조사자료 활용 (동해-104 line)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False
depth = [0, 10, 20, 30, 50, 75, 100, 125, 150, 200]

temp = [24.25, 14.39, 10.87, 9.94, 7.89, 5.89, 4.34, 2.99, 1.72, 1.47]
psu = [33.06, 34.17, 34.25, 34.22, 34.1, 34.06, 34.2, 34.12, 34.11, 34.04]

fig, ax_temp = plt.subplots(figsize=(7, 8))
ax_temp.plot(
    temp,
    depth,
    marker="o",
    linewidth=2,
    label="수온(°C)"
)

ax_temp.set_xlabel("수온(°C)")
ax_temp.set_ylabel("수심(m)")

ax_temp.invert_yaxis()

ax_temp.set_ylim(200, 0)
ax_temp.grid(True, alpha=0.3)

ax_sal = ax_temp.twiny()

ax_sal.plot(
    psu,
    depth,
    marker="o",
    linewidth=2,
    label="염분(psu)",
    color="orange"
)

ax_sal.set_xlabel("염분(psu)")
ax_sal.set_xlim(33.0, 35.0)

ax_temp.set_title(
    "수온ㆍ염분 수직 분포",
    loc="left",
    fontsize=18,
    fontweight="bold",
    pad=40
)

plt.tight_layout()
plt.show()