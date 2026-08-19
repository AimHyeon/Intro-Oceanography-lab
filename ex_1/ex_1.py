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
import seawater
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# df = pd.read_excel("./ex_1/data/data.xlsx")
# # - 국립수산과학원 정선해양조사자료 활용 (동해-104 line)
depth = [0, 10, 20, 30, 50, 75, 100, 125, 150, 200]

temp = [24.25, 14.39, 10.87, 9.94, 7.89, 5.89, 4.34, 2.99, 1.72, 1.47]

psu = [33.06, 34.17, 34.25, 34.22, 34.1, 34.06, 34.2, 34.12, 34.11, 34.04]

fig, ax_temp = plt.subplots(figsize=(7, 8))

ax_temp.plot(
    temp,
    depth,
    linewidth=2,
    label="수온(°C)"
)

ax_temp.set_ylabel("수심(m)")
ax_temp.set_ylim(200, 0)
ax_temp.grid(True, alpha=0.3)

ax_sal = ax_temp.twiny()

ax_sal.plot(
    psu,
    depth,
    linewidth=2,
    linestyle="--",
    color="orange",
    label="염분(psu)"
)

ax_sal.set_xlim(33.0, 35.0)

ax_temp.xaxis.tick_top()
ax_temp.xaxis.set_label_position("top")
ax_temp.set_xlabel("수온(°C)")

ax_temp.tick_params(
    axis="x",
    top=True,
    labeltop=True,
    bottom=False,
    labelbottom=False
)

ax_sal.xaxis.tick_top()
ax_sal.xaxis.set_label_position("top")
ax_sal.set_xlabel("염분(psu)")

ax_sal.spines["top"].set_position(("outward", 45))

ax_temp.set_title(
    "수온ㆍ염분 수직 분포",
    loc="left",
    fontsize=18,
    fontweight="bold",
    pad=80
)

lines_temp, labels_temp = ax_temp.get_legend_handles_labels()
lines_sal, labels_sal = ax_sal.get_legend_handles_labels()

ax_temp.legend(
    lines_temp + lines_sal,
    labels_temp + labels_sal,
    loc="lower right"
)

plt.tight_layout()
plt.show()


# EX1-2: 표층과 저층의 밀도 차이 비교

# depth = pd.to_numeric(df.columns, errors="coerce")
# temperature = pd.to_numeric(df.iloc[0, :], errors="coerce")
# salinity = pd.to_numeric(df.iloc[1, :], errors="coerce")

# profile = pd.DataFrame({
#     "수심(m)": depth,
#     "수온(°C)": temperature.values,
#     "염분(‰)": salinity.values
# })

# profile = profile.dropna()
# profile = profile.sort_values("수심(m)").reset_index(drop=True)

# surface = profile.iloc[0]
# bottom = profile.iloc[-1]

# surface_depth = surface["수심(m)"]
# surface_temp = surface["수온(°C)"]
# surface_salinity = surface["염분(‰)"]

# bottom_depth = bottom["수심(m)"]
# bottom_temp = bottom["수온(°C)"]
# bottom_salinity = bottom["염분(‰)"]

# a_bar = 0.15
# b_bar = 0.78
# k_bar = 4.5e-3

# rho_0 = 1027
# T_0 = 10
# S_0 = 35

# def calculate_density(temperature, salinity, depth):
#     pressure = depth

#     density = (
#         rho_0
#         - a_bar * (temperature - T_0)
#         + b_bar * (salinity - S_0)
#         + k_bar * pressure
#     )

#     return density

# surface_density = calculate_density(
#     surface_temp,
#     surface_salinity,
#     surface_depth
# )

# bottom_density = calculate_density(
#     bottom_temp,
#     bottom_salinity,
#     bottom_depth
# )

# density_difference = bottom_density - surface_density

# print(f"표층 수심: {surface_depth:.0f} m")
# print(f"표층 수온: {surface_temp:.3f} °C")
# print(f"표층 염분: {surface_salinity:.3f} ‰")
# print(f"표층 밀도: {surface_density:.3f} kg/m³")

# print()

# print(f"저층 수심: {bottom_depth:.0f} m")
# print(f"저층 수온: {bottom_temp:.3f} °C")
# print(f"저층 염분: {bottom_salinity:.3f} ‰")
# print(f"저층 밀도: {bottom_density:.3f} kg/m³")
# print()

