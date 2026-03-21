import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import locale 
import sys
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
from pathlib import Path

## Configuration du script 
EXCEL_FILE = "/Users/alexandralepine/Desktop/Data_velo/Data Vélo.xlsx"
GRAPHS_DIR = Path ("graphs")
GRAPHS_DIR.mkdir (exist_ok=True)

# Correction des valeurs de couleur dans le dictionnaire COLORS
COLORS = {"Gym": "#FF0000", "Maison": "#E8834A"}
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi" : 150})

##Chargement et nettoyage des données (ETL)
df = pd.read_excel (EXCEL_FILE)
df["Emplacement"] = df["Emplacement"].str.strip().str.capitalize()
df["Date"]= pd.to_datetime(df["Date"])

## Redirection des print() vers le terminal et un fichier txt
class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
    def flush(self):
        for f in self.files:
            f.flush()
rapport = open("rapport_performance_velo.txt", "w", encoding="utf-8")
sys.stdout = Tee(sys.stdout, rapport)

##Convertir le temps en minutes
def to_minutes (t):
    try:
        parts = str(t).split(":")
        heures = int(parts[0])
        minutes = int (parts[1])
        seconde = int (parts[2]) if len (parts) == 3 else 0
        return heures * 60 + minutes + seconde /60
    except:
        return None
df ["Temps en minutes"] = df["Temps"].apply(to_minutes)
df["KM/H"] = (df ["Distance (KM)"] / df ["Temps en minutes"] * 60 ).round(2)
df["Mois"] = df["Date"].dt.strftime("%B %Y")

# Convertir la colonne "Mois" en type datetime pour un tri chronologique
df["Mois"] = pd.to_datetime(df["Mois"], format="%B %Y")

# Trier les données par mois
df = df.sort_values("Mois")

# Reconvertir la colonne "Mois" en format texte pour l'affichage
df["Mois"] = df["Mois"].dt.strftime("%B %Y")

gym = df[df["Emplacement"] == "Gym"]
maison = df[df["Emplacement"] == "Maison"]

## Sommaire des résultats de la performance en vélo stationnaire
def stats_bloc(label, subset):
    d = subset["Distance (KM)"]
    v = subset["KM/H"]
    t = subset ["Temps en minutes"]
    print (f"\n{'-'*40}")
    print (f" {label} ({len(subset)} séances)")
    print(('-'*40))
    print(f"Distance -> moy {d.mean():.1f} km | écart-type {d.std():.1f} km")
    print(f"Distance -> min {d.min():.1f} km | max {d.max():.1f} km | total { d.sum():.1f} km")
    print(f"Vitesse -> moy {v.mean():.1f} KM/H | max {v.max():.1f} KM/H")
    print (f"Durée -> moyenne {t.mean():.1f} minutes")
    
print ("ANALYSE DE PERFORMANCE EN VÉLO STATIONNAIRE🚴🔥💪")
stats_bloc("🏋️ GYM", gym)
stats_bloc("🏡 MAISON", maison)
print (f"\n{'-'*40}")
print (f"TOTAL -> {len(df)} séances | {df['Distance (KM)'].sum():.1f}km")

##Graphique 1 - Évolution de la distance
# Vérifier et trier les données par date pour garantir un tracé correct des lignes
# Supprimer les lignes avec des valeurs manquantes dans les colonnes "Date" et "Distance (KM)"
df = df.dropna(subset=["Date", "Distance (KM)"])

# Trier les données par date
df = df.sort_values("Date")

# Recalculer et tracer les lignes correctement
fig, ax = plt.subplots(figsize=(12,5))
for lieu, groupe in df.groupby("Emplacement"):
    ax.scatter(groupe["Date"], groupe["Distance (KM)"],
               color=COLORS[lieu], label=lieu, s=70, zorder=3)
    ax.plot(groupe["Date"], groupe["Distance (KM)"],
            color=COLORS[lieu], alpha=0.4, linewidth=1)

##Ligne de tendance globale
z = np.polyfit(mdates.date2num(df["Date"]), df ["Distance (KM)"],1)
p = np.poly1d(z)
ax.plot(df["Date"], p(mdates.date2num(df["Date"])),
        "--", color="gray", linewidth=1.5, label="Tendance Globale")
