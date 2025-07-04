#!/usr/bin/env python3
"""
GTI700 Lab 6 - Temperature Data Analysis Script
Team: Équipe 05

Statistical analysis of temperature monitoring data using Pandas.
Calculates system performance metrics and generates reports.

Analyzes:
- Temperature statistics (mean, std, min, max)
- Threshold violation patterns  
- System performance metrics
- Data quality assessment

Usage: python3 analysis_equipe_05.py

Author: Mohamed-Amine Djelloud
Course: GTI700 - École de technologie supérieure
"""
import pandas as pd
import time
import os

def analyze_data():
    """Analyser les données du fichier CSV avec Pandas"""
    
    print("📊 DÉMARRAGE DE L'ANALYSE DES DONNÉES")
    print("=" * 40)
    
    start_time = time.time()
    
    # Vérifier que le fichier existe
    if not os.path.exists('results_equipe_05.csv'):
        print("❌ ERREUR: Le fichier 'results_equipe_xx.csv' n'existe pas!")
        print("💡 Assurez-vous d'avoir exécuté le script principal d'abord.")
        return None
    
    try:
        # Lire le fichier CSV
        print("📂 Lecture du fichier CSV...")
        df = pd.read_csv('results_equipe_05.csv')
        
        # Vérifier que le fichier n'est pas vide
        if df.empty:
            print("❌ ERREUR: Le fichier CSV est vide!")
            return None
        
        print(f"✅ Données chargées: {len(df)} enregistrements")
        
        # Convertir la colonne température en numérique (au cas où)
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['limit_max'] = pd.to_numeric(df['limit_max'], errors='coerce')
        df['limit_min'] = pd.to_numeric(df['limit_min'], errors='coerce')
        
        # Calculer les statistiques demandées
        print("🔢 Calcul des statistiques...")
        
        # i) Température moyenne
        temp_moyenne = df['temperature'].mean()
        
        # ii) Limite maximale définie (la plus haute valeur atteinte)
        limite_max_definie = df['limit_max'].max()
        
        # iii) Limite minimale définie (la plus basse valeur atteinte)
        limite_min_definie = df['limit_min'].min()
        
        # iv) Nombre de violations limite inférieure (dernière valeur)
        violations_inf = df['violations_min'].iloc[-1] if len(df) > 0 else 0
        
        # v) Nombre de violations limite supérieure (dernière valeur)
        violations_sup = df['violations_max'].iloc[-1] if len(df) > 0 else 0
        
        # vi) Temps d'exécution de ce script
        end_time = time.time()
        temps_execution = end_time - start_time
        
        # Afficher les résultats
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS DE L'ANALYSE")
        print("=" * 50)
        print(f"i)   Température moyenne: {temp_moyenne:.2f}°C")
        print(f"ii)  Limite maximale définie: {limite_max_definie:.1f}°C")
        print(f"iii) Limite minimale définie: {limite_min_definie:.1f}°C")
        print(f"iv)  Violations limite inférieure: {violations_inf}")
        print(f"v)   Violations limite supérieure: {violations_sup}")
        print(f"vi)  Temps d'exécution du script: {temps_execution:.6f} secondes")
        print("=" * 50)
        
        # Statistiques supplémentaires utiles
        print("\n📈 STATISTIQUES SUPPLÉMENTAIRES:")
        print(f"🌡️  Température min mesurée: {df['temperature'].min():.2f}°C")
        print(f"🌡️  Température max mesurée: {df['temperature'].max():.2f}°C")
        print(f"📊 Écart-type température: {df['temperature'].std():.2f}°C")
        print(f"🚨 Total violations: {violations_inf + violations_sup}")
        print(f"📏 Nombre total de mesures: {len(df)}")
        
        # Distribution des statuts
        print(f"\n📋 DISTRIBUTION DES STATUTS:")
        status_counts = df['status'].value_counts()
        for status, count in status_counts.items():
            percentage = (count / len(df)) * 100
            print(f"   {status}: {count} fois ({percentage:.1f}%)")
        
        # Retourner les résultats pour d'éventuels traitements supplémentaires
        results = {
            'temp_moyenne': temp_moyenne,
            'limite_max': limite_max_definie,
            'limite_min': limite_min_definie,
            'violations_inf': violations_inf,
            'violations_sup': violations_sup,
            'temps_execution': temps_execution,
            'total_mesures': len(df),
            'temp_min_mesuree': df['temperature'].min(),
            'temp_max_mesuree': df['temperature'].max(),
            'ecart_type': df['temperature'].std()
        }
        
        print(f"\n✅ Analyse terminée en {temps_execution:.6f} secondes")
        
        return results
        
    except pd.errors.EmptyDataError:
        print("❌ ERREUR: Le fichier CSV est vide ou mal formaté!")
        return None
    except pd.errors.ParserError as e:
        print(f"❌ ERREUR de parsing CSV: {e}")
        return None
    except Exception as e:
        print(f"❌ ERREUR inattendue: {e}")
        return None

def save_analysis_results(results):
    """Sauvegarder les résultats d'analyse dans un fichier"""
    if results is None:
        return
    
    try:
        with open('analysis_results_equipe_05.txt', 'w') as f:
            f.write("RÉSULTATS D'ANALYSE - SYSTÈME DE TEMPÉRATURE\n")
            f.write("=" * 50 + "\n")
            f.write(f"Température moyenne: {results['temp_moyenne']:.2f}°C\n")
            f.write(f"Limite maximale définie: {results['limite_max']:.1f}°C\n")
            f.write(f"Limite minimale définie: {results['limite_min']:.1f}°C\n")
            f.write(f"Violations limite inférieure: {results['violations_inf']}\n")
            f.write(f"Violations limite supérieure: {results['violations_sup']}\n")
            f.write(f"Temps d'exécution: {results['temps_execution']:.6f} secondes\n")
            f.write(f"Total mesures: {results['total_mesures']}\n")
        
        print(f"💾 Résultats sauvegardés dans: analysis_results_equipe_05.txt")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde résultats: {e}")

if __name__ == '__main__':
    print("🐍 SCRIPT D'ANALYSE PANDAS")
    print("Analyseur de données de température IoT")
    print("-" * 40)
    
    # Exécuter l'analyse
    results = analyze_data()
    
    # Optionnel: sauvegarder les résultats
    if results:
        save_analysis_results(results)
    
    print("\n🏁 FIN DE L'ANALYSE")
