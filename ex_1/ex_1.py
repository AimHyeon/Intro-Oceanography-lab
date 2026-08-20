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
import gsw
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_excel("./ex_1/data/data.xlsx")
# # - 국립수산과학원 정선해양조사자료 활용 (동해-104 line)
depth = pd.to_numeric(df.columns[1:], errors="coerce")
temperature = pd.to_numeric(df.iloc[0, 1:], errors="coerce")
salinity = pd.to_numeric(df.iloc[1, 1:], errors="coerce")

# fig, ax_temp = plt.subplots(figsize=(7, 8))

# ax_temp.plot(
#     temperature,
#     depth,
#     linewidth=2,
#     label="수온(°C)"
# )

# ax_temp.set_ylabel("수심(m)")
# ax_temp.set_ylim(500, 0)
# ax_temp.grid(True, alpha=0.3)

# ax_sal = ax_temp.twiny()

# ax_sal.plot(
#     salinity,
#     depth,
#     linewidth=2,
#     linestyle="--",
#     color="orange",
#     label="염분(psu)"
# )

# ax_sal.set_xlim(33.0, 35.0)

# ax_temp.xaxis.tick_top()
# ax_temp.xaxis.set_label_position("top")
# ax_temp.set_xlabel("수온(°C)")

# ax_temp.tick_params(
#     axis="x",
#     top=True,
#     labeltop=True,
#     bottom=False,
#     labelbottom=False
# )

# ax_sal.xaxis.tick_top()
# ax_sal.xaxis.set_label_position("top")
# ax_sal.set_xlabel("염분(psu)")

# ax_sal.spines["top"].set_position(("outward", 45))

# ax_temp.set_title(
#     "수온ㆍ염분 수직 분포",
#     loc="left",
#     fontsize=18,
#     fontweight="bold",
#     pad=80
# )

# lines_temp, labels_temp = ax_temp.get_legend_handles_labels()
# lines_sal, labels_sal = ax_sal.get_legend_handles_labels()

# ax_temp.legend(
#     lines_temp + lines_sal,
#     labels_temp + labels_sal,
#     loc="lower right"
# )

# plt.tight_layout()
# plt.show()


# EX1-2: 표층과 저층의 밀도 차이 비교

depth = pd.to_numeric(df.columns, errors="coerce")
temperature = pd.to_numeric(df.iloc[0, :], errors="coerce")
salinity = pd.to_numeric(df.iloc[1, :], errors="coerce")

profile = pd.DataFrame({
    "수심(m)": depth,
    "수온(°C)": temperature.values,
    "염분": salinity.values
})

profile = profile.dropna()
profile = profile.sort_values("수심(m)").reset_index(drop=True)

lat = 37.0567
lon = 129.7933


profile["압력(dbar)"] = gsw.p_from_z(
    -profile["수심(m)"].to_numpy(),
    lat
)

profile["절대염분(g/kg)"] = gsw.SA_from_SP(
    profile["염분"].to_numpy(),
    profile["압력(dbar)"].to_numpy(),
    lon,
    lat
)

profile["보존수온(°C)"] = gsw.CT_from_t(
    profile["절대염분(g/kg)"].to_numpy(),
    profile["수온(°C)"].to_numpy(),
    profile["압력(dbar)"].to_numpy()
)

profile["밀도(kg/m³)"] = gsw.rho(
    profile["절대염분(g/kg)"].to_numpy(),
    profile["보존수온(°C)"].to_numpy(),
    profile["압력(dbar)"].to_numpy()
)

surface = profile.iloc[0]
bottom = profile.iloc[-1]

surface_depth = surface["수심(m)"]
surface_temp = surface["수온(°C)"]
surface_salinity = surface["염분"]
surface_density = surface["밀도(kg/m³)"]

bottom_depth = bottom["수심(m)"]
bottom_temp = bottom["수온(°C)"]
bottom_salinity = bottom["염분"]
bottom_density = bottom["밀도(kg/m³)"]

density_difference = bottom_density - surface_density