ax.set_title("Distance parcouru par séance", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Mois")
ax.set_ylabel("Distance (KM)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45, ha="right")
ax.legend()
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(GRAPHS_DIR / "Distance_parcouru_par_seance.png")
plt.close()
print("Graphique Distance parcouru par séance créer ✅")

##Graphique 2 - Comparaison Gym VS Maison 
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, col, ylabel in zip(axes,
                            ["Distance (KM)", "KM/H"],
                            ["Distance (KM)", "KM/H"]):
    data = [gym[col].dropna(), maison[col].dropna()]
    bp = ax.boxplot(data, patch_artist=True, widths=0.5,
                    medianprops=dict(color="black", linewidth=2))
    for patch, color in zip(bp["boxes"], COLORS.values()):
        patch.set_facecolor(color)
        patch.set_alpha(0.9)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Gym", "Maison"])
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.5)

axes[0].set_title("Distance parcouru en KM", fontweight="bold")
axes[1].set_title("Vitesse en KM/H", fontweight="bold")
fig.suptitle("Gym versus Maison")
fig.tight_layout()
fig.savefig(GRAPHS_DIR / "Gym_VS_Maison.png", bbox_inches="tight")
plt.close()
print("Graphique Gym VS Maison crée ✅")

##Graphique 3 - Distance totale par mois 
monthly = (df.groupby(["Mois", "Emplacement"])["Distance (KM)"]).sum().unstack(fill_value=0).sort_index()

# S'assurer que l'index du DataFrame "monthly" est trié par ordre chronologique
monthly.index = pd.to_datetime(monthly.index, format="%B %Y")
monthly = monthly.sort_index()
monthly.index = monthly.index.strftime("%B %Y")

for col in ["Gym", "Maison"]:
    if col not in monthly.columns:
        monthly[0] = 0
fig, ax = plt.subplots(figsize=(12,5))
monthly[["Gym", "Maison"]].plot(
    kind="bar", stacked=True, ax=ax,
    color=[COLORS["Gym"], COLORS["Maison"]], width=0.70
)
ax.set_title("Distance totale parcouru par mois", fontsize=14, fontweight="bold", pad=12)  
ax.set_xlabel("Mois")
ax.set_ylabel("Distance (KM)")
ax.set_xticklabels([str(m) for m in monthly.index], rotation=45, ha="right")
ax.legend(title="Emplacement", loc="upper left", bbox_to_anchor=(1, 0.95))
ax.grid(axis="y", alpha=0.5)

for i, (idx, row) in enumerate(monthly.iterrows()):
    total = row["Gym"] + row["Maison"]
    ax.text(i, total + 0.5, f"{total:.1f} km", ha="center", va="bottom", fontsize=10)
ax.margins(y=0.45)
fig.tight_layout(pad=3)
fig.savefig(GRAPHS_DIR / "Distance_par_mois.png")
plt.close()
print("Graphique Distance par mois créée ✅")

##Graphique 4 - Nombre de séances par mois, par emplacement
Seance = df.groupby(["Mois", "Emplacement"]).size().unstack(fill_value=0)

# S'assurer que l'index du DataFrame "Seance" est trié par ordre chronologique
Seance.index = pd.to_datetime(Seance.index, format="%B %Y")
Seance = Seance.sort_index()
Seance.index = Seance.index.strftime("%B %Y")


fig, ax = plt.subplots(figsize=(12, 5))
Seance.plot(
    kind="bar", ax=ax,
    color=[COLORS["Gym"], COLORS["Maison"]], width=0.70
)
ax.set_title("Nombre de séances par mois", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Mois")
ax.set_ylabel("Nombre de séances")
ax.set_xticklabels([str(m) for m in Seance.index], rotation=45, ha="right")
ax.legend(title="Emplacement")
ax.grid(axis="y", alpha=0.7)
fig.tight_layout()
fig.savefig(GRAPHS_DIR / "Nombre_de_seances_par_mois.png")
plt.close()
print("Graphique Nombre de séances par mois créé ✅")

##Graphique 5 - Distance VS durée - Nuage de points
fig, ax = plt.subplots(figsize=(12, 5))
for lieu, groupe in df.groupby("Emplacement"):
    ax.scatter(groupe["Temps en minutes"], groupe["Distance (KM)"],
               color=COLORS[lieu], label=lieu, s=80, alpha=0.9, zorder=3)
mask = df["Temps en minutes"].notna() & df["Distance (KM)"].notna()
z = np.polyfit(df.loc[mask,"Temps en minutes"], df.loc[mask,"Distance (KM)"], 1)
p = np.poly1d(z)
x_line = np.linspace(df["Temps en minutes"].min(), df["Temps en minutes"].max(), 100)
ax.plot(x_line, p(x_line), "--", color="gray", linewidth=1.5, label="Tendance Globale")

ax.set_title("Distance parcourue VS Durée ", fontsize=16, fontweight="bold", pad=12)
ax.set_xlabel("Durée (minutes)")
ax.set_ylabel("Distance (KM)")
ax.legend()
ax.grid(alpha=0.4)
fig.tight_layout()
fig.savefig(GRAPHS_DIR / "Distance_VS_Duree.png")
plt.close()
print("Graphique Distance VS Durée créé ✅")

##Analyse de la performance en vélo stationnaire - Conclusion
print("\nANALYSE DE PERFORMANCE EN VÉLO STATIONNAIRE - CONCLUSION")
print("-"*50)
print("1. La distance parcourue par séance a montré une tendance à l'augmentation au fil du temps, avec des séances plus longues et plus intenses à la maison que au gym.")

print("2. La vitesse moyenne en KM/H était généralement plus élevée lors des séances à la maison, suggérant une meilleure performance ou un effort plus soutenu dans cet environnement.")

print("3. La relation entre la durée et la distance parcourue montre une corrélation positive, indiquant que les séances plus longues tendent à correspondre à des distances plus grandes, ce qui est cohérent avec une amélioration de la performance au fil du temps.")

print("4. Globalement, les données suggèrent une progression significative de la performance en vélo stationnaire, avec une préférence marquée pour les séances à la maison, qui ont tendance à être plus longues et plus intenses que celles au gym.")

print("5. Les graphiques créés fournissent une visualisation claire de l'évolution de la performance, des comparaisons entre les environnements, et des tendances générales dans les données, ce qui peut être utile pour orienter les futures séances d'entraînement et suivre les progrès au fil du temps.")

## Fin du rapport
sys.stdout = sys.__stdout__
rapport.close()
print("Rapport analyse txt crée ✅")
