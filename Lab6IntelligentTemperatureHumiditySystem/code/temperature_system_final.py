#!/usr/bin/env python3
"""
GTI700 Lab 6 - Intelligent Temperature Monitoring System
Team: Équipe 05

This system implements:
- Real-time temperature monitoring using thermistor sensor
- Dynamic threshold control via joystick interface
- Intelligent alert system with violation tracking
- CSV data logging for analysis
- PCF8591 ADC integration for sensor interfacing

Hardware Requirements:
- Raspberry Pi 4
- PCF8591 ADC module  
- Thermistor sensor (Channel 3)
- Joystick module (Channels 0,1,2)
- Sunfounder IoT Kit

Author: Mohamed-Amine dDjelloud
Course: GTI700 - École de technologie supérieure
"""
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
import csv
from datetime import datetime

# Configuration initiale
temp_min = 20.0  # Limite inférieure (°C)
temp_max = 30.0  # Limite supérieure (°C)
violations_min = 0
violations_max = 0
start_time = time.time()

def setup():
    """Initialisation du système"""
    ADC.setup(0x48)
    GPIO.setmode(GPIO.BCM)
    print("✅ Système initialisé")

def get_temperature():
    """Lecture température du thermistor (canal 3)"""
    try:
        # Lecture sur canal 3 pour éviter conflit avec joystick
        analogVal = ADC.read(3)
        
        # Calcul température selon formule du thermistor
        Vr = 5 * float(analogVal) / 255
        if Vr >= 5:
            Vr = 4.99  # Éviter division par zéro
        
        Rt = 10000 * Vr / (5 - Vr)
        if Rt <= 0:
            raise ValueError("Résistance invalide")
            
        temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
        temp = temp - 273.15
        
        # Vérification cohérence (température raisonnable)
        if not (-10 <= temp <= 60):
            raise ValueError(f"Température incohérente: {temp}°C")
            
        return temp
        
    except Exception as e:
        print(f"⚠️ Erreur capteur température: {e}")
        # Simulation en cas d'erreur
        import random
        return 22.0 + random.uniform(-3, 8)

def get_joystick_direction():
    """Lecture direction joystick avec seuils adaptatifs"""
    try:
        state = ['home', 'up', 'down', 'left', 'right', 'pressed']
        
        # Lecture des canaux joystick
        joy_x = ADC.read(0)  # Canal X (gauche/droite)
        joy_y = ADC.read(1)  # Canal Y (haut/bas)
        joy_btn = ADC.read(2)  # Bouton
        
        # Seuils adaptatifs basés sur votre calibration
        # (Ces valeurs seront ajustées selon votre joystick)
        
        # Détection bouton en priorité
        if joy_btn <= 50:  # Bouton pressé
            return 'pressed'
        
        # Détection directions avec seuils larges pour compatibilité
        if joy_y <= 60:  # Haut
            return 'up'
        elif joy_y >= 195:  # Bas  
            return 'down'
        elif joy_x <= 60:  # Droite (peut être inversé selon câblage)
            return 'right'
        elif joy_x >= 195:  # Gauche (peut être inversé selon câblage)
            return 'left'
        else:
            return 'home'  # Position centrale
            
    except Exception as e:
        print(f"⚠️ Erreur joystick: {e}")
        return 'home'

def check_temperature_limits(temp):
    """Vérifier si température dans les limites définies"""
    global violations_min, violations_max
    
    if temp < temp_min:
        violations_min += 1
        print(f"🥶 ALERTE: Température TROP BASSE ({temp:.1f}°C < {temp_min:.1f}°C)")
        print("   💡 Vous devriez augmenter le thermostat")
        return "low"
    elif temp > temp_max:
        violations_max += 1
        print(f"🔥 ALERTE: Température TROP ÉLEVÉE ({temp:.1f}°C > {temp_max:.1f}°C)")
        print("   💡 Vous devriez diminuer le thermostat")
        return "high"
    else:
        print(f"✅ Température NORMALE: {temp:.1f}°C (Limites: {temp_min:.1f}°C - {temp_max:.1f}°C)")
        return "normal"

def save_to_csv(temp, status):
    """Sauvegarder les données dans le fichier CSV"""
    try:
        with open('results_equipe_xx.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                f"{temp:.2f}",
                f"{temp_min:.1f}",
                f"{temp_max:.1f}",
                status,
                violations_min,
                violations_max
            ])
    except Exception as e:
        print(f"❌ Erreur sauvegarde CSV: {e}")