print(f"표층 수심: {surface_depth:.0f} m")
print(f"표층 수온: {surface_temp:.3f} °C")
print(f"표층 염분: {surface_salinity:.3f}")
print(f"표층 밀도: {surface_density:.3f} kg/m³")

print()

print(f"저층 수심: {bottom_depth:.0f} m")
print(f"저층 수온: {bottom_temp:.3f} °C")
print(f"저층 염분: {bottom_salinity:.3f}")
print(f"저층 밀도: {bottom_density:.3f} kg/m³")

print()
print(f"표층과 저층의 밀도 차이: {density_difference:.3f} kg/m³")

fig, ax = plt.subplots(figsize=(7, 8))

ax.plot(
    profile["밀도(kg/m³)"],
    profile["수심(m)"],
    linewidth=2
)

ax.set_title("밀도 수직 분포")
ax.set_xlabel("밀도 (kg/m³)")
ax.set_ylabel("수심 (m)")

ax.invert_yaxis()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Ex-1-3: 동일 지점의 여름철 성층과 겨울철 혼합층 설명

df = pd.read_excel(
    "./ex_1/data/data.xlsx",
    sheet_name="Sheet1",
    header=None
)


depth = pd.to_numeric(df.iloc[0, 1:], errors="coerce")

temp_summer = pd.to_numeric(df.iloc[1, 1:], errors="coerce")
psu_summer = pd.to_numeric(df.iloc[2, 1:], errors="coerce")

temp_winter = pd.to_numeric(df.iloc[3, 1:], errors="coerce")
psu_winter = pd.to_numeric(df.iloc[4, 1:], errors="coerce")

# ------------------------
# 유효 데이터
# ------------------------

valid_temp = (
    depth.notna()
    & temp_summer.notna()
    & temp_winter.notna()
)

valid_psu = (
    depth.notna()
    & psu_summer.notna()
    & psu_winter.notna()
)

valid_density = (
    depth.notna()
    & temp_summer.notna()
    & psu_summer.notna()
    & temp_winter.notna()
    & psu_winter.notna()
)


# ------------------------
# 수온 데이터
# ------------------------

depth_temp = depth[valid_temp].reset_index(drop=True)

temp_summer_plot = temp_summer[valid_temp].reset_index(drop=True)
temp_winter_plot = temp_winter[valid_temp].reset_index(drop=True)


# ------------------------
# 염분 데이터
# ------------------------

depth_psu = depth[valid_psu].reset_index(drop=True)

psu_summer_plot = psu_summer[valid_psu].reset_index(drop=True)
psu_winter_plot = psu_winter[valid_psu].reset_index(drop=True)


# ------------------------
# 밀도 계산용 데이터
# ------------------------

depth_density = depth[valid_density].reset_index(drop=True)

temp_summer_density = temp_summer[valid_density].reset_index(drop=True)
psu_summer_density = psu_summer[valid_density].reset_index(drop=True)

temp_winter_density = temp_winter[valid_density].reset_index(drop=True)
psu_winter_density = psu_winter[valid_density].reset_index(drop=True)


# ------------------------
# GSW 밀도 계산
# ------------------------

lat = 37.0567
lon = 129.7933


# 수심(m) → 압력(dbar)
pressure = gsw.p_from_z(
    -depth_density.to_numpy(),
    lat
)


# 여름
SA_summer = gsw.SA_from_SP(
    psu_summer_density.to_numpy(),
    pressure,
    lon,
    lat
)

CT_summer = gsw.CT_from_t(
    SA_summer,
    temp_summer_density.to_numpy(),
    pressure
)

# sigma0 = 잠재밀도 - 1000
density_summer = 1000 + gsw.sigma0(
    SA_summer,
    CT_summer
)


# 겨울
SA_winter = gsw.SA_from_SP(
    psu_winter_density.to_numpy(),
    pressure,
    lon,
    lat
)

CT_winter = gsw.CT_from_t(
    SA_winter,
    temp_winter_density.to_numpy(),
    pressure
)