# # Ex-1-3: 동일 지점의 여름철 성층과 겨울철 혼합층 설명
df = pd.read_excel(
    "./ex_1/data/data.xlsx",
    sheet_name="Sheet2",
    header=None
)

depth = pd.to_numeric(df.iloc[0, 2:], errors="coerce")

temp_winter = pd.to_numeric(df.iloc[1, 2:], errors="coerce")
psu_winter = pd.to_numeric(df.iloc[2, 2:], errors="coerce")

temp_summer = pd.to_numeric(df.iloc[3, 2:], errors="coerce")
psu_summer = pd.to_numeric(df.iloc[4, 2:], errors="coerce")

valid_temp = (
    depth.notna()
    & temp_summer.notna()
    & temp_winter.notna()
    & (depth <= 5500)
)

valid_psu = (
    depth.notna()
    & psu_summer.notna()
    & psu_winter.notna()
    & (depth <= 5500)
)

depth_temp = depth[valid_temp].reset_index(drop=True)
temp_summer = temp_summer[valid_temp].reset_index(drop=True)
temp_winter = temp_winter[valid_temp].reset_index(drop=True)

depth_psu = depth[valid_psu].reset_index(drop=True)
psu_summer = psu_summer[valid_psu].reset_index(drop=True)
psu_winter = psu_winter[valid_psu].reset_index(drop=True)

y_temp = range(len(depth_temp))
y_psu = range(len(depth_psu))

fig = plt.figure(figsize=(12, 10))

rows = 1
cols = 2

ax1 = fig.add_subplot(rows, cols, 1)

ax1.plot(
    temp_summer,
    y_temp,
    linewidth=2,
    label="여름"
)

ax1.plot(
    temp_winter,
    y_temp,
    linewidth=2,
    linestyle="--",
    label="겨울"
)

ax1.set_title("수온 수직 분포")
ax1.set_xlabel("수온(°C)")
ax1.set_ylabel("수심(m)")

ax1.set_yticks(list(y_temp)[::5])
ax1.set_yticklabels(
    depth_temp.iloc[::5].astype(int)
)

ax1.invert_yaxis()
ax1.grid(True, alpha=0.3)
ax1.legend()


ax2 = fig.add_subplot(rows, cols, 2)

ax2.plot(
    psu_summer,
    y_psu,
    linewidth=2,
    label="여름"
)

ax2.plot(
    psu_winter,
    y_psu,
    linewidth=2,
    linestyle="--",
    label="겨울"
)

ax2.set_title("염분 수직 분포")
ax2.set_xlabel("염분(psu)")
ax2.set_ylabel("수심(m)")

ax2.set_yticks(list(y_psu)[::5])
ax2.set_yticklabels(
    depth_psu.iloc[::5].astype(int)
)

ax2.invert_yaxis()
ax2.grid(True, alpha=0.3)
ax2.legend()

fig.suptitle(
    "동일 지점의 여름철ㆍ겨울철 수직 분포",
    fontsize=18,
    fontweight="bold"
)

fig.tight_layout()

plt.show()
# Ex1-4: 관측자료를 이용하여 T-S diagram 작성 및 설명
# temp = pd.to_numeric(df.iloc[0], errors="coerce")
# salt = pd.to_numeric(df.iloc[1], errors="coerce")

# valid = temp.notna() & salt.notna()

# temp = temp[valid]
# salt = salt[valid]

# smin = salt.min() - 0.5
# smax = salt.max() + 0.5
# tmin = temp.min() - 1
# tmax = temp.max() + 1

# saltL = np.linspace(smin, smax, 200)
# tempL = np.linspace(tmin, tmax, 200)

# Sg, Tg = np.meshgrid(saltL, tempL)

# dens = seawater.dens0(Sg, Tg)

# plt.figure(figsize=(7, 6))

# CS = plt.contour(
#     Sg,
#     Tg,
#     dens,
#     levels=np.arange(1000, 1050, 1),
#     linestyles="dashed",
#     colors="grey"
# )

# plt.clabel(
#     CS,
#     fontsize=10,
#     inline=True,
#     fmt="%.0f",
# )

# plt.scatter(
#     salt,
#     temp,
#     s=20
# )

# plt.xlabel("염분(psu)")
# plt.ylabel("수온(°C)")
# plt.title("T-S Diagram")

# plt.xlim(smin, smax)
# plt.ylim(tmin, tmax)

# plt.tight_layout()
# plt.show()

