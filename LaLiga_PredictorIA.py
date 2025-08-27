# ========================================================================
# 📂 laliga_predictor.py (Versión Final - Basado en Consenso Fantasy)
# ========================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import random

class LaLigaPredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 La Liga Predictor IA (Fantasy Consensus)")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.colors = {
            "bg": "#0d1117", "frame_bg": "#161b22", "text": "#c9d1d9",
            "text_secondary": "#8b949e", "border": "#30363d", "button_bg": "#238636",
            "button_active": "#2ea043", "button_fg": "#ffffff", "champions": "#1a3c2a",
            "europa": "#3d3217", "relegation": "#4a2123", "success": "#2ea043"
        }
        
        self.root.configure(bg=self.colors["bg"])
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.teams_data = self.get_initial_data()
        self.jornada_actual = 3

        self.prediction_weights = {
            'stats_weight': 0.5, # Las estadísticas reales tienen un 50% de peso
            'fantasy_weight': 0.5, # El consenso Fantasy tiene un 50% de peso
            'home_advantage': 1.10 # Ventaja de campo más conservadora
        }

        self.upcoming_matches = [
            {"local": "Real Madrid", "visitante": "FC Barcelona", "desc": "El Clásico"},
            {"local": "Atlético Madrid", "visitante": "Sevilla FC", "desc": "Duelo europeo"},
            {"local": "Athletic Club", "visitante": "Real Sociedad", "desc": "Derby vasco"},
            {"local": "Valencia CF", "visitante": "Villarreal CF", "desc": "Derby valenciano"},
            {"local": "Real Betis", "visitante": "RC Celta", "desc": "Lucha por Europa"},
            {"local": "Getafe CF", "visitante": "CA Osasuna", "desc": "Batalla por puntos"},
            {"local": "RCD Espanyol", "visitante": "Rayo Vallecano", "desc": "Derbi madrileño"},
            {"local": "Granada CF", "visitante": "RCD Mallorca", "desc": "Partido crucial"}
        ]

        self.create_widgets()
        self.update_classification_table()

    def configure_styles(self):
        """Configura los estilos de la interfaz."""
        self.style.configure(".", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.colors["bg"])
        self.style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"])
        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10, background=self.colors["button_bg"], foreground=self.colors["button_fg"], borderwidth=1, relief="raised")
        self.style.map("TButton", background=[('active', self.colors["button_active"])])
        self.style.configure("Treeview", background=self.colors["frame_bg"], fieldbackground=self.colors["frame_bg"], foreground=self.colors["text"], rowheight=25, font=("Segoe UI", 9))
        self.style.map('Treeview', background=[('selected', self.colors["button_bg"])])
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.colors["bg"], foreground=self.colors["text"])
        self.style.configure("Card.TFrame", background=self.colors["frame_bg"], relief="solid", borderwidth=1, bordercolor=self.colors["border"])
        self.style.configure("CardTitle.TLabel", font=("Segoe UI", 12, "bold"), background=self.colors["frame_bg"])
        self.style.configure("CardScore.TLabel", font=("Segoe UI", 24, "bold"), background=self.colors["frame_bg"])
        self.style.configure("CardInfo.TLabel", font=("Segoe UI", 9), background=self.colors["frame_bg"], foreground=self.colors["text_secondary"])
        self.style.configure("Success.TLabel", font=("Segoe UI", 10, "italic"), foreground=self.colors["success"], background=self.colors["bg"])

    def get_initial_data(self):
        """
        Devuelve los datos iniciales, incluyendo el Poder Fantasy de cada equipo.
        Este valor simula el consenso de Biwenger, Marca, Futmondo, etc.
        """
        return {
            "Real Madrid": {"pts": 9, "gf": 8, "gc": 2, "fantasy_power": 98},
            "FC Barcelona": {"pts": 7, "gf": 7, "gc": 3, "fantasy_power": 95},
            "Atlético Madrid": {"pts": 7, "gf": 6, "gc": 2, "fantasy_power": 90},
            "Real Sociedad": {"pts": 5, "gf": 5, "gc": 4, "fantasy_power": 85},
            "Athletic Club": {"pts": 6, "gf": 5, "gc": 2, "fantasy_power": 84},
            "Villarreal CF": {"pts": 4, "gf": 6, "gc": 6, "fantasy_power": 82},
            "Sevilla FC": {"pts": 6, "gf": 4, "gc": 3, "fantasy_power": 80},
            "Real Betis": {"pts": 4, "gf": 3, "gc": 3, "fantasy_power": 78},
            "Valencia CF": {"pts": 4, "gf": 2, "gc": 2, "fantasy_power": 75},
            "RC Celta": {"pts": 3, "gf": 4, "gc": 5, "fantasy_power": 72},
            "CA Osasuna": {"pts": 3, "gf": 3, "gc": 4, "fantasy_power": 70},
            "Getafe CF": {"pts": 3, "gf": 2, "gc": 4, "fantasy_power": 65},
            "Rayo Vallecano": {"pts": 2, "gf": 3, "gc": 5, "fantasy_power": 64},
            "RCD Espanyol": {"pts": 2, "gf": 2, "gc": 4, "fantasy_power": 60},
            "RCD Mallorca": {"pts": 1, "gf": 1, "gc": 3, "fantasy_power": 58},
            "Granada CF": {"pts": 1, "gf": 2, "gc": 5, "fantasy_power": 55},
            "Alavés": {"pts": 1, "gf": 1, "gc": 5, "fantasy_power": 52},
            "Elche CF": {"pts": 0, "gf": 1, "gc": 6, "fantasy_power": 50},
            "Levante UD": {"pts": 0, "gf": 2, "gc": 7, "fantasy_power": 48},
            "Cádiz CF": {"pts": 0, "gf": 0, "gc": 5, "fantasy_power": 45}
        }

    def create_widgets(self):
        """Crea todos los componentes de la interfaz."""
        main_frame = ttk.Frame(self.root, padding="20"); main_frame.pack(expand=True, fill="both")
        control_frame = ttk.Frame(main_frame); control_frame.pack(fill="x", pady=5, anchor="n")
        ttk.Label(control_frame, text="La Liga Predictor", style="Title.TLabel").pack(side="left", expand=True)
        self.update_button = ttk.Button(control_frame, text="🔄 ACTUALIZAR", command=self.refresh_data); self.update_button.pack(side="left", padx=5)
        self.predict_button = ttk.Button(control_frame, text="🎯 PREDICCIONES", command=self.show_predictions_window); self.predict_button.pack(side="left", padx=5)
        class_frame = ttk.Frame(main_frame); class_frame.pack(expand=True, fill="both", pady=10)
        ttk.Label(class_frame, text="Clasificación y Poder Fantasy", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        cols = ("Pos", "Equipo", "Pts", "GF", "GC", "DG", "Poder Fantasy"); self.tree = ttk.Treeview(class_frame, columns=cols, show="headings")
        for col in cols: self.tree.heading(col, text=col); self.tree.column(col, width=100, anchor="center")
        self.tree.column("Equipo", width=150, anchor="w"); self.tree.pack(expand=True, fill="both")
        self.tree.tag_configure('champions', background=self.colors["champions"], foreground=self.colors["text"])
        self.tree.tag_configure('europa', background=self.colors["europa"], foreground=self.colors["text"])
        self.tree.tag_configure('relegation', background=self.colors["relegation"], foreground=self.colors["text"])

    def update_classification_table(self):
        """Actualiza la tabla con los datos de los equipos."""
        for i in self.tree.get_children(): self.tree.delete(i)
        sorted_teams = sorted(self.teams_data.items(), key=lambda x: (x[1]['pts'], x[1]['gf'] - x[1]['gc']), reverse=True)
        for i, (team, stats) in enumerate(sorted_teams, 1):
            tag = ''; 
            if 1 <= i <= 4: tag = 'champions'
            elif 5 <= i <= 6: tag = 'europa'
            elif 18 <= i <= 20: tag = 'relegation'
            values = (i, team, stats['pts'], stats['gf'], stats['gc'], stats['gf'] - stats['gc'], f"⭐ {stats['fantasy_power']}")
            self.tree.insert("", "end", values=values, tags=(tag,))

    def refresh_data(self):
        """
        Simula la actualización de los valores Fantasy basada en noticias y rendimiento reciente.
        """
        teams_to_update = random.sample(list(self.teams_data.keys()), k=random.randint(3, 5))
        updated_teams_info = []

        for team in teams_to_update:
            change = random.randint(-4, 4) # El valor puede subir o bajar
            old_value = self.teams_data[team]['fantasy_power']
            new_value = max(40, min(100, old_value + change))
            self.teams_data[team]['fantasy_power'] = new_value
            
            if change > 0:
                updated_teams_info.append(f"📈 {team}: {old_value} -> {new_value}")
            elif change < 0:
                updated_teams_info.append(f"📉 {team}: {old_value} -> {new_value}")

        self.update_classification_table()
        
        if updated_teams_info:
            messagebox.showinfo("Mercado Fantasy Actualizado", 
                                "El Poder Fantasy se ha actualizado por noticias y rendimientos:\n\n" + 
                                "\n".join(updated_teams_info))
        else:
            messagebox.showinfo("Mercado Fantasy Estable", "No hubo cambios significativos en el mercado Fantasy.")

    def predict_match_advanced(self, local_team, away_team):
        """Algoritmo de predicción basado en el consenso Fantasy y estadísticas reales."""
        local = self.teams_data[local_team]; away = self.teams_data[away_team]
        
        # 1. Fuerza por Estadísticas (50% peso)
        stats_local = (local['pts'] * 2 + (local['gf'] - local['gc']))
        stats_away = (away['pts'] * 2 + (away['gf'] - away['gc']))

        # 2. Fuerza por Poder Fantasy (50% peso)
        fantasy_local = local['fantasy_power'] * 2.5 # Multiplicador para equiparar escalas
        fantasy_away = away['fantasy_power'] * 2.5

        # 3. Combinación Ponderada
        local_strength = (stats_local * self.prediction_weights['stats_weight']) + \
                         (fantasy_local * self.prediction_weights['fantasy_weight'])
        away_strength = (stats_away * self.prediction_weights['stats_weight']) + \
                        (fantasy_away * self.prediction_weights['fantasy_weight'])

        # 4. Aplicar ventaja de campo
        local_strength *= self.prediction_weights['home_advantage']

        # Predicción de goles
        goal_diff = abs(local_strength - away_strength) / 50
        if local_strength > away_strength:
            local_goals = int(random.choice([1, 2]) + goal_diff)
            away_goals = int(random.choice([0, 1]))
        elif away_strength > local_strength:
            away_goals = int(random.choice([1, 2]) + goal_diff)
            local_goals = int(random.choice([0, 1]))
        else:
            local_goals = away_goals = random.choice([0, 1, 2])
        
        local_goals = min(4, local_goals); away_goals = min(4, away_goals)

        if local_goals > away_goals: winner = local_team
        elif away_goals > local_goals: winner = away_team
        else: winner = "Empate"
        
        total_strength = local_strength + away_strength
        if total_strength == 0: total_strength = 1
        confidence = min(98, 60 + (abs(local_strength - away_strength) / total_strength * 40))
        return {"local_goals": local_goals, "away_goals": away_goals, "winner": winner, "confidence": f"{confidence:.1f}%"}

    def show_predictions_window(self):
        """Crea la ventana de predicciones."""
        pred_window = tk.Toplevel(self.root); pred_window.title("🎯 Predicciones de la Jornada"); pred_window.geometry("700x600"); pred_window.configure(bg=self.colors["bg"])
        canvas = tk.Canvas(pred_window, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(pred_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0,10))
        ttk.Label(scrollable_frame, text=f"✓ Predicciones basadas en el consenso Fantasy.", style="Success.TLabel").pack(pady=(0, 10), padx=10)
        for match in self.upcoming_matches:
            prediction = self.predict_match_advanced(match["local"], match["visitante"])
            card = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=15); card.pack(fill="x", padx=10, pady=5)
            ttk.Label(card, text=f"{match['local']} vs {match['visitante']}", style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(card, text=match['desc'], style="CardInfo.TLabel").pack(anchor="w")
            result_frame = ttk.Frame(card, style="Card.TFrame"); result_frame.pack(pady=10)
            ttk.Label(result_frame, text=prediction['local_goals'], style="CardScore.TLabel").pack(side="left", padx=10)
            ttk.Label(result_frame, text="-", style="CardScore.TLabel", foreground=self.colors["text_secondary"]).pack(side="left")
            ttk.Label(result_frame, text=prediction['away_goals'], style="CardScore.TLabel").pack(side="left", padx=10)
            ttk.Label(card, text=f"Ganador: {prediction['winner']}", style="CardInfo.TLabel", font=("Segoe UI", 10, "bold"), foreground=self.colors["text"]).pack()
            ttk.Label(card, text=f"Confianza: {prediction['confidence']}", style="CardInfo.TLabel").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = LaLigaPredictorApp(root)
    root.mainloop()