density_winter = 1000 + gsw.sigma0(
    SA_winter,
    CT_winter
)


# ------------------------
# 그래프
# ------------------------

fig = plt.figure(figsize=(18, 10))

rows = 1
cols = 3


# ------------------------
# 수온
# ------------------------

ax1 = fig.add_subplot(rows, cols, 1)

ax1.plot(
    temp_summer_plot,
    depth_temp,
    linewidth=2,
    label="여름"
)

ax1.plot(
    temp_winter_plot,
    depth_temp,
    linewidth=2,
    linestyle="--",
    label="겨울"
)

ax1.set_title("수온 수직 분포")
ax1.set_xlabel("수온 (°C)")
ax1.set_ylabel("수심 (m)")

ax1.invert_yaxis()
ax1.grid(True, alpha=0.3)
ax1.legend()


# ------------------------
# 염분
# ------------------------

ax2 = fig.add_subplot(rows, cols, 2)

ax2.plot(
    psu_summer_plot,
    depth_psu,
    linewidth=2,
    label="여름"
)

ax2.plot(
    psu_winter_plot,
    depth_psu,
    linewidth=2,
    linestyle="--",
    label="겨울"
)

ax2.set_title("염분 수직 분포")
ax2.set_xlabel("염분")
ax2.set_ylabel("수심 (m)")

ax2.invert_yaxis()
ax2.grid(True, alpha=0.3)
ax2.legend()


# ------------------------
# 잠재밀도
# ------------------------

ax3 = fig.add_subplot(rows, cols, 3)

ax3.plot(
    density_summer,
    depth_density,
    linewidth=2,
    label="여름"
)

ax3.plot(
    density_winter,
    depth_density,
    linewidth=2,
    linestyle="--",
    label="겨울"
)

ax3.set_title("잠재밀도 수직 분포")
ax3.set_xlabel("잠재밀도 (kg/m³)")
ax3.set_ylabel("수심 (m)")

ax3.invert_yaxis()
ax3.grid(True, alpha=0.3)
ax3.legend()


fig.suptitle(
    "동일 지점의 여름철ㆍ겨울철 수직 분포",
    fontsize=18,
    fontweight="bold"
)

plt.tight_layout()
plt.show()

# plt.show()
# Ex1-4: 관측자료를 이용하여 T-S diagram 작성 및 설명
df = pd.read_excel("./ex_1/data/data.xlsx")

temperature = pd.to_numeric(df.iloc[0], errors="coerce")
salt = pd.to_numeric(df.iloc[1], errors="coerce")

valid = temperature.notna() & salt.notna()

temperature = temperature[valid]
salt = salt[valid]


smin = salt.min() - 0.5
smax = salt.max() + 0.5

tmin = temperature.min() - 1
tmax = temperature.max() + 1

saltL = np.linspace(smin, smax, 200)
tempL = np.linspace(tmin, tmax, 200)

Sg, Tg = np.meshgrid(saltL, tempL)


lat = 37.0567
lon = 129.7933

pressure = 10.0


# Practical Salinity → Absolute Salinity
SA = gsw.SA_from_SP(
    Sg,
    pressure,
    lon,
    lat
)

# 현장 수온 → Conservative Temperature
CT = gsw.CT_from_t(
    SA,
    Tg,
    pressure
)

# 밀도 계산
dens = gsw.rho(
    SA,
    CT,
    pressure
)


# ------------------------
# T-S Diagram
# ------------------------

plt.figure(figsize=(7, 6))

CS = plt.contour(
    Sg,
    Tg,
    dens,
    levels=np.arange(1000, 1070, 1),
    linestyles="dashed",
    colors="grey"
)

plt.clabel(
    CS,
    fontsize=10,
    inline=True,
    fmt="%.0f"
)

plt.scatter(
    salt,
    temperature,
    s=20
)

plt.xlabel("염분 (psu)")
plt.ylabel("수온 (°C)")
plt.title("T-S Diagram")

plt.xlim(smin, smax)
plt.ylim(tmin, tmax)

plt.tight_layout()
plt.show()