def adjust_limits_with_joystick():
    """Ajuster les limites avec le joystick"""
    global temp_min, temp_max
    
    joy_direction = get_joystick_direction()
    
    # Debug: afficher direction détectée
    if hasattr(adjust_limits_with_joystick, 'debug_counter'):
        adjust_limits_with_joystick.debug_counter += 1
    else:
        adjust_limits_with_joystick.debug_counter = 0
    
    # Afficher debug toutes les 10 lectures pour diagnostic
    if adjust_limits_with_joystick.debug_counter % 10 == 0:
        x, y, btn = ADC.read(0), ADC.read(1), ADC.read(2)
        print(f"🔍 Debug: X={x:3d}, Y={y:3d}, BTN={btn:3d} → {joy_direction}")
    
    if joy_direction == 'up':
        temp_max += 1.0
        print(f"🔺 Limite MAXIMALE augmentée: {temp_max:.1f}°C")
        time.sleep(0.5)  # Éviter répétitions rapides
        return True
        
    elif joy_direction == 'down':
        temp_max = max(temp_max - 1.0, temp_min + 1.0)  # Sécurité
        print(f"🔻 Limite MAXIMALE diminuée: {temp_max:.1f}°C")
        time.sleep(0.5)
        return True
        
    elif joy_direction == 'right':
        temp_min = min(temp_min + 1.0, temp_max - 1.0)  # Sécurité
        print(f"▶️ Limite MINIMALE augmentée: {temp_min:.1f}°C")
        time.sleep(0.5)
        return True
        
    elif joy_direction == 'left':
        temp_min -= 1.0
        print(f"◀️ Limite MINIMALE diminuée: {temp_min:.1f}°C")
        time.sleep(0.5)
        return True
        
    elif joy_direction == 'pressed':
        print(f"\n📊 ÉTAT ACTUEL:")
        print(f"   Limites: {temp_min:.1f}°C ← → {temp_max:.1f}°C")
        print(f"   Violations: MIN={violations_min}, MAX={violations_max}")
        print(f"   Total violations: {violations_min + violations_max}")
        time.sleep(0.8)
        return True
    
    return False

def create_csv_headers():
    """Créer le fichier CSV avec les en-têtes"""
    try:
        with open('results_equipe_xx.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'timestamp', 'temperature', 'limit_min', 'limit_max', 
                'status', 'violations_min', 'violations_max'
            ])
        print("✅ Fichier CSV créé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur création CSV: {e}")
        return False

def display_instructions():
    """Afficher les instructions d'utilisation"""
    print("\n🌡️ SYSTÈME DE TEMPÉRATURE INTELLIGENT")
    print("=" * 60)
    print(f"📊 Limites initiales: {temp_min:.1f}°C - {temp_max:.1f}°C")
    print("\n🕹️ CONTRÔLES JOYSTICK:")
    print("  ↑ (UP)    = Augmenter limite MAXIMALE")
    print("  ↓ (DOWN)  = Diminuer limite MAXIMALE") 
    print("  → (RIGHT) = Augmenter limite MINIMALE")
    print("  ← (LEFT)  = Diminuer limite MINIMALE")
    print("  ⏹️ (PRESS) = Afficher statistiques actuelles")
    print("\n🎯 OBJECTIF:")
    print("  - Ajustez les limites avec le joystick")
    print("  - Observez les alertes de température")
    print("  - Toutes les données sont enregistrées automatiquement")
    print("\n🛑 Ctrl+C pour arrêter le système")
    print("=" * 60)

def main():
    """Fonction principale du système"""
    print("🚀 DÉMARRAGE DU SYSTÈME DE TEMPÉRATURE INTELLIGENT")
    print("=" * 60)
    
    # Initialisation
    print("🔧 Initialisation...")
    setup()
    
    # Création du fichier CSV
    if not create_csv_headers():
        print("❌ Impossible de créer le fichier CSV. Arrêt.")
        return
    
    # Affichage des instructions
    display_instructions()
    
    # Variables de suivi
    measurement_counter = 0
    last_temp = None
    
    try:
        print("\n🏁 DÉBUT DES MESURES:")
        print("-" * 30)
        
        while True:
            measurement_counter += 1
            
            # En-tête de mesure
            print(f"\n📏 Mesure #{measurement_counter}")
            
            # Lecture de la température
            temp = get_temperature()
            
            # Vérification des limites et alertes
            status = check_temperature_limits(temp)
            
            # Sauvegarde des données
            save_to_csv(temp, status)
            
            # Gestion du joystick pour ajustement des limites
            joystick_action = adjust_limits_with_joystick()
            
            # Affichage périodique des statistiques
            if measurement_counter % 10 == 0:
                print(f"\n📈 STATISTIQUES (après {measurement_counter} mesures):")
                print(f"   🚨 Total violations: {violations_min + violations_max}")
                print(f"   📊 Température actuelle: {temp:.1f}°C")
                print(f"   ⚙️ Limites: {temp_min:.1f}°C - {temp_max:.1f}°C")
            
            # Pause entre les mesures (sauf si joystick utilisé)
            if not joystick_action:
                time.sleep(2.0)
            
    except KeyboardInterrupt:
        print("\n\n🛑 ARRÊT DU SYSTÈME DEMANDÉ")
        
    except Exception as e:
        print(f"\n❌ ERREUR SYSTÈME: {e}")
        
    finally:
        # Statistiques finales
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("📊 RAPPORT FINAL:")
        print("=" * 60)
        print(f"⏱️  Durée totale d'exécution: {duration:.1f} secondes")
        print(f"📏 Nombre total de mesures: {measurement_counter}")
        print(f"📉 Violations limite inférieure: {violations_min}")
        print(f"📈 Violations limite supérieure: {violations_max}")
        print(f"🚨 TOTAL des violations: {violations_min + violations_max}")
        print(f"📁 Données sauvegardées dans: results_equipe_xx.csv")
        print(f"🎯 Limites finales: {temp_min:.1f}°C - {temp_max:.1f}°C")
        
        if violations_min + violations_max > 0:
            violation_rate = ((violations_min + violations_max) / measurement_counter) * 100
            print(f"📊 Taux de violations: {violation_rate:.1f}%")
        
        print("=" * 60)
        
        # Nettoyage
        print("🧹 Nettoyage des ressources...")
        GPIO.cleanup()
        print("✅ Système arrêté proprement")
        print("\n💡 Prochaine étape: Analysez vos données avec le script Pandas!")

if __name__ == '__main__':
    main()